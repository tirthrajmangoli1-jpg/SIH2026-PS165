"""
OIL SIF-Sentinel Backend Application (FastAPI)
Smart India Hackathon: PS 165 - Fatality Precursor Surveillance System

Six-Layer Architecture + Defense-Grade Security & Advanced NLP:
1. Ingestion & Multi-Source Global Datasets (OIL Assam, BSEE Offshore, CSB Petrochemical, IOGP Global)
2. Preprocessing & OPSEC PII Sanitization (Assam Code-Switching + Salted Personnel Anonymization)
3. Feature Extraction & Physical Metric Parsing (psi, bar, kg, meters, ppm H2S, % LEL, Volts)
4. Classification Core (Stage A Recall Pre-Filter -> Stage B Few-Shot Precision + Saliency Heatmap + Causal Reasoning)
5. Human-in-the-Loop Active Learning (Overrides vector-indexed in real time)
6. Pattern Radar & 5x5 Process-Safety Risk Matrix (HDBSCAN Clustering + Density Rankings)
7. Sovereign Military-Grade Cryptography (AES-256 CTR + HMAC-SHA256 + Immutable Merkle Audit Ledger)
"""

import os
import random
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, get_db, Base
from .models import IncidentReport, ExemplarRecord, AuditBlock
from .schemas import (
    IncidentCreate, BatchIngestRequest, ReviewSubmission,
    IncidentResponse, ExemplarSchema, ClusterSummarySchema,
    SecurityAuditStatusSchema, MerkleAuditBlockSchema
)
from .iogp_rules import list_all_iogp_rules
from .preprocessor import clean_and_normalize_text
from .feature_extractor import extract_structured_features
from .stage_a_filter import run_stage_a_prefilter
from .stage_b_classifier import evaluate_few_shot_rubric
from .vector_store import vector_store
from .clustering import analyze_hazard_patterns
from .crypto_engine import crypto_engine
from .data_generator import (
    get_demo_batch, get_dataset_by_key, list_available_datasets
)
from .real_historical_data import REAL_HISTORICAL_TRAGEDIES_DATASET
from .kaggle_dataset import KAGGLE_STEFANINI_DATASET

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OIL SIF-Sentinel API",
    description="Fatality Precursor Early-Warning System for Oil India Limited (PS 165)",
    version="2.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_single_report(
    db: Session,
    report_in: IncidentCreate
) -> IncidentReport:
    """
    Executes the strict 7-layer pipeline on a single incoming report:
    1. OPSEC PII sanitization
    2. Dialect / Code-switch normalization
    3. Feature & physical metric extraction
    4. Stage A recall pre-filter (<5ms)
    5. Stage B few-shot LLM evaluation + saliency heatmap + causal chain
    6. AES-256 authenticated encryption & Merkle blockchain audit block creation
    """
    inc_id = report_in.id or f"OIL-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:17]}"
    
    # Layer 1b: OPSEC Crew PII Sanitization
    opsec_sanitized_text, opsec_redactions = crypto_engine.sanitize_field_crew_opsec(report_in.raw_text)

    # Layer 2: Preprocessing & Domain Lexicon / Code-Switching
    prep_res = clean_and_normalize_text(opsec_sanitized_text)
    
    # Layer 3: Feature Extraction & Physical Metric Parsing
    features = extract_structured_features(
        prep_res.normalized_text,
        detected_lexicon=prep_res.detected_lexicon
    )
    
    # Layer 4 - Stage A: Recall Pre-Filter
    stage_a_res = run_stage_a_prefilter(
        prep_res.normalized_text,
        features=features
    )
    
    # Layer 4 - Stage B: Few-Shot Precision Classifier (ONLY runs if Stage A flags!)
    stage_b_executed = False
    stage_b_score = 0.05
    sif_category = "Low / Non-SIF"
    iogp_rules = ["Work Authorisation"]
    rationale = "Dismissed by Stage A recall filter: No high energy source or barrier failure detected."
    key_phrases = []
    exemplar_ids = []
    saliency_heatmap = []
    causal_chain = {}

    if stage_a_res["flagged"]:
        stage_b_executed = True
        stage_b_res = evaluate_few_shot_rubric(
            normalized_text=prep_res.normalized_text,
            raw_text=report_in.raw_text,
            features=features,
            stage_a_result=stage_a_res
        )
        stage_b_score = stage_b_res["stage_b_score"]
        sif_category = stage_b_res["sif_potential_category"]
        iogp_rules = stage_b_res["iogp_rules"]
        rationale = stage_b_res["written_rationale"]
        key_phrases = stage_b_res["key_driving_phrases"]
        exemplar_ids = stage_b_res["retrieved_exemplar_ids"]
        saliency_heatmap = stage_b_res["saliency_heatmap"]
        causal_chain = stage_b_res["causal_chain"]

    # Layer 7: Military-Grade Authenticated Encryption (AES-256 CTR + HMAC-SHA256)
    encrypted_payload = crypto_engine.encrypt_payload(report_in.raw_text)

    # Merkle Blockchain Audit Ledger chaining
    last_block = db.query(AuditBlock).order_by(AuditBlock.block_height.desc()).first()
    prev_hash = last_block.block_hash if last_block else crypto_engine.genesis_hash
    next_height = (last_block.block_height + 1) if last_block else 1

    audit_data = crypto_engine.create_merkle_audit_block(
        block_height=next_height,
        prev_block_hash=prev_hash,
        incident_id=inc_id,
        raw_text=report_in.raw_text,
        sif_score=stage_b_score
    )

    audit_block = AuditBlock(
        block_height=audit_data["block_height"],
        timestamp=audit_data["timestamp"],
        incident_id=inc_id,
        prev_block_hash=audit_data["prev_block_hash"],
        block_hash=audit_data["block_hash"],
        payload_hash=audit_data["payload_hash"],
        hmac_signature=audit_data["hmac_signature"]
    )
    db.merge(audit_block)

    crypto_metadata = {
        "block_height": audit_data["block_height"],
        "block_hash": audit_data["block_hash"],
        "prev_block_hash": audit_data["prev_block_hash"],
        "payload_hash": audit_data["payload_hash"],
        "cipher": "AES-256-CTR + HMAC-SHA256 (FIPS-197 / FIPS-198-1)"
    }

    # Persist in DB
    record = IncidentReport(
        id=inc_id,
        facility=report_in.facility,
        location=report_in.location,
        dataset_source=report_in.dataset_source or "OIL Upper Assam Operations",
        date_reported=report_in.date_reported or datetime.utcnow().strftime("%Y-%m-%d"),
        raw_text=report_in.raw_text,
        cleaned_text=prep_res.cleaned_text,
        normalized_text=prep_res.normalized_text,
        actual_injury_severity=report_in.actual_injury_severity or "Near Miss / No Injury",
        detected_lexicon=prep_res.detected_lexicon,
        detected_codeswitch=prep_res.detected_codeswitch,
        ocr_metadata=prep_res.ocr_metadata,
        opsec_redactions=opsec_redactions,
        hazard_type=features.get("hazard_type"),
        energy_source=features.get("energy_source"),
        equipment_involved=features.get("equipment_involved"),
        barrier_status=features.get("barrier_status"),
        extracted_features=features,
        physical_quantities=features.get("physical_quantities", []),
        stage_a_flagged=stage_a_res["flagged"],
        stage_a_score=stage_a_res["score"],
        stage_a_triggers=stage_a_res["triggers"],
        stage_b_executed=stage_b_executed,
        stage_b_score=stage_b_score,
        sif_potential_category=sif_category,
        iogp_rules=iogp_rules,
        written_rationale=rationale,
        key_driving_phrases=key_phrases,
        retrieved_exemplar_ids=exemplar_ids,
        saliency_heatmap=saliency_heatmap,
        causal_chain=causal_chain,
        crypto_metadata=crypto_metadata,
        encrypted_payload=encrypted_payload,
        review_status="Pending Review"
    )
    
    merged_record = db.merge(record)
    db.commit()
    db.refresh(merged_record)
    return merged_record


