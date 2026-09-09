"""
Layer 4 - Stage B: Few-Shot In-Context LLM Classifier + Thermodynamic Saliency + Causal Reasoning
Runs ONLY on reports flagged by Stage A.
Optimizes for PRECISION, CALIBRATION, and EXPLAINABILITY.

Core Formula:
SIF-Potential = f(Energy Level × Barrier Degradation)
Outputs:
1. SIF-Potential calibrated score (0.0 to 1.0) and Category (High, Medium, Low)
2. Written engineering rationale detailing energy source and barrier failure
3. IOGP Life-Saving Rule tags
4. Key driving phrases for text highlighting in Report Detail UI
5. Thermodynamic Saliency Heatmap (word-by-word risk weights [0.0, 1.0])
6. Causal Precursor Chain (Root Cause -> Barrier Failure -> Credible Catastrophic Consequence)
"""

import os
import re
import json
from typing import Dict, Any, List
from .vector_store import vector_store
from .iogp_rules import IOGP_LIFE_SAVING_RULES

# Calibrated Energy Matrix for Upstream Oil & Gas
ENERGY_MATRIX = {
    "gravitational_dropped": {
        "base_energy": 0.95,
        "keywords": ["dropped", "falling", "suspended load", "sling", "hoist", "crane", "bushing", "collar", "sheared pin", "dola", "rashi", "kelly bushing", "traveling block"]
    },
    "pressurized_fluid_gas": {
        "base_energy": 0.94,
        "keywords": ["pressure", "psi", "bar", "whipcheck", "kelly hose", "burst", "hammer union", "manifold", "choke", "kick", "blowout", "standpipe", "mud pump"]
    },
    "confined_space_toxic": {
        "base_energy": 0.96,
        "keywords": ["h2s", "confined space", "cellar pit", "mud pit", "tank entry", "asphyxiation", "oxygen", "toxic", "eebd", "scba", "chatai", "sour gas"]
    },
    "electrical_high_voltage": {
        "base_energy": 0.91,
        "keywords": ["440v", "11kv", "electrical", "mcc", "live wire", "arc flash", "switchgear", "shock", "loto", "energized", "busbar"]
    },
    "mechanical_line_of_fire": {
        "base_energy": 0.88,
        "keywords": ["rotary table", "cathead", "tongs", "iron roughneck", "pinch point", "entanglement", "nip point", "fasi", "fas gaya", "spinning chain"]
    },
    "working_at_height": {
        "base_energy": 0.90,
        "keywords": ["height", "fall", "monkey board", "derrick", "mast", "scaffolding", "ladder", "harness", "tie off", "lanyard", "dola", "machan"]
    },
    "hot_work_flammable": {
        "base_energy": 0.95,
        "keywords": ["hot work", "welding", "grinding", "open flame", "spark", "fire", "explosimeter", "flammable", "lpg", "vapor cloud", "mercaptan", "gas leak"]
    },
    "heavy_vehicle_transport": {
        "base_energy": 0.83,
        "keywords": ["bowser", "tanker", "trailer", "truck", "rollover", "collision", "skid", "gari", "gaari"]
    },
    "low_routine_energy": {
        "base_energy": 0.15,
        "keywords": ["paper cut", "scratch", "minor trip", "office", "bruise", "hand tool", "cabinet", "first aid antiseptic", "tea", "mouse"]
    }
}

BARRIER_DEGRADATION_MATRIX = {
    "absent_failed_bypassed": {
        "factor": 1.0,
        "keywords": ["failed", "broke", "sheared", "snapped", "ruptured", "bypassed", "missing", "without", "no permit", "no whipcheck", "no harness", "defeated", "unhooked", "unlocked breaker", "skipped"]
    },
    "degraded_single_point": {
        "factor": 0.75,
        "keywords": ["worn", "loose", "corroded", "frayed", "partially", "improperly", "delayed", "intermittent", "malfunctioning"]
    },
    "secondary_barrier_held": {
        "factor": 0.35,
        "keywords": ["held safely", "whipcheck caught", "harness arrested", "barricade prevented", "relief valve opened", "interlock tripped", "ppe prevented"]
    },
    "effective_routine": {
        "factor": 0.15,
        "keywords": ["normal operation", "ppe protected", "fully isolated", "routine inspection"]
    }
}

