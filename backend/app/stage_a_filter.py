"""
Layer 4 - Stage A: Recall Pre-Filter
Runs on 100% of incoming reports in milliseconds.
Optimizes strictly for RECALL — a missed SIF positive is the catastrophic failure mode.
Combines:
1. FAISS vector similarity to curated High-SIF hazard exemplars
2. High-sensitivity domain keyword & regex triggers
"""

import re
import time
from typing import Dict, Any, List, Tuple
from .vector_store import vector_store

# High-Recall Trigger Lexicon (Energy, Barrier Failure, and Line of Fire Precursors)
STAGE_A_TRIGGERS = [
    {
        "category": "Gravitational / Dropped / Lifting",
        "keywords": ["dropped", "falling", "suspended load", "sling", "hoist", "crane", "shackle", "winch", "rigging", "dola", "rashi", "overhead", "catwalk", "unsecured"]
    },
    {
        "category": "Pressurized Energy / Well Control",
        "keywords": ["pressure", "psi", "bar", "burst", "rupture", "whipcheck", "kelly hose", "blew out", "bop", "kick", "flange", "hammer union", "manifold"]
    },
    {
        "category": "Toxic / Confined Space / Atmospheric",
        "keywords": ["h2s", "confined space", "cellar pit", "mud pit", "tank entry", "vessel", "asphyxiation", "oxygen", "gas detector", "lel", "scba", "eebd", "hawa", "chatai"]
    },
    {
        "category": "Electrical / Stored Energy Isolation",
        "keywords": ["loto", "lockout", "tagout", "energized", "440v", "11kv", "live wire", "breaker", "arc flash", "isolation switch", "stored energy"]
    },
    {
        "category": "Line of Fire / Rotating Rig Machinery",
        "keywords": ["line of fire", "rotary table", "cathead", "tongs", "iron roughneck", "pinch point", "entanglement", "fasi", "fas gaya", "fasi goli"]
    },
    {
        "category": "Working at Height",
        "keywords": ["working at height", "monkey board", "derrick", "crown block", "ladder fall", "scaffold", "safety harness", "lanyard", "tie off", "fall arrest"]
    },
    {
        "category": "Hot Work / Flammable Atmosphere",
        "keywords": ["hot work", "welding", "grinding", "torch cutting", "open flame", "spark in zone", "fire blanket", "explosimeter"]
    },
    {
        "category": "Near-Miss Weak Signal Escapes",
        "keywords": ["bach goli", "bach gaya", "narrowly avoided", "stepped back", "inches away", "missed worker", "near miss", "fell close", "almost struck", "bipod", "khatra", "dangoriya"]
    }
]

SIMILARITY_THRESHOLD = 0.14  # Calibrated for high recall against High-SIF exemplars

def run_stage_a_prefilter(report_text: str, features: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Executes Stage A Recall Pre-filter.
    Returns:
    {
        "flagged": bool,
        "score": float,
        "triggers": list of matched trigger rules,
        "top_exemplar_match": str,
        "similarity_score": float,
        "latency_ms": float
    }
    """
    t0 = time.perf_counter()
    lower_text = report_text.lower()
    
    # 1. Check Keyword Triggers
    matched_triggers = []
    for trig_group in STAGE_A_TRIGGERS:
        matched_kws = [kw for kw in trig_group["keywords"] if kw in lower_text]
        if matched_kws:
            matched_triggers.append(f"{trig_group['category']} ({', '.join(matched_kws[:3])})")

    # 2. Vector Embedding Search against High-SIF Exemplars
    high_sif_matches = vector_store.query_exemplars(report_text, top_k=2, target_class="High")
    top_similarity = high_sif_matches[0]["similarity"] if high_sif_matches else 0.0
    top_exemplar_id = high_sif_matches[0]["id"] if high_sif_matches else "None"

    # 3. Decision Logic: Optimizes for RECALL
    # Flagged if ANY trigger fired OR vector similarity exceeds threshold
    has_triggers = len(matched_triggers) > 0
    high_similarity = top_similarity >= SIMILARITY_THRESHOLD
    
    # Barrier failure check from Layer 3 features
    barrier_failed = False
    if features:
        barrier_status = features.get("barrier_status", "")
        if any(w in barrier_status for w in ["Failed", "Bypassed", "Missing", "Degraded"]):
            barrier_failed = True
            if "Barrier Degradation Detected" not in matched_triggers:
                matched_triggers.append(f"Barrier Status: {barrier_status}")

    flagged = has_triggers or high_similarity or barrier_failed
    
    # Calculate composite Stage A recall score (0.0 to 1.0)
    trigger_weight = min(1.0, len(matched_triggers) * 0.25)
    composite_score = max(top_similarity, (top_similarity * 0.4 + trigger_weight * 0.6))
    if flagged and composite_score < 0.35:
        composite_score = 0.40  # Minimum floor for any flagged event
        
    latency_ms = (time.perf_counter() - t0) * 1000.0

    return {
        "flagged": flagged,
        "score": round(float(composite_score), 3),
        "triggers": matched_triggers,
        "top_exemplar_id": top_exemplar_id,
        "similarity_score": round(float(top_similarity), 3),
        "latency_ms": round(latency_ms, 2)
    }
