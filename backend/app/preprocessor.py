"""
Layer 2: Preprocessing & Domain Lexicon Normalization
Handles:
1. Domain Lexicon Expansion (Oil & Gas upstream acronyms: LOTO, BOP, PTW, JSA, SCBA, etc.)
2. Assam Oilfield Code-Switching (Assamese/Hindi dialect field terminology commonly used in Duliajan, Moran, Digboi)
3. OCR Status Flagging (Clean text intake with explicit production OCR roadmap flag)
"""

import re
from typing import Dict, Any, List, Tuple

# Domain Lexicon: Acronyms & Jargon mapping to normalized expansions & hazard context
DOMAIN_LEXICON: Dict[str, Dict[str, str]] = {
    "LOTO": {"expansion": "Lockout/Tagout (Energy Isolation)", "category": "barrier"},
    "BOP": {"expansion": "Blowout Preventer (Well Control Barrier)", "category": "critical_equipment"},
    "PTW": {"expansion": "Permit to Work (Work Authorisation)", "category": "administrative_barrier"},
    "JSA": {"expansion": "Job Safety Analysis", "category": "administrative_barrier"},
    "JHA": {"expansion": "Job Hazard Analysis", "category": "administrative_barrier"},
    "TBT": {"expansion": "Toolbox Talk (Pre-job briefing)", "category": "administrative_barrier"},
    "SCBA": {"expansion": "Self-Contained Breathing Apparatus", "category": "life_support_barrier"},
    "EEBD": {"expansion": "Emergency Escape Breathing Device", "category": "life_support_barrier"},
    "LEL": {"expansion": "Lower Explosive Limit (Flammable Gas)", "category": "gas_monitoring"},
    "SWL": {"expansion": "Safe Working Load (Rigging limit)", "category": "lifting_barrier"},
    "PRV": {"expansion": "Pressure Relief Valve", "category": "pressure_barrier"},
    "ESD": {"expansion": "Emergency Shutdown System", "category": "automated_barrier"},
    "PPE": {"expansion": "Personal Protective Equipment", "category": "secondary_barrier"},
    "H2S": {"expansion": "Hydrogen Sulfide (Lethal Toxic Gas)", "category": "chemical_energy"},
    "OISD": {"expansion": "Oil Industry Safety Directorate", "category": "regulatory_standard"},
    "DGMS": {"expansion": "Directorate General of Mines Safety", "category": "regulatory_standard"},
    "ESP": {"expansion": "Electric Submersible Pump", "category": "electrical_equipment"},
    "DBB": {"expansion": "Double Block and Bleed Isolation", "category": "isolation_barrier"},
    "IVMS": {"expansion": "In-Vehicle Monitoring System", "category": "driving_control"},
    "WHIPCHECK": {"expansion": "High-Pressure Hose Safety Cable", "category": "line_of_fire_barrier"},
    "MUD MOTOR": {"expansion": "Downhole Mud Motor Drilling Assembly", "category": "drilling_tool"},
    "KELLY": {"expansion": "Kelly Drive Bushing / Kelly Hose", "category": "high_pressure_rotary"},
    "CATHEAD": {"expansion": "Rig Cathead Winch", "category": "rotary_hazard"},
    "MONKEY BOARD": {"expansion": "Derrick Working Platform at 25-30m height", "category": "working_at_height"}
}

