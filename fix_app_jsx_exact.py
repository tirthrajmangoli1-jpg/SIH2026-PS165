with open('frontend/src/App.jsx', 'r') as f:
    content = f.read()

pattern = """        {activeTab === 'triage' ? (
          <TriageFeed
            incidents={incidents}
            onSelectIncident={(inc) => setSelectedIncident(inc)}
            onOpenContext={(inc) => setContextIncident(inc)}
            onReviewIncident={(inc) => setReviewingIncident(inc)}
            selectedId={selectedIncident?.id}
          />
        ) : (
          <PatternDashboard
            patterns={patterns}
            onSelectTheme={(theme) => console.log(theme)}
            onSelectIncidentId={(id) => {
              const inc = incidents.find(i => i.id === id);
              if (inc) setSelectedIncident(inc);
            }}
          />
        )}"""

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
          <PatternDashboard
            patterns={patterns}
            onSelectTheme={(theme) => console.log(theme)}
            onSelectIncidentId={(id) => {
              const inc = incidents.find(i => i.id === id);
              if (inc) setSelectedIncident(inc);
            }}
          />
        )}"""

content = content.replace(pattern, new_code)
with open('frontend/src/App.jsx', 'w') as f:
    f.write(content)
