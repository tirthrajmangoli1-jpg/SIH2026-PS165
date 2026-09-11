import re

file_path = '/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/PatternDashboard.jsx'

with open(file_path, 'r') as f:
    content = f.read()

# We need to split the file at rankingTab === 'activities' to only fix the sites tab
sites_tab_index = content.find("rankingTab === 'sites'")
activities_tab_index = content.find("rankingTab === 'activities'")

sites_part = content[sites_tab_index:activities_tab_index]
activities_part = content[activities_tab_index:]

# Fix act -> site in the sites part
sites_part = sites_part.replace('act.sample_incident_ids', 'site.sample_incident_ids')

new_content = content[:sites_tab_index] + sites_part + activities_part

with open(file_path, 'w') as f:
    f.write(new_content)

