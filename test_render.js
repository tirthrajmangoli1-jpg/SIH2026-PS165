import React from 'react';
import { renderToString } from 'react-dom/server';
import ReportDetailModal from './frontend/src/components/ReportDetailModal.jsx';

const mockIncident = {
  id: "HIST-BAGHJAN-001",
  facility: "Baghjan Gas Well No. 5",
  location: "Baghjan, Tinsukia, Assam",
  date_reported: "2020-05-15",
  dataset_source: "Baghjan Blowout Pre-Incident Logs",
  actual_injury_severity: "Near Miss / No Injury",
  sif_potential_category: "High SIF Potential",
  stage_b_score: 0.95,
  raw_text: "Observed multiple minor gas kicks...",
  physical_quantities: [],
  causal_chain: {
    root_precursor: "Testing",
    intermediate_barrier_failure: "Testing",
    credible_catastrophic_consequence: "Testing"
  },
  saliency_heatmap: [],
  key_driving_phrases: [],
  written_rationale: "Rationale",
  hazard_type: "Hazard",
  energy_source: "Energy",
  equipment_involved: "Equipment",
  barrier_status: "Failed",
  iogp_rules: [],
  detected_codeswitch: [],
  opsec_redactions: [],
  review_status: "Pending Review"
};

try {
  const html = renderToString(React.createElement(ReportDetailModal, { incident: mockIncident, onClose: () => {} }));
  console.log("RENDER SUCCESS: ", html.substring(0, 50));
} catch (e) {
  console.error("RENDER CRASHED:", e);
}
