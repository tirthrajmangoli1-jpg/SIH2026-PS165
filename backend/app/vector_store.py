"""
Vector Store for Curated SIF Precursor Exemplars and Human-in-the-Loop Feedback.
Built on FAISS (IndexFlatIP with L2 normalized dense vectors) and domain semantic embeddings.
Supports dynamic live updates without retrain.
"""

import os
import json
import faiss
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer

# Seed Curated Exemplars (Covering High SIF Near-Misses, Medium SIF, and Low SIF)
INITIAL_CURATED_EXEMPLARS: List[Dict[str, Any]] = [
    {
        "id": "EX-01",
        "text": "During tripping out at Rig OIL-04, the 85 kg Kelly bushing detached from hoist at 14m height and fell to the rig floor, landing 1 meter from a roughneck. No injury sustained as worker stepped back to grab slips.",
        "energy_source": "Gravitational Potential Energy (Heavy suspended equipment)",
        "barrier_status": "Failed (Hoist safety latch pin sheared; drop zone barricade degraded)",
        "sif_potential": "High",
        "sif_score": 0.95,
        "iogp_rule": "Safe Mechanical Lifting",
        "rationale": "Massive gravitational potential energy at 14m height. Primary barrier (hoist safety pin) failed completely. Worker was in direct line of fire; fatality was prevented solely by chance/timing, not an engineered barrier. Textbook High-SIF near-miss despite 0 reported injuries.",
        "source": "initial_curated",
        "version": 1
    },
    {
        "id": "EX-02",
        "text": "At Moran Production Station, a contractor entered the crude oil storage tank cellar pit without atmospheric gas test or standby watchman to retrieve a dropped wrench. Felt dizzy from H2S fumes and climbed out.",
        "energy_source": "Chemical / Asphyxiant Energy (H2S toxic gas / hydrocarbon vapors)",
        "barrier_status": "Bypassed / Defeated (No gas testing, no PTW, no standby sentry)",
        "sif_potential": "High",
        "sif_score": 0.93,
        "iogp_rule": "Confined Space",
        "rationale": "High toxic chemical energy (H2S/flammable vapor in cellar). All administrative and physical barriers (entry permit, atmospheric testing, SCBA, standby watchman) were bypassed. Worker experienced early toxic symptoms; imminent fatality risk averted purely by self-egress.",
        "source": "initial_curated",
        "version": 1
    },
    {
        "id": "EX-03",
        "text": "Standpipe manifold pressurized to 3200 psi during cement pumping. Kelly hose whipcheck safety cable was found missing. High pressure fluid hammer union developed pinhole jetting into walk path.",
        "energy_source": "High Pressure Fluid Energy (3200 psi hydraulic head)",
        "barrier_status": "Missing / None (Whipcheck safety restraint absent; pressure seal degraded)",
        "sif_potential": "High",
        "sif_score": 0.90,
        "iogp_rule": "Line of Fire",
        "rationale": "Extreme hydraulic energy (>3000 psi) with missing whipcheck secondary restraint. A complete union failure would cause violent whipping capable of fatal blunt force or high-pressure fluid injection.",
        "source": "initial_curated",
        "version": 1
    },
    {
        "id": "EX-04",
        "text": "Electrician was preparing to test 440V mud pump motor terminal box. Breaker was switched off at MCC, but padlock was not applied and voltage test before touch was skipped. Shift supervisor halted work before touching lugs.",
        "energy_source": "High Voltage Electrical Energy (440V)",
        "barrier_status": "Degraded / Bypassed (LOTO padlock omitted, test-before-touch omitted)",
        "sif_potential": "High",
        "sif_score": 0.88,
        "iogp_rule": "Energy Isolation",
        "rationale": "Lethal electrical potential. LOTO positive isolation was defeated; absence of padlock meant circuit could be re-energized inadvertently by another operator. Intervened prior to contact.",
        "source": "initial_curated",
        "version": 1
    },
    {
        "id": "EX-05",
        "text": "Roustabout was grinding drill collar lifting sub flange inside rig workshop without safety glasses. Flying metal sliver struck upper cheek, causing minor superficial 3mm scratch. First aid antiseptic applied.",
        "energy_source": "Low Mechanical Kinetic Energy (Minor particulate fragment)",
        "barrier_status": "Bypassed (Eye PPE omitted, but machinery guard in place)",
        "sif_potential": "Low",
        "sif_score": 0.15,
        "iogp_rule": "Work Authorisation",
        "rationale": "Low localized energy. While PPE rule was breached, the particulate mass lacks energy capacity to cause serious life-threatening injury or fatality under normal workshop conditions.",
        "source": "initial_curated",
        "version": 1
    },
    {
        "id": "EX-06",
        "text": "Administrative clerk tripped on edge of door mat entering Duliajan base office and bruised knee. Ice pack administered at camp dispensary, returned to desk duties immediately.",
        "energy_source": "Negligible Energy (Walking level fall)",
        "barrier_status": "Intact / Non-Hazardous Environment",
        "sif_potential": "Low",
        "sif_score": 0.05,
        "iogp_rule": "Work Authorisation",
        "rationale": "Zero industrial energy source. Routine slip/trip at grade level in non-hazardous office environment. Zero fatality or permanent disability potential.",
        "source": "initial_curated",
        "version": 1
    },
    {
        "id": "EX-07",
        "text": "Crane operator was offloading drill pipes from flatbed trailer. Tagline was tied loosely, causing the bundle to swing slightly beyond designated rack boundary before coming to rest against buffer stanchion.",
        "energy_source": "Medium Mechanical Kinetic Energy (Swinging pipe bundle)",
        "barrier_status": "Degraded (Sub-optimal tagline tension, but exclusion zone maintained)",
        "sif_potential": "Medium",
        "sif_score": 0.52,
        "iogp_rule": "Safe Mechanical Lifting",
        "rationale": "Moderate energy present in suspended pipe bundle. Tagline guidance was loose (degraded barrier), but secondary barrier (barricaded exclusion zone) held, preventing personnel from being in the line of fire.",
        "source": "initial_curated",
        "version": 1
    }
]

