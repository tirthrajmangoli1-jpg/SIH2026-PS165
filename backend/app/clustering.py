"""
Layer 6: Pattern Analysis, Hazard Clustering & 5x5 Process-Safety Risk Matrix
Uses HDBSCAN and embedding representations across reports to surface:
- Recurring hazard themes
- Facility/Rig hotspot distributions
- 5x5 Process-Safety Risk Heatmap Matrix (Energy vs Barrier Vulnerability)
- Time trend analysis for Recharts
- Cross-tabulation of SIF Potential vs Actual Injury Severity
- SIF Precursor Density rankings for Sites & Activities with HSE Interventions
"""

from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import hdbscan

THEME_TEMPLATES = [
    {
        "pattern": ["dropped", "lifting", "suspended", "sling", "hoist", "crane", "bushing", "cylinder"],
        "name": "Hoisting Gear & Dropped Object Recurrence",
        "rule": "Safe Mechanical Lifting"
    },
    {
        "pattern": ["pressure", "psi", "whipcheck", "kelly hose", "burst", "manifold", "choke", "kick", "blowout", "bop"],
        "name": "Pressurized Mud Line & Secondary Restraint Failure",
        "rule": "Line of Fire"
    },
    {
        "pattern": ["h2s", "confined", "pit", "tank", "gas", "chatai", "asphyxiation", "manway"],
        "name": "Cellar Pit & Confined Space Toxic Gas Incursions",
        "rule": "Confined Space"
    },
    {
        "pattern": ["loto", "electrical", "440v", "breaker", "switchgear", "live wire", "arc flash", "busbar"],
        "name": "Electrical LOTO & Energized Equipment Isolation",
        "rule": "Energy Isolation"
    },
    {
        "pattern": ["rotary", "cathead", "tongs", "fasi", "fas gaya", "nip point", "iron roughneck", "spinning chain"],
        "name": "Drill Floor Rotating Machinery Line of Fire",
        "rule": "Line of Fire"
    },
    {
        "pattern": ["monkey board", "height", "derrick", "fall", "harness", "scaffold", "ladder", "tie-off"],
        "name": "Derrick Working at Height & Fall Arrest Deficiencies",
        "rule": "Working at Height"
    },
    {
        "pattern": ["welding", "hot work", "grinding", "spark", "flame", "pyrophoric", "flare"],
        "name": "Hot Work & Explosive Vapor Flash Hazards",
        "rule": "Hot Work"
    },
    {
        "pattern": ["bowser", "vehicle", "truck", "skid", "rollover", "transport"],
        "name": "Heavy Oilfield Logistics & Fleet Transport Risk",
        "rule": "Driving"
    },
    {
        "pattern": ["office", "paper", "trip", "minor", "cut", "bruise", "tea", "mouse", "catering"],
        "name": "Routine Non-Industrial Slips & Minor First Aid",
        "rule": "Work Authorisation"
    }
]

