"""
SQLAlchemy Data Models for OIL SIF-Sentinel:
1. IncidentReport: Stores ingested reports, multi-stage classifications, extracted features,
   thermodynamic saliency weights, causal chains, physical quantities, and cryptographic Merkle proof.
2. ExemplarRecord: Curated and reviewer-overridden exemplars powering Stage A and Stage B vector stores.
3. AuditBlock: Immutable Merkle Blockchain Audit Ledger for sovereign anti-tamper tracking.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, JSON, DateTime
from .database import Base

class IncidentReport(Base):
    __tablename__ = "incident_reports"

    id = Column(String(64), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    date_reported = Column(String(32), nullable=True)
    facility = Column(String(128), index=True)      # e.g., "Rig OIL-04", "Duliajan Central Workshop"
    location = Column(String(128), index=True)      # e.g., "Duliajan", "Moran", "Nahorkatiya"
    dataset_source = Column(String(64), default="OIL Upper Assam Operations", index=True)
    
    # Text contents
    raw_text = Column(Text, nullable=False)
    cleaned_text = Column(Text, nullable=True)
    normalized_text = Column(Text, nullable=True)
    
    # Ground truth / reported actual outcome (Crucial distinction from SIF potential)
    actual_injury_severity = Column(String(64), default="Near Miss / No Injury")
    
    # Preprocessing metadata
    detected_lexicon = Column(JSON, default=list)
    detected_codeswitch = Column(JSON, default=list)
    ocr_metadata = Column(JSON, default=dict)
    opsec_redactions = Column(JSON, default=list)
    
    # Feature Extraction (Layer 3)
    hazard_type = Column(String(128), nullable=True)
    energy_source = Column(String(128), nullable=True)
    equipment_involved = Column(String(128), nullable=True)
    barrier_status = Column(String(128), nullable=True)
    extracted_features = Column(JSON, default=dict)
    physical_quantities = Column(JSON, default=list)
    
    # Stage A Classification (Recall Pre-Filter)
    stage_a_flagged = Column(Boolean, default=False, index=True)
    stage_a_score = Column(Float, default=0.0)
    stage_a_triggers = Column(JSON, default=list)
    
    # Stage B Classification (Few-Shot Precision LLM + Saliency + Causal Chain)
    stage_b_executed = Column(Boolean, default=False)
    stage_b_score = Column(Float, default=0.0, index=True) # 0.0 - 1.0 calibrated SIF potential
    sif_potential_category = Column(String(32), default="Low / Non-SIF", index=True) # High, Medium, Low
    iogp_rules = Column(JSON, default=list)               # e.g. ["Safe Mechanical Lifting", "Line of Fire"]
    written_rationale = Column(Text, nullable=True)
    key_driving_phrases = Column(JSON, default=list)       # Substrings driving classification for UI highlight
    retrieved_exemplar_ids = Column(JSON, default=list)
    
    # Advanced NLP Additions
    saliency_heatmap = Column(JSON, default=list)          # Token-level saliency weights [{token, weight, tag}]
    causal_chain = Column(JSON, default=dict)              # {root_precursor, barrier_failure, catastrophic_consequence}
    
    # Cryptographic & Merkle Audit Metadata
    crypto_metadata = Column(JSON, default=dict)           # {merkle_block_height, block_hash, prev_hash, hmac_signature}
    encrypted_payload = Column(JSON, default=dict)         # AES-256 ciphertext & HMAC tag
    
    # Human-in-the-Loop Review (Layer 5)
    review_status = Column(String(32), default="Pending Review", index=True) # "Pending Review", "Confirmed", "Overridden"
    reviewer_name = Column(String(64), nullable=True)
    reviewer_override_score = Column(Float, nullable=True)
    reviewer_override_category = Column(String(32), nullable=True)
    reviewer_notes = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    exemplar_created_id = Column(String(64), nullable=True)
    
    # Pattern Analysis clustering tag (Layer 6)
    cluster_id = Column(Integer, default=-1, index=True)
    cluster_theme = Column(String(128), nullable=True)


class ExemplarRecord(Base):
    __tablename__ = "exemplars"

    id = Column(String(64), primary_key=True, index=True)
    incident_id = Column(String(64), nullable=True)
    text = Column(Text, nullable=False)
    energy_source = Column(String(128), nullable=True)
    barrier_status = Column(String(128), nullable=True)
    sif_potential = Column(String(32), nullable=False)     # "High", "Medium", "Low"
    sif_score = Column(Float, default=0.0)
    iogp_rule = Column(String(64), nullable=False)
    rationale = Column(Text, nullable=True)
    source = Column(String(32), default="initial_curated")  # "initial_curated" or "human_override"
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditBlock(Base):
    __tablename__ = "merkle_audit_blocks"

    block_height = Column(Integer, primary_key=True, index=True)
    timestamp = Column(Float, nullable=False)
    incident_id = Column(String(64), index=True)
    prev_block_hash = Column(String(64), nullable=False)
    block_hash = Column(String(64), nullable=False, unique=True)
    payload_hash = Column(String(64), nullable=False)
    hmac_signature = Column(String(64), nullable=False)
    is_tampered_simulation = Column(Boolean, default=False)