class ExemplarVectorStore:
    def __init__(self):
        self.exemplars: List[Dict[str, Any]] = [dict(e) for e in INITIAL_CURATED_EXEMPLARS]
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.index: Optional[faiss.IndexFlatIP] = None
        self.rebuild_index()

    def rebuild_index(self):
        """Re-fits vectorizer and builds normalized FAISS IndexFlatIP index."""
        texts = [
            f"{e['text']} {e['energy_source']} {e['barrier_status']} {e['iogp_rule']}"
            for e in self.exemplars if e.get("is_active", True)
        ]
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=512,
            sublinear_tf=True
        )
        X = self.vectorizer.fit_transform(texts).toarray().astype("float32")
        faiss.normalize_L2(X)
        self.index = faiss.IndexFlatIP(X.shape[1])
        self.index.add(X)

    def query_exemplars(self, query_text: str, top_k: int = 3, target_class: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves top_k most semantically similar exemplars.
        Optionally filters by target_class ('High', 'Medium', 'Low').
        """
        if not self.index or not self.vectorizer:
            self.rebuild_index()

        q_vec = self.vectorizer.transform([query_text]).toarray().astype("float32")
        faiss.normalize_L2(q_vec)
        
        # Search more if filtering is required
        search_k = min(len(self.exemplars), max(top_k * 3, 5))
        distances, indices = self.index.search(q_vec, search_k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.exemplars):
                continue
            item = self.exemplars[idx]
            if target_class and item.get("sif_potential") != target_class:
                continue
            res_item = dict(item)
            res_item["similarity"] = float(dist)
            results.append(res_item)
            if len(results) >= top_k:
                break
                
        return results

    def add_override_exemplar(
        self,
        incident_id: str,
        text: str,
        energy_source: str,
        barrier_status: str,
        sif_potential: str,
        sif_score: float,
        iogp_rule: str,
        rationale: str,
        reviewer_name: str
    ) -> Dict[str, Any]:
        """
        Writes a reviewer override into the versioned exemplar vector store.
        Immediately re-indexes so future classifications reflect reviewer knowledge.
        """
        new_id = f"EX-REV-{len(self.exemplars) + 1:03d}"
        new_item = {
            "id": new_id,
            "incident_id": incident_id,
            "text": text,
            "energy_source": energy_source,
            "barrier_status": barrier_status,
            "sif_potential": sif_potential,
            "sif_score": sif_score,
            "iogp_rule": iogp_rule,
            "rationale": f"[Reviewer Override by {reviewer_name}]: {rationale}",
            "source": "human_override",
            "version": 1,
            "is_active": True
        }
        self.exemplars.append(new_item)
        self.rebuild_index()
        return new_item

    def list_all_exemplars(self) -> List[Dict[str, Any]]:
        return self.exemplars

# Global singleton instance
vector_store = ExemplarVectorStore()