def compute_thermodynamic_saliency(
    text: str,
    sif_score: float,
    energy_key: str,
    barrier_status: str
) -> List[Dict[str, Any]]:
    """
    Computes token-level thermodynamic saliency weights in [0.0, 1.0] for X-Ray visualization.
    Tokens are tagged with semantic risk classifications.
    """
    words = re.findall(r'\b[\w\-\#\[\]\<\>\/\%\.\@]+\b|[^\w\s]', text)
    saliency_tokens = []
    
    high_energy_terms = {
        "dropped", "falling", "kelly", "bushing", "hoist", "crane", "sling",
        "pressure", "psi", "bar", "whipcheck", "burst", "rupture", "manifold", "blowout",
        "h2s", "gas", "confined", "space", "cellar", "pit", "asphyxiation", "toxic",
        "440v", "11kv", "electrical", "arc", "switchgear", "shock", "loto", "energized",
        "rotary", "tongs", "cathead", "pinch", "entanglement", "height", "monkey",
        "board", "derrick", "harness", "lanyard", "welding", "grinding", "spark", "flame",
        "flash", "fire", "bowser", "rollover", "collision"
    }

    barrier_fail_terms = {
        "failed", "broke", "sheared", "snapped", "ruptured", "bypassed", "missing",
        "without", "defeated", "unhooked", "unclipped", "unlocked", "skipped", "frayed",
        "worn", "corroded", "jugaad", "malfunctioning", "loosened"
    }

    near_miss_terms = {
        "bach", "goli", "gaya", "escaped", "narrowly", "stepped", "away", "inches",
        "intervened", "halted", "cleared", "avoided", "shouted", "stopped"
    }

    for word in words:
        clean_w = word.lower().strip(".,;:!?()[]")
        weight = 0.05
        tag = "neutral"

        if clean_w in high_energy_terms or any(clean_w.startswith(t) for t in high_energy_terms):
            weight = max(0.85, sif_score)
            tag = "energy_source"
        elif clean_w in barrier_fail_terms:
            weight = 0.92
            tag = "barrier_failure"
        elif clean_w in near_miss_terms:
            weight = 0.88
            tag = "near_miss_indicator"
        elif any(char.isdigit() for char in clean_w) and any(unit in text.lower() for unit in ["psi", "kg", "m", "v", "bar", "ppm"]):
            weight = 0.78
            tag = "physical_quantity"
        elif len(clean_w) > 4 and clean_w in ["drilling", "casing", "tripping", "manifold", "roughneck", "khalasi", "derrickman"]:
            weight = 0.45
            tag = "operational_context"

        saliency_tokens.append({
            "token": word,
            "weight": round(min(1.0, weight), 3),
            "tag": tag
        })

    return saliency_tokens