# --- API ENDPOINTS ---

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "OIL SIF-Sentinel Defense Safety Platform",
        "vector_store_size": len(vector_store.list_all_exemplars()),
        "time": datetime.utcnow().isoformat(),
        "cryptographic_standard": "AES-256-CTR + HMAC-SHA256 (FIPS-197)"
    }

@app.get("/api/iogp-rules")
def get_iogp_rules():
    """Returns fixed 9 IOGP Life-Saving Rules reference corpus."""
    return list_all_iogp_rules()

@app.get("/api/exemplars", response_model=List[ExemplarSchema])
def get_exemplars():
    """Returns current active vector store exemplars (curated + reviewer overrides)."""
    return vector_store.list_all_exemplars()

@app.get("/api/datasets")
def get_datasets():
    """Returns all available curated process-safety datasets."""
    return list_available_datasets()

@app.post("/api/datasets/load/{dataset_key}", response_model=List[IncidentResponse])
def load_dataset(dataset_key: str, db: Session = Depends(get_db)):
    """Loads and ingests a specified multi-source dataset."""
    db.query(IncidentReport).delete()
    db.query(AuditBlock).delete()
    db.commit()

    records = get_dataset_by_key(dataset_key)
    processed = []
    for rep in records:
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
        processed.append(rec)
    return processed

