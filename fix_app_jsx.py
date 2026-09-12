import re

with open('frontend/src/App.jsx', 'r') as f:
    content = f.read()

pattern = r"""        \{activeTab === 'triage' \? \(
          <TriageFeed
            incidents=\{incidents\}
            onSelectIncident=\{\(inc\) => setSelectedIncident\(inc\)\}
            onOpenContext=\{\(inc\) => setContextIncident\(inc\)\}
            onReviewIncident=\{\(inc\) => setReviewingIncident\(inc\)\}
            selectedId=\{selectedIncident\?\.id\}
          />
        \) : \(
          <PatternDashboard"""

new_code = """        {activeTab === 'triage' && (
          <TriageFeed
            incidents={incidents}
            onSelectIncident={(inc) => setSelectedIncident(inc)}
            onOpenContext={(inc) => setContextIncident(inc)}
            onReviewIncident={(inc) => setReviewingIncident(inc)}
            selectedId={selectedIncident?.id}
          />
        )}
        
        {activeTab === 'decisions' && (
          <OfficerDecisions incidents={incidents} />
        )}
        
        {activeTab === 'patterns' && (
          <PatternDashboard"""

# Also fix the previous PatternDashboard if condition, because activeTab was just a ternary
# If the original was a ternary, we must handle the closing tags correctly!
