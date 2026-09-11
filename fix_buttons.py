import re

file_path = '/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/PatternDashboard.jsx'

with open(file_path, 'r') as f:
    content = f.read()

# Replace inner buttons with span
content = re.sub(
    r'<button key=\{id\} onClick=\{.*?\} className="(.*?)">(.*?)</button>',
    r'<span key={id} className="\1">\2</span>',
    content
)

with open(file_path, 'w') as f:
    f.write(content)