# Assamese & Hindi Code-Switching Glossary frequently used in Upper Assam OIL operations
CODE_SWITCH_GLOSSARY: Dict[str, Dict[str, str]] = {
    # Roles & Personnel
    "khalasi": {"english": "rig floor helper / roustabout", "lang": "Assamese/Hindi"},
    "khalaasi": {"english": "rig floor helper / roustabout", "lang": "Assamese/Hindi"},
    "thekedaar": {"english": "contractor labor", "lang": "Hindi/Assamese"},
    "thekedar": {"english": "contractor labor", "lang": "Hindi/Assamese"},
    "toli": {"english": "work crew / gang", "lang": "Hindi/Assamese"},
    "sentry": {"english": "standby watchman", "lang": "Assamese/Hindi"},
    
    # Locations & Rig components
    "dola": {"english": "suspended derrick monkey board / elevated platform", "lang": "Assamese"},
    "chatai": {"english": "cellar pit / sub-surface well trench", "lang": "Assamese"},
    "gorto": {"english": "open excavation / pit", "lang": "Assamese"},
    "gadda": {"english": "pit / sump", "lang": "Hindi"},
    "machan": {"english": "temporary wooden / bamboo scaffolding platform", "lang": "Assamese/Hindi"},
    
    # Equipment & Rigging
    "rashi": {"english": "winch wire rope / lifting cable", "lang": "Assamese"},
    "roshi": {"english": "wire rope / cable", "lang": "Assamese"},
    "taar": {"english": "metal wire / cable", "lang": "Hindi/Assamese"},
    "dori": {"english": "fiber rope / tagline", "lang": "Hindi"},
    "gari": {"english": "transport vehicle / crude bowser truck", "lang": "Assamese/Hindi"},
    "gaari": {"english": "transport vehicle / crude bowser truck", "lang": "Assamese/Hindi"},
    
    # Action & Outcome Indicators (Weak-signal near misses)
    "bach goli": {"english": "narrowly escaped injury (near-miss indicator)", "lang": "Assamese"},
    "bach gaya": {"english": "narrowly escaped injury (near-miss indicator)", "lang": "Hindi"},
    "fasi": {"english": "jammed / pinned in pinch point", "lang": "Assamese/Hindi"},
    "fas gaya": {"english": "trapped in line of fire", "lang": "Hindi"},
    "fasi goli": {"english": "got trapped / stuck in machinery", "lang": "Assamese"},
    "ghasita": {"english": "dragged by moving line", "lang": "Hindi"},
    "chot": {"english": "physical injury", "lang": "Hindi/Assamese"},
    "ghatna": {"english": "incident / occurrence", "lang": "Hindi/Assamese"},
    "durghatna": {"english": "accident", "lang": "Hindi/Assamese"},
    "bipod": {"english": "grave danger / hazard", "lang": "Assamese"},
    "khatra": {"english": "hazard / severe danger", "lang": "Hindi"},
    "dangoriya": {"english": "high risk / alarming condition", "lang": "Assamese"},
    "joldhi": {"english": "rushing / hasty bypass of safety steps", "lang": "Assamese"},
    "jaldi": {"english": "rushing / in a hurry without authorization", "lang": "Hindi"},
    
    # Fluids & Atmospheric
    "hawa": {"english": "gas venting / atmospheric vapor", "lang": "Hindi/Assamese"},
    "tel": {"english": "crude oil", "lang": "Hindi/Assamese"},
    "pani": {"english": "drilling fluid wash / water", "lang": "Hindi/Assamese"},

    # ─── Kannada Code-Switching (Used in Karnataka O&G / ONGC Hazira / Refinery workers) ───
    "hegide": {"english": "how is it / how was it done", "lang": "Kannada"},
    "aalasya": {"english": "laziness / skipped safety step", "lang": "Kannada"},
    "aparadha": {"english": "violation / fault / negligence", "lang": "Kannada"},
    "upaya": {"english": "workaround / jugaad bypass", "lang": "Kannada"},
    "ashta": {"english": "eight / shift number (common in Kannada rig log)", "lang": "Kannada"},
    "samaya": {"english": "time / shift timing", "lang": "Kannada"},
    "bittu": {"english": "left behind / abandoned equipment", "lang": "Kannada"},
    "bidditu": {"english": "it fell down / object dropped", "lang": "Kannada"},
    "gottilla": {"english": "did not know / unaware of hazard", "lang": "Kannada"},
    "aaythu": {"english": "it happened / incident occurred", "lang": "Kannada"},
    "hodi": {"english": "hit / struck", "lang": "Kannada"},
    "hoditu": {"english": "it struck / it hit someone", "lang": "Kannada"},
    "kela": {"english": "below / underneath the platform", "lang": "Kannada"},
    "mele": {"english": "above / at height / on top", "lang": "Kannada"},
    "bayalli": {"english": "outside / in the open area", "lang": "Kannada"},
    "olage": {"english": "inside / confined space entry", "lang": "Kannada"},
    "tappa": {"english": "escaped / narrowly avoided injury", "lang": "Kannada"},
    "tappisikondaru": {"english": "narrowly escaped / near miss indicator", "lang": "Kannada"},
    "beeki": {"english": "fire / open flame", "lang": "Kannada"},
    "usiru": {"english": "breath / oxygen / atmosphere check", "lang": "Kannada"},
    "odedaru": {"english": "broke / ruptured / snapped", "lang": "Kannada"},
    "sigutilla": {"english": "permit not obtained / missing authorization", "lang": "Kannada"},
    "sigalilla": {"english": "not received / not given (PTW not issued)", "lang": "Kannada"},
    "yentu": {"english": "what happened / incident description start", "lang": "Kannada"},

    # ─── Extended Assamese Regional Terms ───
    "hobo pare": {"english": "could have happened / near miss warning", "lang": "Assamese"},
    "khub khatra": {"english": "very high danger / extreme hazard", "lang": "Assamese"},
    "kela mara": {"english": "fell down / dropped object", "lang": "Assamese"},
    "pora gol": {"english": "fell into / person entered pit", "lang": "Assamese"},
    "ulai gol": {"english": "overflowed / spilled over", "lang": "Assamese"},
    "mati khahi": {"english": "ground gave way / soil collapse", "lang": "Assamese"},
    "gol gol": {"english": "rotating part / rotating equipment entanglement", "lang": "Assamese"},
    "jalinu": {"english": "burning / on fire", "lang": "Assamese"},
    "dhuan": {"english": "smoke / gas cloud visible", "lang": "Assamese/Hindi"}
}

