"""
Layer 3: Advanced Feature Extraction & Physical Quantity Extractor
Extracts structured JSON fields from incident reports:
- hazard_type
- energy_source
- equipment_involved
- barrier_status
- work_activity
- personnel_exposure
- physical_quantities (psi, bar, kg, meters, ppm H2S, % LEL, Volts, Amps)
"""

import re
import os
import json
from typing import Dict, Any, List

# Domain hazard taxonomy and energy signatures
HAZARD_SIGNATURES = [
    {
        "hazard_type": "Dropped Object / Suspended Load",
        "energy_source": "Gravitational Potential Energy (Heavy suspended mass)",
        "equipment": ["Travelling Block", "Crown Block", "Kelly Bushing", "Casing Hoist", "Crane", "Winch Sling", "Elevator", "Rotary Hook"],
        "keywords": ["dropped", "falling", "suspended load", "sling slip", "winch", "crane line", "dola", "rashi", "overhead", "hoist", "unsecured", "dropped object"]
    },
    {
        "hazard_type": "Pressurized Fluid / Gas Release",
        "energy_source": "High Hydraulic / Pneumatic Pressure (>1000 psi)",
        "equipment": ["Kelly Hose", "Standpipe Manifold", "Choke Line", "Mud Pump Discharge", "Hammer Union", "Flange", "Whipcheck", "BOP Accumulator"],
        "keywords": ["pressure", "burst", "rupture", "whipcheck", "kelly hose", "blew out", "leak", "high pressure", "manifold", "flange pin", "3200 psi", "kick", "blowout", "bop"]
    },
    {
        "hazard_type": "Toxic / Hazardous Gas Atmosphere",
        "energy_source": "Chemical / Asphyxiant Energy (H2S / Methane / O2 Deficiency)",
        "equipment": ["Mud Tank", "Cellar Pit", "Crude Storage Sump", "Separator Vessel", "Gas Detector", "SCBA", "EEBD", "Explosimeter"],
        "keywords": ["h2s", "gas leak", "confined space", "cellar pit", "mud pit", "asphyxiation", "breathing", "toxic", "lel", "chatai", "hawa", "sour gas", "sulfide", "ppm"]
    },
    {
        "hazard_type": "Line of Fire / Moving Machinery",
        "energy_source": "Rotational / Kinetic Mechanical Energy",
        "equipment": ["Rotary Table", "Iron Roughneck", "Cathead", "Drill Pipe Tongs", "Top Drive", "Agitator", "Mud Agitator"],
        "keywords": ["line of fire", "rotary table", "cathead", "tongs", "pinch point", "entanglement", "caught in", "fasi", "fas gaya", "nip point", "spinning chain"]
    },
    {
        "hazard_type": "Fall from Height",
        "energy_source": "Gravitational Potential Energy (Personnel >1.8m elevation)",
        "equipment": ["Monkey Board", "Derrick Ladder", "Rig Mast", "Pipe Rack Catwalk", "Scaffolding", "Safety Harness", "Self-Retracting Lifeline"],
        "keywords": ["height", "fall", "monkey board", "derrick", "scaffold", "ladder", "harness unclipped", "fall arrest", "dola", "machan", "catwalk", "unlatched"]
    },
    {
        "hazard_type": "Hot Work / Flammable Atmosphere Ignition",
        "energy_source": "Thermal / Pyrophoric Energy (Ignition in hazardous Zone)",
        "equipment": ["Welding Torch", "Angle Grinder", "Cutting Rig", "Separator Drum", "Flare Line", "Storage Tank Vent"],
        "keywords": ["hot work", "welding", "grinding", "spark", "flame", "fire blanket", "ignition", "flash fire", "burning", "pyrophoric", "flammable"]
    },
    {
        "hazard_type": "Uncontrolled Electrical Arc / Energized System",
        "energy_source": "High Voltage Electrical Energy (440V / 11kV)",
        "equipment": ["MCC Panel", "ESP Switchgear", "Generator Cable", "Transformer", "Breaker", "Substation Busbar"],
        "keywords": ["electrical", "live wire", "switchgear", "shock", "loto", "energized", "breaker", "arc flash", "cable damage", "440v", "11kv", "busbar"]
    },
    {
        "hazard_type": "Heavy Transport / Oilfield Vehicle Incident",
        "energy_source": "Kinetic Energy of Heavy Vehicles",
        "equipment": ["Crude Oil Bowser", "Pipe Trailer", "Frac Truck", "Crane Carrier", "Rig Pickup", "Winch Tractor"],
        "keywords": ["bowser", "vehicle", "truck", "skid", "rollover", "collision", "brake failure", "speeding", "gari", "gaari", "trailer"]
    }
]