def compute_5x5_risk_matrix(reports: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes a 5x5 Process-Safety Risk Heatmap Matrix:
    X-axis: Barrier Integrity (Missing, Failed, Bypassed, Degraded, Intact)
    Y-axis: Energy Level (Catastrophic Industrial, High Potential, Moderate, Low, Minimal)
    """
    energy_levels = [
        "Catastrophic (>3000 psi / Heavy Dropped / H2S)",
        "High Energy (440V / 1000-3000 psi / Monkey Board)",
        "Moderate Energy (Moving Parts / Pressurized Utility)",
        "Low Energy (Hand Tools / Low Elevation)",
        "Minimal (Administrative / Non-Industrial)"
    ]
    
    barrier_levels = [
        "Missing / None",
        "Failed / Parted",
        "Bypassed / Overridden",
        "Degraded / Worn",
        "Intact / Controlled"
    ]
    
    # Initialize 5x5 matrix
    matrix_cells = []
    for y_idx, energy in enumerate(energy_levels):
        for x_idx, barrier in enumerate(barrier_levels):
            # Theoretical severity / SIF potential
            risk_score = round((5 - y_idx) * (5 - x_idx) / 25.0, 2)
            matrix_cells.append({
                "y_index": y_idx,
                "x_index": x_idx,
                "energy_level": energy,
                "barrier_status": barrier,
                "theoretical_sif": risk_score,
                "incident_count": 0,
                "incident_ids": []
            })

    def map_report_to_cell(r: Dict[str, Any]) -> tuple:
        txt = (r.get("normalized_text", "") + " " + r.get("raw_text", "")).lower()
        b_status = r.get("barrier_status", "Intact / Controlled")
        sif_score = r.get("stage_b_score", 0.1)
        
        # Determine energy row (0 = Catastrophic, 4 = Minimal)
        if any(k in txt for k in ["3200 psi", "85 kg", "14 meters", "22 meters", "h2s hawa", "8,500 psi", "3000 psi", "3.2 ton", "4500 psi", "blowout"]):
            y_idx = 0
        elif any(k in txt for k in ["440v", "11kv", "monkey board", "28 meters", "vibrator hose", "bowser", "grinding", "top-drive", "compressor skid", "arc flash"]):
            y_idx = 1
        elif any(k in txt for k in ["rotary table", "tongs", "45 psi", "chemical injection", "spinning chain", "pipe trailer", "forklift"]):
            y_idx = 2
        elif any(k in txt for k in ["kerb", "concrete kerb", "minor trip", "stewards", "aluminum door", "frayed stitching"]):
            y_idx = 3
        else:
            y_idx = 4

        # Determine barrier column (0 = Missing, 4 = Intact)
        if "Missing" in b_status or "None" in b_status or "without" in txt:
            x_idx = 0
        elif "Failed" in b_status or "broke" in txt or "sheared" in txt or "ruptured" in txt:
            x_idx = 1
        elif "Bypassed" in b_status or "Defeated" in b_status or "jugaad" in txt or "unlocked" in txt:
            x_idx = 2
        elif "Degraded" in b_status or "frayed" in txt or "worn" in txt or "intermittent" in txt:
            x_idx = 3
        else:
            x_idx = 4
            
        return y_idx, x_idx

    for r in reports:
        y_idx, x_idx = map_report_to_cell(r)
        cell = next((c for c in matrix_cells if c["y_index"] == y_idx and c["x_index"] == x_idx), None)
        if cell:
            cell["incident_count"] += 1
            cell["incident_ids"].append(r.get("id"))

    return {
        "energy_levels": energy_levels,
        "barrier_levels": barrier_levels,
        "cells": matrix_cells
    }

def analyze_hazard_patterns(reports: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Performs HDBSCAN clustering and trend analysis across all processed reports.
    Returns structured dashboard payload for React + Recharts frontend.
    """
    if not reports:
        return {
            "clusters": [],
            "timeline_trends": [],
            "rig_distribution": [],
            "barrier_distribution": [],
            "sif_vs_injury_matrix": [],
            "site_density_ranking": [],
            "activity_density_ranking": [],
            "risk_matrix_5x5": {"energy_levels": [], "barrier_levels": [], "cells": []}
        }

    texts = [r.get("normalized_text", r.get("raw_text", "")) for r in reports]
    
    # 1. Vectorize text corpus
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=256, stop_words="english")
    try:
        X = vectorizer.fit_transform(texts).toarray()
    except Exception:
        X = np.eye(len(texts))

    # 2. HDBSCAN Clustering
    min_cluster_size = 2 if len(reports) >= 4 else 1
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=1,
        metric='euclidean',
        cluster_selection_epsilon=0.3
    )
    labels = clusterer.fit_predict(X)

    # 3. Aggregate Clusters
    cluster_groups: Dict[int, List[Dict[str, Any]]] = {}
    for idx, label in enumerate(labels):
        cluster_id = int(label)
        if cluster_id not in cluster_groups:
            cluster_groups[cluster_id] = []
        reports[idx]["cluster_id"] = cluster_id
        cluster_groups[cluster_id].append(reports[idx])

    cluster_summaries = []
    for c_id, group_reports in cluster_groups.items():
        combined_text = " ".join([r.get("normalized_text", "").lower() for r in group_reports])
        
        # Match best human-readable theme name
        matched_theme = "Rig Site Mechanical Precursor Pattern"
        matched_rule = "Safe Mechanical Lifting"
        best_match_count = -1
        
        for tpl in THEME_TEMPLATES:
            hits = sum(1 for kw in tpl["pattern"] if kw in combined_text)
            if hits > best_match_count:
                best_match_count = hits
                matched_theme = tpl["name"]
                matched_rule = tpl["rule"]

        high_sif_count = sum(1 for r in group_reports if r.get("sif_potential_category") == "High SIF Potential")
        facilities = list(set([r.get("facility", "Unknown") for r in group_reports]))
        locations = list(set([r.get("location", "Unknown") for r in group_reports]))
        incident_ids = [r.get("id") for r in group_reports]

        # Update each report's cluster theme
        for r in group_reports:
            r["cluster_theme"] = matched_theme

        cluster_summaries.append({
            "cluster_id": c_id,
            "theme_name": matched_theme,
            "incident_count": len(group_reports),
            "high_sif_count": high_sif_count,
            "dominant_iogp_rule": matched_rule,
            "facilities_impacted": facilities,
            "locations_impacted": locations,
            "sample_incident_ids": incident_ids[:3]
        })

    cluster_summaries.sort(key=lambda c: c["high_sif_count"], reverse=True)

    # 4. Compute Rig Distribution for Recharts
    rig_counts: Dict[str, Dict[str, int]] = {}
    for r in reports:
        fac = r.get("facility", "Other")
        if fac not in rig_counts:
            rig_counts[fac] = {"facility": fac, "high_sif": 0, "medium_sif": 0, "low_sif": 0, "total": 0}
        cat = r.get("sif_potential_category", "Low / Non-SIF")
        if "High" in cat:
            rig_counts[fac]["high_sif"] += 1
        elif "Medium" in cat:
            rig_counts[fac]["medium_sif"] += 1
        else:
            rig_counts[fac]["low_sif"] += 1
        rig_counts[fac]["total"] += 1
        if "incident_ids" not in rig_counts[fac]:
            rig_counts[fac]["incident_ids"] = []
        rig_counts[fac]["incident_ids"].append(r.get("id"))

    rig_distribution = list(rig_counts.values())
    rig_distribution.sort(key=lambda x: x["high_sif"], reverse=True)

    # 5. Compute Barrier Distribution for Recharts
    barrier_counts: Dict[str, int] = {}
    for r in reports:
        b_status = r.get("barrier_status", "Unknown")
        barrier_counts[b_status] = barrier_counts.get(b_status, 0) + 1
    barrier_distribution = [{"status": k, "count": v} for k, v in barrier_counts.items()]

    # 6. SIF Potential vs Actual Injury Severity Cross-Tabulation
    cross_tab = {
        "Near Miss / No Injury": {"High SIF": 0, "Medium SIF": 0, "Low SIF": 0},
        "First Aid": {"High SIF": 0, "Medium SIF": 0, "Low SIF": 0},
        "Medical Treatment Case": {"High SIF": 0, "Medium SIF": 0, "Low SIF": 0},
        "Lost Time Injury": {"High SIF": 0, "Medium SIF": 0, "Low SIF": 0},
        "Fatality": {"High SIF": 0, "Medium SIF": 0, "Low SIF": 0}
    }
    for r in reports:
        sev = r.get("actual_injury_severity", "Near Miss / No Injury")
        if sev not in cross_tab:
            sev = "Near Miss / No Injury"
        cat = r.get("sif_potential_category", "Low / Non-SIF")
        sif_col = "High SIF" if "High" in cat else ("Medium SIF" if "Medium" in cat else "Low SIF")
        cross_tab[sev][sif_col] += 1

    sif_vs_injury_matrix = [
        {"reported_severity": k, "high_sif": v["High SIF"], "medium_sif": v["Medium SIF"], "low_sif": v["Low SIF"]}
        for k, v in cross_tab.items()
    ]

    # 7. Timeline Trends
    timeline_dict: Dict[str, Dict[str, Any]] = {}
    for r in reports:
        date_str = r.get("date_reported", "2024-05")
        month = date_str[:7] if len(date_str) >= 7 else "2024-05"
        if month not in timeline_dict:
            timeline_dict[month] = {"month": month, "high_sif": 0, "medium_sif": 0, "low_sif": 0, "total": 0}
        cat = r.get("sif_potential_category", "Low / Non-SIF")
        if "High" in cat:
            timeline_dict[month]["high_sif"] += 1
        elif "Medium" in cat:
            timeline_dict[month]["medium_sif"] += 1
        else:
            timeline_dict[month]["low_sif"] += 1
        timeline_dict[month]["total"] += 1

    timeline_trends = sorted(list(timeline_dict.values()), key=lambda x: x["month"])

    # 8. Site SIF-Precursor Density Ranking
    site_density_ranking = []
    for fac, data in rig_counts.items():
        total = data["total"]
        high = data["high_sif"]
        density = round((high / total) * 100, 1) if total > 0 else 0.0
        
        fac_reports = [r for r in reports if r.get("facility") == fac]
        loc = fac_reports[0].get("location", "Upper Assam") if fac_reports else "Upper Assam"
        
        rules_list = []
        barriers_list = []
        for r in fac_reports:
            if r.get("iogp_rules"):
                rules_list.extend(r.get("iogp_rules", []))
            if r.get("barrier_status") and r.get("barrier_status") != "Unknown":
                barriers_list.append(r.get("barrier_status"))
                
        dominant_rule = max(set(rules_list), key=rules_list.count) if rules_list else "Work Authorisation"
        dominant_barrier = max(set(barriers_list), key=barriers_list.count) if barriers_list else "Degraded"
        
        if "Lifting" in dominant_rule:
            rec_action = "Mandate immediate stand-down & NDT inspection of all hoist slings, sheaves, and rig floor exclusion zones."
        elif "Line of Fire" in dominant_rule:
            rec_action = "Inspect high-pressure mud lines; replace missing whipchecks and verify snubbing cables across manifold."
        elif "Confined" in dominant_rule:
            rec_action = "Halt vessel entries; audit calibration of 4-gas detectors and enforce SCBA sign-off before manway access."
        elif "Height" in dominant_rule:
            rec_action = "Enforce 100% dual-lanyard harness tie-off and audit monkey board inertia reel anchors."
        elif "Energy Isolation" in dominant_rule:
            rec_action = "Conduct zero-energy LOTO audit on switchgear and electrical breakers before maintenance."
        elif "Hot Work" in dominant_rule:
            rec_action = "Enforce mandatory explosive gas LEL sniffer test and deploy continuous water deluge mist."
        else:
            rec_action = "Reinforce dynamic Job Safety Analysis (JSA) and operational Permit-to-Work (PTW) compliance."

        site_density_ranking.append({
            "facility": fac,
            "location": loc,
            "total_reports": total,
            "high_sif_count": high,
            "medium_sif_count": data["medium_sif"],
            "low_sif_count": data["low_sif"],
            "sif_density_pct": density,
            "dominant_iogp_rule": dominant_rule,
            "dominant_barrier_failure": dominant_barrier,
            "recommended_hse_action": rec_action,
            "sample_incident_ids": data.get("incident_ids", [])[:3]
        })
        
    site_density_ranking.sort(key=lambda x: (x["sif_density_pct"], x["high_sif_count"]), reverse=True)

    # 9. Operational Activity SIF-Precursor Density Ranking
    def infer_activity(r: Dict[str, Any]) -> str:
        ext = r.get("extracted_features") or {}
        if ext.get("work_activity") and ext["work_activity"] != "Rig Operations / General Field Maintenance":
            return ext["work_activity"]
        txt = (r.get("normalized_text", "") + " " + r.get("raw_text", "")).lower()
        if any(k in txt for k in ["kelly hose", "manifold", "pressure", "whipcheck", "standpipe", "3200 psi", "burst", "choke", "kick", "blowout", "bop"]):
            return "High-Pressure Mud Manifold Ops"
        elif any(k in txt for k in ["bushing", "sling", "crane", "hoist", "elevator", "dropped", "winch", "rig floor", "kelly", "top-drive"]):
            return "Mechanical Heavy Lifting & Hoisting"
        elif any(k in txt for k in ["cellar pit", "confined space", "h2s", "tank", "pit", "sludge", "entry", "manway", "asphyxiation"]):
            return "Confined Space & Sump/Pit Entry"
        elif any(k in txt for k in ["monkey board", "derrick", "height", "mast", "scaffold", "fall", "harness", "tie-off"]):
            return "Derrick & Monkey Board Operations"
        elif any(k in txt for k in ["tripping", "drill string", "drill pipe", "tongs", "slip", "cathead", "rotary table"]):
            return "Tubular Handling & Tripping Pipe"
        elif any(k in txt for k in ["electrical", "440v", "panel", "breaker", "switchgear", "cable", "shock", "arc flash", "11kv", "busbar"]):
            return "Electrical Switchgear Maintenance"
        elif any(k in txt for k in ["welding", "hot work", "cutting", "grinding", "torch", "spark", "pyrophoric"]):
            return "Hot Work & Welding Fabrication"
        elif any(k in txt for k in ["bowser", "vehicle", "truck", "skid", "road", "speed"]):
            return "Oilfield Heavy Vehicle Transport"
        return "Routine Field Maintenance"

    activity_counts: Dict[str, Dict[str, Any]] = {}
    for r in reports:
        act = infer_activity(r)
        if act not in activity_counts:
            activity_counts[act] = {
                "activity": act,
                "total_reports": 0,
                "high_sif_count": 0,
                "rules": [],
                "barriers": []
            }
        activity_counts[act]["total_reports"] += 1
        cat = r.get("sif_potential_category", "")
        if "High" in cat:
            activity_counts[act]["high_sif_count"] += 1
        if r.get("iogp_rules"):
            activity_counts[act]["rules"].extend(r.get("iogp_rules", []))
        if r.get("barrier_status") and r.get("barrier_status") != "Unknown":
            activity_counts[act]["barriers"].append(r.get("barrier_status"))

    activity_density_ranking = []
    for act, data in activity_counts.items():
        total = data["total_reports"]
        high = data["high_sif_count"]
        density = round((high / total) * 100, 1) if total > 0 else 0.0
        dominant_rule = max(set(data["rules"]), key=data["rules"].count) if data["rules"] else "Work Authorisation"
        dominant_barrier = max(set(data["barriers"]), key=data["barriers"].count) if data["barriers"] else "Degraded"

        if "Lifting" in dominant_rule:
            focus_rec = "Audit crane/hoist pre-use certifications; strictly enforce red-zone barricades under suspended loads."
        elif "Line of Fire" in dominant_rule:
            focus_rec = "Install certified whipcheck arrestors on all high-pressure hose connections; verify relief valve calibrations."
        elif "Confined" in dominant_rule:
            focus_rec = "Enforce continuous 4-gas atmosphere testing, forced ventilation, and dedicated standby observer with SCBA."
        elif "Height" in dominant_rule:
            focus_rec = "Mandate 100% dual-tie-off harness compliance with shock absorbers; inspect inertia reels daily."
        elif "Energy Isolation" in dominant_rule:
            focus_rec = "Enforce Zero-Energy Verification (test-before-touch) and personal padlock key custody on 440V switchgear."
        elif "Hot Work" in dominant_rule:
            focus_rec = "Verify 0.0% LEL gas sniffer test before spark generation; post dedicated fire watcher with pressurized extinguisher."
        else:
            focus_rec = "Conduct pre-task safety huddle and verify dynamic risk assessment with field supervisor."

        activity_density_ranking.append({
            "activity": act,
            "total_reports": total,
            "high_sif_count": high,
            "sif_density_pct": density,
            "dominant_iogp_rule": dominant_rule,
            "key_barrier_failure": dominant_barrier,
            "hse_focus_intervention": focus_rec
        })

    activity_density_ranking.sort(key=lambda x: (x["sif_density_pct"], x["high_sif_count"]), reverse=True)

    # 10. 5x5 Process Safety Risk Heatmap Matrix
    risk_matrix = compute_5x5_risk_matrix(reports)

    return {
        "clusters": cluster_summaries,
        "rig_distribution": rig_distribution,
        "barrier_distribution": barrier_distribution,
        "sif_vs_injury_matrix": sif_vs_injury_matrix,
        "timeline_trends": timeline_trends,
        "site_density_ranking": site_density_ranking,
        "activity_density_ranking": activity_density_ranking,
        "risk_matrix_5x5": risk_matrix
    }