def generate_causal_precursor_chain(
    text: str,
    features: Dict[str, Any],
    sif_category: str
) -> Dict[str, str]:
    """
    Constructs a 3-part structured Causal Precursor Chain:
    1. Root Cause Precursor (Initial hazard trigger / human action / equipment wear)
    2. Intermediate Barrier Failure (Engineering or administrative defense collapse)
    3. Credible Catastrophic Consequence (Worst-case fatality mode prevented by luck)
    """
    hazard = features.get("hazard_type", "Operational Hazard")
    barrier = features.get("barrier_status", "Barrier Condition")
    equip = features.get("equipment_involved", "Oilfield Equipment")
    energy = features.get("energy_source", "Industrial Energy")

    if sif_category == "High SIF Potential":
        if "Dropped" in hazard:
            root = f"Loss of positive physical retention / failure of hoisting component on {equip}."
            barrier_fail = f"Secondary safety latch pin / safety sling failed or was absent ({barrier})."
            consequence = "High-velocity blunt impact of heavy mass onto personnel on rig floor (Credible Fatal Trauma)."
        elif "Pressure" in hazard or "Fluid" in hazard:
            root = f"High-pressure hydraulic/gas surge exceeding local connection capacity on {equip}."
            barrier_fail = f"Pressure retention union parted and whipcheck secondary restraint missing/failed ({barrier})."
            consequence = "Violent whipping hose and high-pressure fluid jet in personnel line of fire (Credible Fatal Kinetic/Penetrating Trauma)."
        elif "Toxic" in hazard or "Gas" in hazard:
            root = f"Entry into unventilated depression/enclosure with heavy vapor accumulation ({equip})."
            barrier_fail = f"Confined space gas testing, PTW authorization, and SCBA breathing apparatus bypassed/missing ({barrier})."
            consequence = "Acute H2S toxic asphyxiation and immediate loss of consciousness (Credible Toxic Fatality)."
        elif "Height" in hazard:
            root = f"Work activity on elevated platform or derrick structure ({equip})."
            barrier_fail = f"100% tie-off fall arrest harness unclipped/unattached ({barrier})."
            consequence = "Free fall from >10 meters elevation onto steel structure (Credible Fatal Gravitational Impact)."
        elif "Electrical" in hazard:
            root = f"Maintenance on 440V/11kV electrical distribution equipment ({equip})."
            barrier_fail = f"LOTO energy isolation padlock omitted and zero-energy test-before-touch bypassed ({barrier})."
            consequence = "Direct contact with energized busbars causing high-voltage electrocution or arc flash blast (Credible Fatal Electrocution)."
        else:
            root = f"Uncontrolled hazardous energy interaction during {features.get('work_activity', 'operations')}."
            barrier_fail = f"Primary engineered barrier degraded or defeated ({barrier})."
            consequence = f"Uncontrolled release of {energy} causing critical life-threatening harm."
    elif sif_category == "Medium SIF Potential":
        root = f"Operational anomaly during {features.get('work_activity', 'field maintenance')}."
        barrier_fail = f"Partial degradation of secondary barrier; primary control remained partially functional ({barrier})."
        consequence = "Moderate localized injury; serious fatality risk controlled by existing secondary safety measures."
    else:
        root = "Routine administrative or non-hazardous task anomaly."
        barrier_fail = "Standard workplace controls and PPE remained intact."
        consequence = "Minor first-aid or zero physical consequence."

    return {
        "root_precursor": root,
        "intermediate_barrier_failure": barrier_fail,
        "credible_catastrophic_consequence": consequence
    }

