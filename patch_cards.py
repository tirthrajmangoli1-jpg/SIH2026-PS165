import re

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/PatternDashboard.jsx", "r") as f:
    content = f.read()

# Site card
content = re.sub(
    r'<div \n                    key={idx}\n                    className={`rounded-2xl p-5 border transition',
    r'<button \n                    onClick={() => onSelectIncidentId && site.sample_incident_ids && site.sample_incident_ids.length > 0 && onSelectIncidentId(site.sample_incident_ids[0])}\n                    key={idx}\n                    className={`text-left w-full cursor-pointer rounded-2xl p-5 border transition',
    content
)

# End of site card
content = re.sub(
    r'</div>\n                \);\n              }\)}\n            </div>\n          </div>\n        \)}',
    r'</button>\n                );\n              })}\n            </div>\n          </div>\n        )}',
    content,
    count=1
)

# Activity card
content = re.sub(
    r'<div \n                    key={idx}\n                    className={`rounded-2xl p-5 border transition',
    r'<button \n                    onClick={() => onSelectIncidentId && act.sample_incident_ids && act.sample_incident_ids.length > 0 && onSelectIncidentId(act.sample_incident_ids[0])}\n                    key={idx}\n                    className={`text-left w-full cursor-pointer rounded-2xl p-5 border transition',
    content
)

# End of activity card
content = re.sub(
    r'</div>\n                \);\n              }\)}\n            </div>\n          </div>\n        \)}',
    r'</button>\n                );\n              })}\n            </div>\n          </div>\n        )}',
    content
)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/PatternDashboard.jsx", "w") as f:
    f.write(content)

