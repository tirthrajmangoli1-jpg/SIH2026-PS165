with open('frontend/src/components/OfficerDecisions.jsx', 'r') as f:
    content = f.read()

# Replace the TR style to add a highlight if it's a real decision (we can just add a property `isReal: true` in the map)
pattern_map = "status: i.review_action === 'override' ? 'Calibrated' : 'Reviewed'"
new_map = "status: i.review_action === 'override' ? 'Calibrated' : 'Reviewed',\n      isReal: true"
content = content.replace(pattern_map, new_map)

pattern_tr = """<tr key={decision.id} className="hover:bg-slate-800/20 transition group">"""
new_tr = """<tr key={decision.id} className={`transition group ${decision.isReal ? 'bg-indigo-950/20 hover:bg-indigo-900/30' : 'hover:bg-slate-800/20'}`}>"""
content = content.replace(pattern_tr, new_tr)

with open('frontend/src/components/OfficerDecisions.jsx', 'w') as f:
    f.write(content)