@app.get("/api/stream/next", response_model=IncidentResponse)
def stream_next_telemetry(db: Session = Depends(get_db)):
    """
    Simulates real-time streaming ingestion of an active field safety report.
    Picks from candidate operational field events to demonstrate live telemetry.
    """
    all_pool = REAL_HISTORICAL_TRAGEDIES_DATASET + KAGGLE_STEFANINI_DATASET
    sample = random.choice(all_pool)
    stream_id = f"STREAM-{datetime.utcnow().strftime('%H%M%S')}"
    
    inc_in = IncidentCreate(
        id=stream_id,
        facility=sample["facility"],
        location=sample["location"],
        date_reported=datetime.utcnow().strftime("%Y-%m-%d"),
        raw_text=sample["raw_text"],
        actual_injury_severity=sample.get("actual_injury_severity", "Near Miss / No Injury"),
        dataset_source=f"Live Telemetry ({sample.get('dataset_source', 'Field')})"
    )
    return process_single_report(db, inc_in)

@app.post("/api/ingest/demo", response_model=List[IncidentResponse])
def ingest_demo_batch(db: Session = Depends(get_db)):
    """Ingests default calibrated demo batch."""
    return load_dataset("oil_assam", db)

@app.post("/api/ingest/single", response_model=IncidentResponse)
def ingest_single(report: IncidentCreate, db: Session = Depends(get_db)):
    """Ingest a single new incident report (Screen 1 & 2)."""
    return process_single_report(db, report)

@app.post("/api/ingest/batch", response_model=List[IncidentResponse])
def ingest_batch(batch: BatchIngestRequest, db: Session = Depends(get_db)):
    """Ingest a batch of custom incident reports."""
    results = []
    for rep in batch.incidents:
        rec = process_single_report(db, rep)
        results.append(rec)
    return results

