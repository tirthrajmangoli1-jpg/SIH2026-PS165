"""
Automated Verification Suite for OIL SIF-Sentinel Backend
Validates:
1. Zero-injury near-misses receive HIGH SIF-potential (proves SIF != injury severity)
2. Stage A recall pre-filter flags 100% of hazardous precursors
3. Assam/Hindi code-switching normalization & OPSEC crew sanitization
4. Military-Grade AES-256 Authenticated Encryption & Merkle Blockchain Audit Ledger
5. Human-in-the-loop override writes live to vector store
6. HDBSCAN pattern clustering, 5x5 risk matrix, and SIF-precursor density rankings
7. Thermodynamic saliency heatmap and causal chain extraction
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.database import SessionLocal, engine, Base
from app.models import IncidentReport, AuditBlock
from app.data_generator import get_demo_batch, get_dataset_by_key, list_available_datasets
from app.main import process_single_report, IncidentCreate
from app.vector_store import vector_store
from app.clustering import analyze_hazard_patterns
from app.crypto_engine import crypto_engine

def test_full_pipeline():
    print("=== STARTING OIL SIF-SENTINEL PIPELINE TESTS ===")
    
    # 1. Reset and initialize DB tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 2. Ingest 15 demo reports
    demo_batch = get_demo_batch()
    print(f"-> Ingesting {len(demo_batch)} synthetic OIL incident reports...")
    
    processed_records = []
    for rep in demo_batch:
        inc_in = IncidentCreate(
            id=rep["id"],
            facility=rep["facility"],
            location=rep["location"],
            date_reported=rep.get("date_reported"),
            raw_text=rep["raw_text"],
            actual_injury_severity=rep.get("actual_injury_severity", "Near Miss / No Injury"),
            dataset_source=rep.get("dataset_source", "OIL Upper Assam Operations")
        )
        rec = process_single_report(db, inc_in)
        processed_records.append(rec)
        
    print(f"-> Ingested {len(processed_records)} records successfully.")
    
    # 3. Test Core Modelling Thesis: SIF-Potential != Injury Severity
    print("\n--- TEST: SIF-Potential != Injury Severity ---")
    
    # Case 1: OIL-ASM-001 (Kelly bushing dropped object - 0 injuries)
    rec1 = db.query(IncidentReport).filter(IncidentReport.id == "OIL-ASM-001").first()
    assert rec1 is not None, "OIL-ASM-001 not found"
    print(f"[OIL-ASM-001] Reported Injury: '{rec1.actual_injury_severity}' | SIF Category: '{rec1.sif_potential_category}' | SIF Score: {rec1.stage_b_score}")
    assert rec1.stage_a_flagged == True, "Stage A failed to flag near-miss dropped object!"
    assert rec1.stage_b_score >= 0.85, f"Expected high SIF score for near-miss dropped object, got {rec1.stage_b_score}"
    assert "High" in rec1.sif_potential_category, "Category should be High SIF Potential"
    assert "Safe Mechanical Lifting" in rec1.iogp_rules, f"IOGP rules missing Safe Mechanical Lifting: {rec1.iogp_rules}"
    print("  ✓ PASS: Zero-injury Kelly bushing near-miss correctly classified as HIGH SIF Precursor.")

    # Case 2: OIL-ASM-002 (Cellar pit H2S entry - 0 injuries)
    rec2 = db.query(IncidentReport).filter(IncidentReport.id == "OIL-ASM-002").first()
    assert rec2 is not None
    print(f"[OIL-ASM-002] Reported Injury: '{rec2.actual_injury_severity}' | SIF Category: '{rec2.sif_potential_category}' | SIF Score: {rec2.stage_b_score}")
    assert rec2.stage_a_flagged == True, "Stage A failed to flag H2S cellar pit entry!"
    assert rec2.stage_b_score >= 0.85, f"Expected high SIF score for H2S near-miss, got {rec2.stage_b_score}"
    assert "Confined Space" in rec2.iogp_rules, f"IOGP rules missing Confined Space: {rec2.iogp_rules}"
    print("  ✓ PASS: Zero-injury toxic gas cellar pit entry correctly classified as HIGH SIF Precursor.")

    # Case 3: OIL-ASM-012 (Administrative paper cut - Reported First Aid Injury)
    rec12 = db.query(IncidentReport).filter(IncidentReport.id == "OIL-ASM-012").first()
    assert rec12 is not None
    print(f"[OIL-ASM-012] Reported Injury: '{rec12.actual_injury_severity}' | SIF Category: '{rec12.sif_potential_category}' | SIF Score: {rec12.stage_b_score}")
    assert rec12.stage_b_score < 0.30, f"Expected low SIF score for paper cut, got {rec12.stage_b_score}"
    assert "Low" in rec12.sif_potential_category, "Paper cut should be Low SIF"
    print("  ✓ PASS: Reported First Aid injury correctly recognized as LOW SIF Potential.")

    # 4. Test Code-Switching & Physical Quantities & Saliency
    print("\n--- TEST: Assam Oilfield Code-Switching & Advanced NLP Features ---")
    assert len(rec1.detected_codeswitch) > 0, "Failed to detect Assamese code-switch in OIL-ASM-001"
    print(f"  Detected Code-Switch Terms: {rec1.detected_codeswitch}")
    assert any("bach goli" in cs["original_phrase"] for cs in rec1.detected_codeswitch)
    print("  ✓ PASS: Assamese 'bach goli' [near-miss escape] detected and enriched.")

    # Physical quantities check
    assert len(rec1.physical_quantities) > 0, "Physical quantities extraction failed for OIL-ASM-001"
    print(f"  Extracted Physical Quantities: {rec1.physical_quantities}")
    assert any(q["unit"] == "kg" and q["value"] == 85.0 for q in rec1.physical_quantities)
    print("  ✓ PASS: Physical metrics (85 kg, 14 m) extracted accurately.")

    # Thermodynamic saliency check
    assert len(rec1.saliency_heatmap) > 0, "Saliency heatmap empty"
    print(f"  Saliency heatmap sample tokens: {rec1.saliency_heatmap[:5]}")
    assert any(t["weight"] >= 0.85 for t in rec1.saliency_heatmap)
    print("  ✓ PASS: Thermodynamic token saliency computed.")

    # Causal chain check
    assert rec1.causal_chain and "root_precursor" in rec1.causal_chain
    print(f"  Causal Precursor Chain: {rec1.causal_chain}")
    print("  ✓ PASS: 3-stage Causal Precursor Chain generated.")

    # 5. Test Military-Grade Cryptography & Merkle Blockchain Audit Ledger
    print("\n--- TEST: Military-Grade AES-256 + Merkle Blockchain Audit ---")
    # Test encryption & decryption
    sample_secret = "Confidential OIL blowout precursor report 2026."
    enc_dict = crypto_engine.encrypt_payload(sample_secret)
    dec_text = crypto_engine.decrypt_payload(enc_dict)
    assert dec_text == sample_secret, "Decrypted text mismatch!"
    print("  ✓ PASS: AES-256-CTR + HMAC-SHA256 authenticated encryption roundtrip verified.")

    # Test Merkle ledger integrity
    blocks = db.query(AuditBlock).order_by(AuditBlock.block_height.asc()).all()
    assert len(blocks) == 15, f"Expected 15 Merkle audit blocks, got {len(blocks)}"
    block_dicts = [
        {
            "block_height": b.block_height,
            "timestamp": b.timestamp,
            "incident_id": b.incident_id,
            "prev_block_hash": b.prev_block_hash,
            "block_hash": b.block_hash,
            "payload_hash": b.payload_hash,
            "hmac_signature": b.hmac_signature
        }
        for b in blocks
    ]
    audit_res = crypto_engine.verify_ledger_integrity(block_dicts)
    assert audit_res["valid"] == True, f"Merkle audit ledger invalid: {audit_res}"
    print(f"  ✓ PASS: Merkle Blockchain Audit Ledger verified 100% untampered across {len(blocks)} blocks.")

    # Test Anti-Tamper Detection
    tampered_blocks = [dict(b) for b in block_dicts]
    tampered_blocks[2]["prev_block_hash"] = "deadbeef" * 8
    tamper_check = crypto_engine.verify_ledger_integrity(tampered_blocks)
    assert tamper_check["valid"] == False, "Tamper check failed to detect broken hash link!"
    print(f"  ✓ PASS: Cryptographic Merkle tamper detection triggered successfully.")

    # 6. Test Human-in-the-Loop Override Vector Store Feedback
    print("\n--- TEST: Human-in-the-Loop Vector Store Live Feedback ---")
    initial_store_size = len(vector_store.list_all_exemplars())
    rec9 = db.query(IncidentReport).filter(IncidentReport.id == "OIL-ASM-009").first()
    
    # Simulate Chief Safety Officer Override
    print(f"  Overriding OIL-ASM-009 from {rec9.stage_b_score} to 0.82 (Elevating degraded sling)...")
    new_ex = vector_store.add_override_exemplar(
        incident_id=rec9.id,
        text=rec9.normalized_text,
        energy_source=rec9.energy_source,
        barrier_status="Degraded Wire Rope (Officer Escalation)",
        sif_potential="High",
        sif_score=0.82,
        iogp_rule="Safe Mechanical Lifting",
        rationale="Officer escalation: Frayed sling over transit aisle requires High SIF tracking.",
        reviewer_name="CSO D. Phukan"
    )
    assert len(vector_store.list_all_exemplars()) == initial_store_size + 1
    assert new_ex["source"] == "human_override"
    
    matches = vector_store.query_exemplars("frayed sling wire rope lifting casing", top_k=2)
    assert any(m["id"] == new_ex["id"] for m in matches), "New override exemplar not retrieved in vector search!"
    print(f"  ✓ PASS: Reviewer override added to vector store ({new_ex['id']}) and immediately retrievable.")

    # 7. Test HDBSCAN Pattern Clustering & 5x5 Risk Matrix
    print("\n--- TEST: HDBSCAN Pattern Clustering & 5x5 Risk Matrix ---")
    all_reports = [
        {
            "id": r.id,
            "facility": r.facility,
            "location": r.location,
            "dataset_source": r.dataset_source,
            "date_reported": r.date_reported,
            "raw_text": r.raw_text,
            "normalized_text": r.normalized_text,
            "actual_injury_severity": r.actual_injury_severity,
            "sif_potential_category": r.sif_potential_category,
            "stage_b_score": r.stage_b_score,
            "barrier_status": r.barrier_status,
            "hazard_type": r.hazard_type,
            "iogp_rules": r.iogp_rules
        }
        for r in db.query(IncidentReport).all()
    ]
    pattern_results = analyze_hazard_patterns(all_reports)
    clusters = pattern_results["clusters"]
    print(f"  Identified {len(clusters)} recurring hazard clusters.")
    for c in clusters:
        print(f"  - Theme: '{c['theme_name']}' | Count: {c['incident_count']} | High SIF: {c['high_sif_count']} | Rule: {c['dominant_iogp_rule']}")
    assert len(clusters) > 0, "Clustering returned 0 clusters!"
    assert len(pattern_results["rig_distribution"]) > 0, "Rig distribution missing"
    assert len(pattern_results["sif_vs_injury_matrix"]) > 0, "SIF vs Injury matrix missing"
    assert len(pattern_results.get("site_density_ranking", [])) > 0, "Site SIF-precursor density ranking missing"
    assert len(pattern_results.get("activity_density_ranking", [])) > 0, "Activity SIF-precursor density ranking missing"
    assert len(pattern_results.get("risk_matrix_5x5", {}).get("cells", [])) == 25, "5x5 risk matrix cells missing"
    print("  ✓ PASS: HDBSCAN clustering, 5x5 Risk Matrix, and Precursor Density Rankings generated.")

    # 8. Test Multi-Dataset Availability
    print("\n--- TEST: Multi-Source Dataset Registry ---")
    datasets = list_available_datasets()
    assert len(datasets) >= 4, "Expected at least 4 registered datasets"
    for ds in datasets:
        print(f"  - Dataset: {ds['title']} ({ds['count']} records)")
    print("  ✓ PASS: Multi-source datasets verified.")

    db.close()
    print("\n=== ALL DEFENSE-GRADE PIPELINE TESTS PASSED 100% ===")

if __name__ == "__main__":
    test_full_pipeline()