BARRIER_STATUS_RULES = [
    {
        "status": "Failed",
        "indicators": ["broke", "snapped", "ruptured", "failed", "slipped off", "burst", "sheared", "parted", "gave way", "malfunctioned", "sheared pin", "corroded bolt"]
    },
    {
        "status": "Bypassed / Defeated",
        "indicators": ["bypassed", "jumpered", "disabled", "defeated", "overridden", "removed guard", "unhooked", "unclipped", "no permit", "unauthorized", "jugaad", "unlocked breaker"]
    },
    {
        "status": "Missing / None",
        "indicators": ["no barrier", "missing", "absent", "without whipcheck", "without harness", "without ptw", "without gas test", "no tagline", "without scba"]
    },
    {
        "status": "Degraded",
        "indicators": ["corroded", "worn out", "damaged sling", "frayed wire", "partial isolation", "loose clamp", "intermittent alarm", "frayed"]
    },
    {
        "status": "Intact / Effective",
        "indicators": ["held safely", "barrier prevented", "arrested fall", "tripped cleanly", "contained by", "whipcheck caught", "relief valve popped", "ppe prevented"]
    }
]

def extract_physical_quantities(text: str) -> List[Dict[str, Any]]:
    """
    Parses exact numerical metrics and engineering units from text:
    - Pressure: psi, bar, kPa
    - Mass/Weight: kg, ton, lbs
    - Distance/Elevation: meters, m, ft, feet, cm, inches
    - Toxic Gas: ppm H2S, % LEL, % O2
    - Electrical: V, Volts, kV, Amps
    - Speed: km/h, mph
    """
    quantities = []
    
    patterns = [
        (r"(\d+(?:\.\d+)?)\s*(?:psi|PSI)\b", "Pressure", "psi"),
        (r"(\d+(?:\.\d+)?)\s*(?:bar|BAR)\b", "Pressure", "bar"),
        (r"(\d+(?:\.\d+)?)\s*(?:kg|KG|kilograms?)\b", "Mass / Weight", "kg"),
        (r"(\d+(?:\.\d+)?)\s*(?:tons?|tonne?s?)\b", "Mass / Weight", "ton"),
        (r"(\d+(?:\.\d+)?)\s*(?:lbs?|pounds?)\b", "Mass / Weight", "lbs"),
        (r"(\d+(?:\.\d+)?)\s*(?:meters?|metres?|m)\b(?!\w)", "Elevation / Distance", "m"),
        (r"(\d+(?:\.\d+)?)\s*(?:feet|ft)\b", "Elevation / Distance", "ft"),
        (r"(\d+(?:\.\d+)?)\s*(?:inches?|in)\b", "Distance", "in"),
        (r"(\d+(?:\.\d+)?)\s*(?:cm)\b", "Distance", "cm"),
        (r"(\d+(?:\.\d+)?)\s*(?:ppm|PPM)\b", "Gas Concentration", "ppm"),
        (r"(\d+(?:\.\d+)?)\s*%\s*(?:LEL|lel)\b", "Flammability", "% LEL"),
        (r"(\d+(?:\.\d+)?)\s*%\s*(?:O2|oxygen)\b", "Oxygen Level", "% O2"),
        (r"(\d+(?:\.\d+)?)\s*(?:v|V|volts?|Volts?|kV|KV)\b", "Electrical Voltage", "V"),
        (r"(\d+(?:\.\d+)?)\s*(?:km/h|kmph|mph)\b", "Speed / Velocity", "km/h")
    ]
    
    for pat, category, std_unit in patterns:
        for m in re.finditer(pat, text):
            val_str = m.group(1)
            raw_str = m.group(0)
            try:
                val = float(val_str)
                quantities.append({
                    "value": val,
                    "unit": std_unit,
                    "category": category,
                    "raw_string": raw_str
                })
            except ValueError:
                pass
                
    return quantities