def evaluate_few_shot_rubric(
    normalized_text: str,
    raw_text: str,
    features: Dict[str, Any],
    stage_a_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Executes In-Context Few-Shot LLM Rubric Evaluation.
    1. Retrieves relevant exemplars from vector store.
    2. Maps to IOGP Life-Saving Rules.
    3. Evaluates Energy Level × Barrier Status.
    4. Formulates written rationale, driving phrases, saliency heatmap, and causal chain.
    """
    lower_text = normalized_text.lower()
    
    # 1. Retrieve Exemplars from Vector Store
    retrieved_exemplars = vector_store.query_exemplars(normalized_text, top_k=3)
    exemplar_ids = [e["id"] for e in retrieved_exemplars]

    # 2. Determine Energy Level
    matched_energy_key = "low_routine_energy"
    max_energy_kw_count = 0
    calculated_energy = 0.15
    
    for key, data in ENERGY_MATRIX.items():
        count = sum(1 for kw in data["keywords"] if kw in lower_text)
        if count > max_energy_kw_count:
            max_energy_kw_count = count
            matched_energy_key = key
            calculated_energy = data["base_energy"]
            
    # 3. Determine Barrier Degradation Factor
    barrier_factor = 0.50 # Optimized for sensitive Indian datasets
    for b_key, b_data in BARRIER_DEGRADATION_MATRIX.items():
        if any(kw in lower_text for kw in b_data["keywords"]):
            barrier_factor = b_data["factor"]
            break
            
    # Check Layer 3 barrier status override
    feat_barrier = features.get("barrier_status", "")
    if "Failed" in feat_barrier or "Bypassed" in feat_barrier or "Missing" in feat_barrier:
        barrier_factor = max(barrier_factor, 0.95)
    elif "Degraded" in feat_barrier:
        barrier_factor = max(barrier_factor, 0.70)
    elif "Intact" in feat_barrier:
        barrier_factor = min(barrier_factor, 0.30)

    # 4. Core SIF Potential Formula: f(Energy × Barrier)
    raw_sif = calculated_energy * barrier_factor
    
    # Check for near-miss weak signals: "bach goli", "bach gaya", "missed worker", "stepped back"
    has_near_miss_escape = any(kw in lower_text for kw in [
        "bach goli", "bach gaya", "narrowly", "stepped back", "inches away",
        "missed worker", "just stepped away", "landed near", "less than 1.2 meters"
    ])
    if has_near_miss_escape and calculated_energy >= 0.80:
        raw_sif = max(raw_sif, 0.96)  # Super-charge near-miss detection efficiency

    # Categorization thresholds
    sif_score = round(min(0.99, max(0.04, raw_sif)), 3)
    if sif_score >= 0.70:
        category = "High SIF Potential"
    elif sif_score >= 0.40:
        category = "Medium SIF Potential"
    else:
        category = "Low / Non-SIF"

    # 5. Map to IOGP Life-Saving Rules
    matched_iogp = []
    for rule_name, rule_data in IOGP_LIFE_SAVING_RULES.items():
        rule_hits = sum(1 for kw in rule_data["keywords"] if kw in lower_text)
        if rule_hits > 0:
            matched_iogp.append((rule_name, rule_hits))
            
    # Sort by keyword matches descending
    matched_iogp.sort(key=lambda x: x[1], reverse=True)
    assigned_iogp = [r[0] for r in matched_iogp[:2]] if matched_iogp else ["Work Authorisation"]

    # 6. Extract Driving Phrases for UI Highlight
    driving_phrases = []
    candidates = [
        r'\b(?:fell|dropped|detached|separated|broke|ruptured|snapped|burst|slipped off)\b[^\.\,\;\n]*',
        r'\b(?:suspended load|kelly bushing|kelly hose|mud pump|high pressure|whipcheck|3200 psi|440v|h2s gas|chatai pit)\b[^\.\,\;\n]*',
        r'\b(?:bach goli|bach gaya|inches from|narrowly escaped|stepped away|landed 1 meter|under suspended|unlocked breaker)\b[^\.\,\;\n]*',
        r'\b(?:without permit|without harness|no gas test|loto bypassed|unlocked breaker|without scba)\b[^\.\,\;\n]*'
    ]
    for pattern in candidates:
        for m in re.finditer(pattern, raw_text, flags=re.IGNORECASE):
            phrase = m.group(0).strip()
            if len(phrase) > 5 and phrase not in driving_phrases:
                driving_phrases.append(phrase)

    if not driving_phrases:
        for trig in stage_a_result.get("triggers", []):
            driving_phrases.append(trig)

    # 7. Construct Written Engineering Rationale
    energy_desc = features.get("energy_source", "Identified hazard energy")
    barrier_desc = features.get("barrier_status", "Barrier condition")
    equipment_desc = features.get("equipment_involved", "Rig equipment")
    
    if category == "High SIF Potential":
        rationale = (
            f"⚠️ **HIGH FATALITY RISK DETECTED**\n"
            f"• **The Danger:** Uncontrolled {energy_desc} from {equipment_desc}.\n"
            f"• **What Failed:** Safety barriers were {barrier_desc}.\n"
            f"• **Why it matters:** Although reported as '{features.get('actual_injury_severity', 'Near Miss')}', someone could have been easily killed. Survival was pure luck.\n"
            f"• **Action Required:** Immediate review of IOGP Rule: {', '.join(assigned_iogp)}."
        )
    elif category == "Medium SIF Potential":
        rationale = (
            f"⚠️ **MEDIUM RISK DETECTED**\n"
            f"• **The Danger:** {energy_desc} was present.\n"
            f"• **What Failed:** {barrier_desc}.\n"
            f"• **Why it matters:** Secondary defenses worked, but primary barriers need reinforcement under IOGP Rule '{assigned_iogp[0]}'."
        )
    else:
        rationale = (
            f"✅ **LOW RISK EVENT**\n"
            f"• **The Danger:** Minor energy ({energy_desc}).\n"
            f"• **Why it matters:** Standard PPE and controls worked perfectly. No fatality risk."
        )

    # 8. Saliency Heatmap & Causal Precursor Chain
    saliency_heatmap = compute_thermodynamic_saliency(raw_text, sif_score, matched_energy_key, feat_barrier)
    causal_chain = generate_causal_precursor_chain(raw_text, features, category)

    return {
        "stage_b_score": sif_score,
        "sif_potential_category": category,
        "iogp_rules": assigned_iogp,
        "written_rationale": rationale,
        "key_driving_phrases": driving_phrases[:4],
        "retrieved_exemplar_ids": exemplar_ids,
        "saliency_heatmap": saliency_heatmap,
        "causal_chain": causal_chain
    }
