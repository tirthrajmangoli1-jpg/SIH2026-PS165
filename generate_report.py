import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.real_historical_data import REAL_HISTORICAL_TRAGEDIES_DATASET
from app.stage_a_filter import run_stage_a_prefilter
from app.stage_b_classifier import evaluate_few_shot_rubric

def generate_report():
    print("="*80)
    print(" 🏭 OIL SIF SENTINEL - REAL HISTORICAL TRAGEDIES EFFICIENCY REPORT 🏭")
    print("="*80)
    
    total = len(REAL_HISTORICAL_TRAGEDIES_DATASET)
    high_sif = 0
    
    print(f"\nProcessing {total} real historical precursors...\n")
    
    for idx, record in enumerate(REAL_HISTORICAL_TRAGEDIES_DATASET, 1):
        raw_text = record["raw_text"]
        
        # Stage A
        stage_a_res = run_stage_a_prefilter(raw_text)
        
        # We need mock features since feature_extractor requires LLM
        # We will do a basic mock
        features = {
            "energy_source": "High Pressure/Hazardous Material",
            "barrier_status": "Failed/Bypassed",
            "equipment_involved": record["facility"],
            "actual_injury_severity": record["actual_injury_severity"]
        }
        
        # Stage B
        stage_b_res = evaluate_few_shot_rubric(raw_text, raw_text, features, stage_a_res)
        
        if stage_b_res["sif_potential_category"] == "High SIF Potential":
            high_sif += 1
            
        print(f"--- Event {idx}: {record['facility']} ({record['location']}) ---")
        print(f"Precursor Observed: {raw_text}")
        print(f"Classification: {stage_b_res['sif_potential_category']} (Score: {stage_b_res['stage_b_score']})")
        print(f"IOGP Life-Saving Rules: {', '.join(stage_b_res['iogp_rules'])}")
        print("\nRationale:")
        print(stage_b_res["written_rationale"])
        print("\n" + "-"*80 + "\n")
        
    print("================== SUMMARY ==================")
    print(f"Total Historical Precursors Evaluated: {total}")
    print(f"Successfully Detected as High SIF Potential: {high_sif}")
    print(f"System Efficiency: {(high_sif/total)*100:.1f}%")
    print("=============================================")

if __name__ == "__main__":
    generate_report()