def extract_structured_features(text: str, detected_lexicon: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Extracts structured hazard type, energy source, equipment, barrier status,
    and physical engineering quantities from incident text.
    """
    lower_text = text.lower()
    
    # 1. Match Hazard & Energy Signature
    matched_hazard = None
    best_score = 0
    
    for sig in HAZARD_SIGNATURES:
        score = sum(1 for kw in sig["keywords"] if kw in lower_text)
        if score > best_score:
            best_score = score
            matched_hazard = sig
            
    if not matched_hazard or best_score == 0:
        hazard_type = "Routine Operational Hazard"
        energy_source = "Low / Controlled Energy"
        equipment_candidates = ["Standard Hand Tools / General Rig Equipment"]
    else:
        hazard_type = matched_hazard["hazard_type"]
        energy_source = matched_hazard["energy_source"]
        equipment_candidates = matched_hazard["equipment"]

    # 2. Extract Equipment Involved
    found_equip = []
    for eq in equipment_candidates:
        if eq.lower() in lower_text or any(w.lower() in lower_text for w in eq.split()):
            found_equip.append(eq)
    
    # Check lexicon for equipment
    if detected_lexicon:
        for lex in detected_lexicon:
            if lex.get("category") in ["critical_equipment", "pressure_barrier", "lifting_barrier", "electrical_equipment"]:
                found_equip.append(lex["term"])
                
    equipment_involved = ", ".join(list(dict.fromkeys(found_equip))) if found_equip else equipment_candidates[0]

    # 3. Determine Barrier Status
    detected_barrier_status = "Intact / Controlled"
    for rule in BARRIER_STATUS_RULES:
        if any(ind in lower_text for ind in rule["indicators"]):
            detected_barrier_status = rule["status"]
            break

    # 4. Determine Personnel Exposure & Line of Fire
    if any(k in lower_text for k in ["under", "line of fire", "struck", "stepped away", "bach goli", "bach gaya", "inches from", "hit helmet", "narrowly"]):
        personnel_exposure = "Immediate Zone of Potential Impact (Line of Fire)"
    elif any(k in lower_text for k in ["inside pit", "entered tank", "cellar pit", "confined space"]):
        personnel_exposure = "Enclosed in Hazardous Atmosphere"
    else:
        personnel_exposure = "Standard Operational Perimeter"

    # 5. Extract Activity
    activity = "Rig Operations / General Field Maintenance"
    if "tripping" in lower_text:
        activity = "Tripping Drill Pipe"
    elif "lifting" in lower_text or "crane" in lower_text or "hoist" in lower_text:
        activity = "Mechanical Heavy Lifting & Hoisting"
    elif "welding" in lower_text or "grinding" in lower_text or "cutting" in lower_text:
        activity = "Hot Work Fabrication"
    elif "tank" in lower_text or "pit" in lower_text or "confined space" in lower_text:
        activity = "Confined Space & Sump/Pit Entry"
    elif "transport" in lower_text or "driving" in lower_text or "bowser" in lower_text:
        activity = "Heavy Vehicle Transport"
    elif "electrical" in lower_text or "panel" in lower_text or "mcc" in lower_text:
        activity = "Electrical Substation & Switchgear Ops"
    elif "manifold" in lower_text or "pump" in lower_text or "pressure" in lower_text:
        activity = "High-Pressure Mud Manifold Ops"
    elif "monkey board" in lower_text or "derrick" in lower_text:
        activity = "Derrick & Monkey Board Operations"

    # 6. Physical Quantities Extraction
    phys_quantities = extract_physical_quantities(text)

    return {
        "hazard_type": hazard_type,
        "energy_source": energy_source,
        "equipment_involved": equipment_involved,
        "barrier_status": detected_barrier_status,
        "work_activity": activity,
        "personnel_exposure": personnel_exposure,
        "physical_quantities": phys_quantities
    }