class PreprocessingResult:
    def __init__(
        self,
        raw_text: str,
        cleaned_text: str,
        normalized_text: str,
        detected_lexicon: List[Dict[str, str]],
        detected_codeswitch: List[Dict[str, str]],
        ocr_metadata: Dict[str, Any]
    ):
        self.raw_text = raw_text
        self.cleaned_text = cleaned_text
        self.normalized_text = normalized_text
        self.detected_lexicon = detected_lexicon
        self.detected_codeswitch = detected_codeswitch
        self.ocr_metadata = ocr_metadata

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_text": self.raw_text,
            "cleaned_text": self.cleaned_text,
            "normalized_text": self.normalized_text,
            "detected_lexicon": self.detected_lexicon,
            "detected_codeswitch": self.detected_codeswitch,
            "ocr_metadata": self.ocr_metadata
        }

def clean_and_normalize_text(raw_text: str) -> PreprocessingResult:
    """
    Cleans raw incident report, normalizes oilfield acronyms,
    detects Assamese/Hindi code-switching, and applies standard domain context.
    """
    if not raw_text:
        raw_text = ""

    # 1. Basic sanitization: normalize whitespace and remove weird artifacts
    cleaned = re.sub(r'[\r\t]+', ' ', raw_text)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()

    # 2. Detect Domain Lexicon Acronyms
    detected_lexicon = []
    for term, info in DOMAIN_LEXICON.items():
        pattern = r'\b' + re.escape(term) + r'\b'
        if re.search(pattern, cleaned, flags=re.IGNORECASE):
            detected_lexicon.append({
                "term": term,
                "expansion": info["expansion"],
                "category": info["category"]
            })

    # 3. Detect & Translate Assamese/Hindi Code-Switching
    detected_codeswitch = []
    normalized = cleaned
    
    # Sort terms by length descending so longer multi-word phrases get replaced first
    sorted_codeswitch = sorted(CODE_SWITCH_GLOSSARY.items(), key=lambda x: len(x[0]), reverse=True)
    
    for foreign_term, meta in sorted_codeswitch:
        pattern = r'\b' + re.escape(foreign_term) + r'\b'
        matches = list(re.finditer(pattern, normalized, flags=re.IGNORECASE))
        if matches:
            detected_codeswitch.append({
                "original_phrase": foreign_term,
                "normalized_meaning": meta["english"],
                "language_origin": meta["lang"],
                "count": len(matches)
            })
            # Subtly enrich the normalized text with clarifying context in brackets
            # e.g. "khalasi bach goli" -> "khalasi [rig helper] bach goli [narrowly escaped near-miss]"
            def repl(m):
                orig = m.group(0)
                return f"{orig} [{meta['english']}]"
            normalized = re.sub(pattern, repl, normalized, flags=re.IGNORECASE)

    # 4. OCR Metadata (Section 6 compliant: explicitly flagged as clean text prototype)
    ocr_metadata = {
        "ocr_applied": False,
        "source_format": "clean_digital_text",
        "ocr_engine": "Tesseract-Ready (Flagged Roadmap Component)",
        "note": "Production OCR for handwritten field report forms is flagged as next step; prototype consumes digital text directly."
    }

    return PreprocessingResult(
        raw_text=raw_text,
        cleaned_text=cleaned,
        normalized_text=normalized,
        detected_lexicon=detected_lexicon,
        detected_codeswitch=detected_codeswitch,
        ocr_metadata=ocr_metadata
    )
