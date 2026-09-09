"""
Pydantic Schemas for OIL SIF-Sentinel API
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class IncidentCreate(BaseModel):
    id: Optional[str] = None
    facility: str = Field(..., example="Rig OIL-04")
    location: str = Field(..., example="Duliajan")
    date_reported: Optional[str] = Field(None, example="2024-05-12")
    raw_text: str = Field(..., example="While tripping pipe, Kelly hose safety clamp broke loose...")
    actual_injury_severity: Optional[str] = Field("Near Miss / No Injury", example="Near Miss / No Injury")
    dataset_source: Optional[str] = Field("OIL Upper Assam Operations", example="OIL Upper Assam Operations")

class BatchIngestRequest(BaseModel):
    incidents: List[IncidentCreate]

class ReviewSubmission(BaseModel):
    reviewer_name: str = Field(..., example="Chief Safety Officer Borah")
    action: str = Field(..., example="confirm") # "confirm" or "override"
    override_category: Optional[str] = Field(None, example="High SIF Potential")
    override_score: Optional[float] = Field(None, example=0.88)
    notes: Optional[str] = Field(None, example="High pressure release in immediate line of fire; sling was single barrier.")

class IncidentResponse(BaseModel):
    id: str
    created_at: Optional[datetime] = None
    date_reported: Optional[str] = None
    facility: str
    location: str
    dataset_source: Optional[str] = "OIL Upper Assam Operations"
    raw_text: str
    cleaned_text: Optional[str] = None
    normalized_text: Optional[str] = None
    actual_injury_severity: str
    
    # Preprocessing
    detected_lexicon: List[Dict[str, Any]] = []
    detected_codeswitch: List[Dict[str, Any]] = []
    ocr_metadata: Dict[str, Any] = {}
    opsec_redactions: List[Dict[str, str]] = []
    
    # Feature Extraction
    hazard_type: Optional[str] = None
    energy_source: Optional[str] = None
    equipment_involved: Optional[str] = None
    barrier_status: Optional[str] = None
    extracted_features: Dict[str, Any] = {}
    physical_quantities: List[Dict[str, Any]] = []
    
    # Classification
    stage_a_flagged: bool
    stage_a_score: float
    stage_a_triggers: List[str] = []
    
    stage_b_executed: bool
    stage_b_score: float
    sif_potential_category: str
    iogp_rules: List[str] = []
    written_rationale: Optional[str] = None
    key_driving_phrases: List[str] = []
    retrieved_exemplar_ids: List[str] = []
    
    # Advanced NLP
    saliency_heatmap: List[Dict[str, Any]] = []
    causal_chain: Dict[str, Any] = {}
    
    # Cryptographic Proof
    crypto_metadata: Dict[str, Any] = {}
    encrypted_payload: Dict[str, Any] = {}
    
    # Review
    review_status: str
    reviewer_name: Optional[str] = None
    reviewer_override_score: Optional[float] = None
    reviewer_override_category: Optional[str] = None
    reviewer_notes: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    exemplar_created_id: Optional[str] = None

    # Cluster
    cluster_id: Optional[int] = None
    cluster_theme: Optional[str] = None

    class Config:
        from_attributes = True

class ExemplarSchema(BaseModel):
    id: str
    incident_id: Optional[str] = None
    text: str
    energy_source: Optional[str] = None
    barrier_status: Optional[str] = None
    sif_potential: str
    sif_score: float
    iogp_rule: str
    rationale: Optional[str] = None
    source: str
    version: int
    is_active: bool

    class Config:
        from_attributes = True

class ClusterSummarySchema(BaseModel):
    cluster_id: int
    theme_name: str
    keywords: List[str]
    incident_count: int
    high_sif_count: int
    dominant_iogp_rule: str
    facilities_impacted: List[str]
    sample_incident_ids: List[str]

class MerkleAuditBlockSchema(BaseModel):
    block_height: int
    timestamp: float
    incident_id: str
    prev_block_hash: str
    block_hash: str
    payload_hash: str
    hmac_signature: str
    is_tampered_simulation: bool

    class Config:
        from_attributes = True

class SecurityAuditStatusSchema(BaseModel):
    valid: bool
    total_blocks: int
    tampered_count: int
    tampered_details: List[Dict[str, Any]]
    cryptographic_standard: str
    audit_status: str
    sovereign_key_id: str
    blocks: List[MerkleAuditBlockSchema]
