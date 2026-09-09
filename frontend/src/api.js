/**
 * API client for OIL SIF-Sentinel Backend
 */

const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchIncidents(params = {}) {
  const query = new URLSearchParams();
  if (params.facility) query.append('facility', params.facility);
  if (params.location) query.append('location', params.location);
  if (params.sif_category) query.append('sif_category', params.sif_category);
  if (params.dataset) query.append('dataset', params.dataset);
  if (params.search) query.append('search', params.search);

  const res = await fetch(`${API_BASE}/incidents?${query.toString()}`);
  return res.json();
}

export async function fetchIncidentDetail(id) {
  const res = await fetch(`${API_BASE}/incidents/${id}`);
  return res.json();
}

export async function ingestDemoBatch() {
  const res = await fetch(`${API_BASE}/ingest/demo`, { method: 'POST' });
  return res.json();
}

export async function ingestSingleReport(data) {
  const res = await fetch(`${API_BASE}/ingest/single`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function submitReview(id, reviewData) {
  const res = await fetch(`${API_BASE}/incidents/${id}/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reviewData)
  });
  return res.json();
}

export async function fetchPatterns() {
  const res = await fetch(`${API_BASE}/patterns`);
  return res.json();
}

export async function fetchExemplars() {
  const res = await fetch(`${API_BASE}/exemplars`);
  return res.json();
}

export async function fetchIOGPRules() {
  const res = await fetch(`${API_BASE}/iogp-rules`);
  return res.json();
}

export async function fetchDatasets() {
  const res = await fetch(`${API_BASE}/datasets`);
  return res.json();
}

export async function loadDataset(datasetKey) {
  const res = await fetch(`${API_BASE}/datasets/load/${datasetKey}`, { method: 'POST' });
  return res.json();
}

export async function streamNextTelemetry() {
  const res = await fetch(`${API_BASE}/stream/next`);
  return res.json();
}

export async function fetchSecurityAuditLedger() {
  const res = await fetch(`${API_BASE}/security/audit-ledger`);
  return res.json();
}

export async function simulateLedgerTampering() {
  const res = await fetch(`${API_BASE}/security/simulate-tamper`, { method: 'POST' });
  return res.json();
}

export async function restoreLedger() {
  const res = await fetch(`${API_BASE}/security/restore-ledger`, { method: 'POST' });
  return res.json();
}

export async function resetDatabase() {
  const res = await fetch(`${API_BASE}/reset`, { method: 'POST' });
  return res.json();
}

export async function fetchIndustryParameters() {
  const res = await fetch(`${API_BASE}/industry-parameters`);
  return res.json();
}

export async function fetchDatasetSources() {
  const res = await fetch(`${API_BASE}/dataset-sources`);
  return res.json();
}

export async function fetchTrainingStatus() {
  const res = await fetch(`${API_BASE}/training/status`);
  return res.json();
}

export async function triggerRetraining(epochs = 5) {
  const res = await fetch(`${API_BASE}/training/retrain?epochs=${epochs}`, { method: 'POST' });
  return res.json();
}
