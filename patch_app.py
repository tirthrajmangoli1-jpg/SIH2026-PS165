import re

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/App.jsx", "r") as f:
    content = f.read()

# Imports
if "HistoricalContextModal" not in content:
    content = content.replace("import IntakeLogModal from './components/IntakeLogModal';", "import IntakeLogModal from './components/IntakeLogModal';\nimport HistoricalContextModal from './components/HistoricalContextModal';\nimport ReviewHistoryModal from './components/ReviewHistoryModal';")

# State
if "showReviewHistory" not in content:
    content = content.replace("const [showTrainingModal, setShowTrainingModal] = useState(false);", "const [showTrainingModal, setShowTrainingModal] = useState(false);\n  const [contextIncident, setContextIncident] = useState(null);\n  const [showReviewHistory, setShowReviewHistory] = useState(false);")

# Header Props
if "onOpenReviewHistory" not in content:
    content = content.replace("onOpenTrainingHub={() => setShowTrainingModal(true)}", "onOpenTrainingHub={() => setShowTrainingModal(true)}\n        onOpenReviewHistory={() => setShowReviewHistory(true)}")

# Report Detail Modal Props
if "onOpenContext" not in content:
    content = content.replace("onOpenReview={(inc) => setReviewingIncident(inc)}", "onOpenReview={(inc) => setReviewingIncident(inc)}\n          onOpenContext={(inc) => setContextIncident(inc)}")

# Mount components at bottom
if "<ReviewHistoryModal" not in content:
    content = content.replace("</div>\n  );\n}", "  {contextIncident && <HistoricalContextModal incident={contextIncident} onClose={() => setContextIncident(null)} />}\n      {showReviewHistory && <ReviewHistoryModal incidents={incidents} onClose={() => setShowReviewHistory(false)} onSelectIncidentId={(id) => { const inc = incidents.find(i => i.id === id); if (inc) setSelectedIncident(inc); }} />}\n    </div>\n  );\n}")

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/App.jsx", "w") as f:
    f.write(content)

