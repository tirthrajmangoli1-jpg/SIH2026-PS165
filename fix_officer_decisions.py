import re

with open('frontend/src/components/OfficerDecisions.jsx', 'r') as f:
    content = f.read()

# Replace the component signature
content = content.replace("export default function OfficerDecisions() {", "export default function OfficerDecisions({ incidents = [] }) {")

# Right after state definitions, parse real decisions
parse_logic = """
  // Parse real decisions from triage incidents
  const realDecisions = incidents
    .filter(i => i.review_status === "Reviewed" || i.reviewer_name)
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
    .map(i => ({
      id: "DEC-" + i.id.split("-")[0],
      incident_id: i.id,
      officer_name: i.reviewer_name || "Assigned Officer",
      date: new Date(i.created_at || Date.now()).toISOString().split('T')[0],
      site: i.site_name || "Unknown Site",
      action: i.review_action === 'override' ? `Escalate: ${i.review_sif_category || 'High SIF'}` : 'Confirmed AI Verdict',
      comments: i.review_comments || "No justification provided.",
      language: (i.detected_codeswitch && i.detected_codeswitch.length > 0) ? "Regional Translated" : "English",
      status: i.review_action === 'override' ? 'Calibrated' : 'Reviewed'
    }));

  const allDecisions = [...realDecisions, ...mockDecisions];

  const filteredDecisions = allDecisions.filter(d => {"""

content = content.replace("  const filteredDecisions = mockDecisions.filter(d => {", parse_logic)

with open('frontend/src/components/OfficerDecisions.jsx', 'w') as f:
    f.write(content)