@app.get("/api/incidents", response_model=List[IncidentResponse])
def list_incidents(
    facility: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    sif_category: Optional[str] = Query(None),
    dataset: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Screen 3: Triage Feed
    Ranked primarily by stage_b_score (SIF-potential score) descending.
    """
    query = db.query(IncidentReport)
    
    if facility:
        query = query.filter(IncidentReport.facility == facility)
    if location:
        query = query.filter(IncidentReport.location == location)
    if sif_category:
        query = query.filter(IncidentReport.sif_potential_category == sif_category)
    if dataset:
        query = query.filter(IncidentReport.dataset_source == dataset)
    if search:
        s = f"%{search}%"
        query = query.filter(
            (IncidentReport.raw_text.ilike(s)) |
            (IncidentReport.facility.ilike(s)) |
            (IncidentReport.hazard_type.ilike(s)) |
            (IncidentReport.equipment_involved.ilike(s))
        )
        
    incidents = query.order_by(IncidentReport.stage_b_score.desc()).all()
    return incidents

@app.get("/api/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident_detail(incident_id: str, db: Session = Depends(get_db)):
    """Screen 4: Report Detail view."""
    rec = db.query(IncidentReport).filter(IncidentReport.id == incident_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Incident not found")
    return rec

@app.post("/api/incidents/{incident_id}/review", response_model=IncidentResponse)
def submit_review(
    incident_id: str,
    review: ReviewSubmission,
    db: Session = Depends(get_db)
):
    """
    Screen 5: Reviewer Decision (Human-in-the-Loop)
    Confirm or override model classification.
    Overrides write immediately to the versioned exemplar vector store!
    """
    rec = db.query(IncidentReport).filter(IncidentReport.id == incident_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    rec.reviewer_name = review.reviewer_name
    rec.reviewed_at = datetime.utcnow()
    rec.reviewer_notes = review.notes

    if review.action.lower() == "confirm":
        rec.review_status = "Confirmed"
    elif review.action.lower() == "override":
        rec.review_status = "Overridden"
        if review.override_score is not None:
            rec.reviewer_override_score = review.override_score
            rec.stage_b_score = review.override_score
        if review.override_category:
            rec.reviewer_override_category = review.override_category
            rec.sif_potential_category = review.override_category
            
        rule_tag = rec.iogp_rules[0] if rec.iogp_rules else "Work Authorisation"
        new_ex = vector_store.add_override_exemplar(
            incident_id=rec.id,
            text=rec.normalized_text or rec.raw_text,
            energy_source=rec.energy_source or "High Risk Overridden Energy",
            barrier_status=rec.barrier_status or "Reviewer Overridden Barrier",
            sif_potential="High" if "High" in rec.sif_potential_category else "Medium",
            sif_score=rec.stage_b_score,
            iogp_rule=rule_tag,
            rationale=review.notes or "Reviewer manual classification override",
            reviewer_name=review.reviewer_name
        )
        rec.exemplar_created_id = new_ex["id"]

    db.commit()
    db.refresh(rec)
    return rec

@app.get("/api/patterns")
def get_patterns(db: Session = Depends(get_db)):
    """
    Screen 6: Hazard Pattern Dashboard & 5x5 Risk Matrix
    HDBSCAN clustering, theme grouping, and trend charts.
    """
    incidents = db.query(IncidentReport).all()
    inc_dicts = [
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
            "barrier_status": r.barrier_status or "Unknown",
            "hazard_type": r.hazard_type,
            "extracted_features": r.extracted_features or {},
            "iogp_rules": r.iogp_rules or []
        }
        for r in incidents
    ]
    
    pattern_data = analyze_hazard_patterns(inc_dicts)
    return pattern_data

# --- MILITARY CRYPTOGRAPHY & AUDIT LEDGER ENDPOINTS ---

@app.get("/api/security/audit-ledger", response_model=SecurityAuditStatusSchema)
def get_security_audit_ledger(db: Session = Depends(get_db)):
    """Returns the complete immutable Merkle blockchain audit ledger with verification status."""
    blocks = db.query(AuditBlock).order_by(AuditBlock.block_height.asc()).all()
    block_dicts = [
        {
            "block_height": b.block_height,
            "timestamp": b.timestamp,
            "incident_id": b.incident_id,
            "prev_block_hash": b.prev_block_hash,
            "block_hash": b.block_hash,
            "payload_hash": b.payload_hash,
            "hmac_signature": b.hmac_signature,
            "is_tampered_simulation": b.is_tampered_simulation
        }
        for b in blocks
    ]
    
    audit_check = crypto_engine.verify_ledger_integrity(block_dicts)
    return {
        "valid": audit_check["valid"],
        "total_blocks": audit_check["total_blocks"],
        "tampered_count": audit_check["tampered_count"],
        "tampered_details": audit_check["tampered_details"],
        "cryptographic_standard": "AES-256-CTR + HMAC-SHA256 (FIPS-197 / FIPS-198-1)",
        "audit_status": audit_check["audit_status"],
        "sovereign_key_id": "OIL-ASSAM-SEC-2026-FIPS197",
        "blocks": block_dicts
    }

@app.post("/api/security/simulate-tamper")
def simulate_ledger_tampering(db: Session = Depends(get_db)):
    """
    Demonstrates Merkle blockchain anti-tamper security for Hackathon Judges.
    Simulates a rogue database update mutating a previous block's hash.
    """
    blocks = db.query(AuditBlock).order_by(AuditBlock.block_height.asc()).all()
    if len(blocks) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 audit blocks to simulate tampering.")
        
    target_block = blocks[1]
    target_block.prev_block_hash = "0000deadbeefbadf00d000000000000000000000000000000000000000000000"
    target_block.is_tampered_simulation = True
    db.commit()
    return {"message": f"Tamper simulated at block height #{target_block.block_height}. Run integrity check to observe alert."}

@app.post("/api/security/restore-ledger")
def restore_ledger(db: Session = Depends(get_db)):
    """Restores Merkle blockchain ledger to valid state."""
    blocks = db.query(AuditBlock).order_by(AuditBlock.block_height.asc()).all()
    curr_prev = crypto_engine.genesis_hash
    for b in blocks:
        b.prev_block_hash = curr_prev
        b.is_tampered_simulation = False
        curr_prev = b.block_hash
    db.commit()
    return {"message": "Merkle blockchain audit ledger restored to 100% integrity."}

@app.post("/api/reset")
def reset_database(db: Session = Depends(get_db)):
    """Resets database and loads default OIL Assam batch."""
    return load_dataset("oil_assam", db)

# --- INDUSTRY PARAMETERS & AI MODEL TRAINING ENDPOINTS ---

from .industry_trainer import industry_trainer, INDUSTRY_PARAMETERS, DATASET_SOURCES_CATALOGUE

@app.get("/api/industry-parameters")
def get_industry_parameters():
    """Returns all real-world engineering and regulatory safety standards."""
    return INDUSTRY_PARAMETERS

@app.get("/api/dataset-sources")
def get_dataset_sources_catalogue():
    """Returns detailed dataset catalogue with direct official links and parameter maps."""
    return DATASET_SOURCES_CATALOGUE

@app.get("/api/training/status")
def get_training_status():
    """Returns live training status, convergence curves, and accuracy benchmarks."""
    return industry_trainer.get_status()

@app.post("/api/training/retrain")
def trigger_ai_retraining(epochs: int = 5):
    """Calibrates and fine-tunes the neuro-symbolic models against industry standards."""
    return industry_trainer.trigger_retraining(epochs=epochs)

# Mount static frontend build if available
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/dist"))
assets_dir = os.path.join(frontend_dist, "assets")

if os.path.exists(assets_dir):
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
