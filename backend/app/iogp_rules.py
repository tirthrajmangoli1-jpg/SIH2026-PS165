"""
IOGP Life-Saving Rules (Fixed Reference Corpus - 9 Rules)
International Association of Oil & Gas Producers (IOGP) Report 459 standard.
Used as the authoritative reference across Oil India Limited (OIL) operations.
"""

from typing import Dict, List, Any

IOGP_LIFE_SAVING_RULES: Dict[str, Dict[str, Any]] = {
    "Bypassing Safety Controls": {
        "id": "IOGP-01",
        "name": "Bypassing Safety Controls",
        "statement": "Obtain authorisation before overriding or disabling safety controls.",
        "icon": "shield-alert",
        "description": "Safety-critical equipment and interlocks, gas detectors, relief valves, ESDs, or BOP fail-safes must never be bypassed, inhibited, or defeated without a formal management-of-change and bypass permit.",
        "key_energy_sources": ["High pressure hydrocarbons", "Toxic gas (H2S)", "Mechanical fail-safes"],
        "typical_barriers": ["Interlocks", "ESD (Emergency Shutdown)", "Relief Valves", "PRV", "Bypass Permit (PTW)", "Gas Detection Alarm"],
        "keywords": [
            "bypass", "bypassed", "override", "overridden", "disable", "disabled", "defeat", "defeated",
            "jumper", "bridged", "inhibited", "interlock bypassed", "alarm muted", "esd bypassed",
            "safety device isolated", "sensor disconnected", "limit switch bypassed"
        ]
    },
    "Confined Space": {
        "id": "IOGP-02",
        "name": "Confined Space",
        "statement": "Obtain authorisation before entering a confined space.",
        "icon": "box",
        "description": "Entry into tanks, mud pits, vessels, crude storage sumps, or cellar pits is strictly prohibited without atmospheric testing, continuous ventilation, rescue plan, and a stand-by watchman.",
        "key_energy_sources": ["Atmospheric hazard (Oxygen deficiency, H2S, flammable vapors)", "Engulfment", "Mechanical agitation"],
        "typical_barriers": ["Gas Test Certificate", "Continuous Ventilation", "Standby Sentry / Attendant", "SCBA / EEBD", "Rescue Tripod & Harness", "Positive Isolation (Spade/Blind)"],
        "keywords": [
            "confined space", "mud pit", "crude tank", "cellar pit", "vessel entry", "separator drum",
            "sump pit", "h2s gas", "oxygen deficient", "asphyxiation", "standby person", "gas tester",
            "entry permit", "gas monitor", "breathe", "suffocate", "toxic atmosphere"
        ]
    },
    "Driving": {
        "id": "IOGP-03",
        "name": "Driving",
        "statement": "Follow safe driving rules.",
        "icon": "truck",
        "description": "Always wear seatbelts, adhere to speed limits, never use mobile phones while driving, assess road journey conditions in Assam oilfield terrain, and never drive while fatigued.",
        "key_energy_sources": ["Kinetic energy of heavy vehicles, crude bowsers, pipe carriers, crane trucks"],
        "typical_barriers": ["Seatbelt", "Speed Limiter / IVMS", "Journey Management Plan (JMP)", "Pre-trip Inspection", "Road Hazard Signage"],
        "keywords": [
            "driving", "vehicle", "bowser", "crude tanker", "truck", "pickup", "jeep", "trailer",
            "speeding", "seatbelt", "collision", "overturn", "rollover", "ivms", "oilfield road",
            "ditch", "skid", "brake failure", "driver fatigue"
        ]
    },
    "Energy Isolation": {
        "id": "IOGP-04",
        "name": "Energy Isolation",
        "statement": "Verify isolation and zero energy state before work begins.",
        "icon": "zap-off",
        "description": "Lockout / Tagout (LOTO), mechanical blinding/spading, and electrical isolation must be applied, verified, and zero energy confirmed before breaking containment or servicing energized systems.",
        "key_energy_sources": ["High pressure fluid/gas", "Electrical voltage (440V / 11kV)", "Stored mechanical energy (springs/counterweights)", "Residual hydrostatic head"],
        "typical_barriers": ["LOTO Padlock & Tag", "Double Block and Bleed (DBB)", "Spectacle Blind / Spade", "Voltage Detector / Test Before Touch", "Pressure Bleed Off"],
        "keywords": [
            "isolation", "loto", "lockout", "tagout", "energized", "live wire", "stored energy",
            "bleed off", "residual pressure", "blinding", "spading", "breaker", "switchgear",
            "zero energy", "electrical shock", "lock out", "tag out", "containment breach"
        ]
    },
    "Hot Work": {
        "id": "IOGP-05",
        "name": "Hot Work",
        "statement": "Clear flammable materials and control ignition sources before hot work.",
        "icon": "flame",
        "description": "Welding, torch cutting, or grinding within classified hazardous areas (Zone 0/1/2) requires explosive gas testing (LEL check), fire blankets, water hose charged, and an authorized Hot Work Permit.",
        "key_energy_sources": ["Thermal energy", "Sparks / Open flame", "Volatile hydrocarbons / Crude oil vapors / Methane"],
        "typical_barriers": ["Hot Work Permit (HWP)", "Explosimeter / LEL Gas Test", "Fire Watcher & Fire Extinguisher", "Pressurized Fire Blanket", "15-meter Buffer Cleared"],
        "keywords": [
            "hot work", "welding", "grinding", "torch cutting", "gas cutting", "spark", "open flame",
            "flammable gas", "lel", "explosive atmosphere", "fire watch", "fire blanket", "hydrocarbon leak",
            "manifold welding", "tank welding", "drill floor welding"
        ]
    },
    "Line of Fire": {
        "id": "IOGP-06",
        "name": "Line of Fire",
        "statement": "Keep yourself and others out of the line of fire.",
        "icon": "target",
        "description": "Positioning personnel away from moving machinery (rotary table, cathead, iron roughneck), high pressure releases (kelly hose, hammer union), pressurized discharge lines, or falling trajectories.",
        "key_energy_sources": ["Mechanical kinetic / rotational energy", "High pressure trajectory", "Strained cables / Whipping hoses"],
        "typical_barriers": ["Exclusion Zone", "Whipcheck / Safety Sling on Hoses", "Rotary Table Guard", "Spotter", "Physical Barricading"],
        "keywords": [
            "line of fire", "whipcheck", "whipping hose", "kelly hose", "iron roughneck", "rotary table",
            "cathead", "tongs", "struck by", "pinch point", "crushed by", "hydraulic hose rupture",
            "hammer union", "trajectory", "snapping cable", "winch line"
        ]
    },
    "Safe Mechanical Lifting": {
        "id": "IOGP-07",
        "name": "Safe Mechanical Lifting",
        "statement": "Plan lifting operations and control the area under suspended loads.",
        "icon": "anchor",
        "description": "Never walk, stand, or position oneself under a suspended load. Rigging gear must be certified, SWL verified, tagline used to guide loads, and crane exclusion zone barricaded.",
        "key_energy_sources": ["Gravitational potential energy of heavy drill pipe, casing, mud motor, BOP stack"],
        "typical_barriers": ["Lifting Plan", "Certified Slings & Shackles (SWL)", "Tagline", "Barricaded Drop Zone", "Crane Load Limiter", "Trained Rigger"],
        "keywords": [
            "lifting", "crane", "hoist", "suspended load", "sling", "shackle", "rigging", "tagline",
            "under load", "dropped load", "swl", "winch", "wire rope", "casing hoist", "drill collar lifting",
            "chain pulley", "boom crane"
        ]
    },
    "Work Authorisation": {
        "id": "IOGP-08",
        "name": "Work Authorisation",
        "statement": "Work with a valid permit when required.",
        "icon": "file-check",
        "description": "All non-routine, hazardous, or classified work requires a validated Permit to Work (PTW), a Job Safety Analysis (JSA), and a mandatory pre-job toolbox talk (TBT) before starting.",
        "key_energy_sources": ["Uncontrolled operational hazards across all energy classes"],
        "typical_barriers": ["Permit to Work (PTW)", "Job Safety Analysis (JSA)", "Toolbox Talk (TBT)", "Authorised Performing Authority (PA)", "Area Authority Endorsement"],
        "keywords": [
            "permit to work", "ptw", "work permit", "jsa", "job safety analysis", "toolbox talk", "tbt",
            "unauthorised work", "no permit", "unpermitted", "cold work permit", "hot work permit",
            "cross-shift handover", "job hazard analysis"
        ]
    },
    "Working at Height": {
        "id": "IOGP-09",
        "name": "Working at Height",
        "statement": "Protect yourself against a fall when working at height.",
        "icon": "arrow-up-right",
        "description": "Any work conducted >1.8 meters above ground (derrick monkey board, crown block, rig mast, pipe rack catwalk, scaffold) requires 100% tie-off safety harness, inertia reel, or rigid guardrails.",
        "key_energy_sources": ["Gravitational potential energy of personnel (>1.8m)"],
        "typical_barriers": ["Full Body Harness with Shock Absorber", "100% Dual Lanyard Tie-off", "Inertia Reel / Fall Arrest Block", "Scaffold Tag (Green Tag)", "Certified Anchor Point (5000 lbs)"],
        "keywords": [
            "working at height", "fall from height", "height", "monkey board", "derrick", "crown block",
            "mast", "scaffolding", "safety harness", "lanyard", "tie off", "fall arrest", "inertia reel",
            "catwalk", "stairway fall", "rig floor edge"
        ]
    }
}

def get_iogp_rule_by_name(name: str) -> Dict[str, Any]:
    """Retrieve rule details by canonical name or partial match."""
    for rule_name, rule_data in IOGP_LIFE_SAVING_RULES.items():
        if rule_name.lower() == name.lower():
            return rule_data
    return {}

def list_all_iogp_rules() -> List[Dict[str, Any]]:
    """Return all 9 IOGP Life-Saving Rules."""
    return [
        {"name": name, **details}
        for name, details in IOGP_LIFE_SAVING_RULES.items()
    ]
