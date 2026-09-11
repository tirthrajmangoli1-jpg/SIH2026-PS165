import re

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/ReviewerModal.jsx", "r") as f:
    content = f.read()

content = re.sub(r'bg-amber-100 text-amber-800 border border-amber-300', 'bg-slate-200 text-slate-800 border border-slate-300', content)
content = re.sub(r'bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-md shadow-amber-500/20', 'bg-slate-800 hover:bg-slate-900 text-white shadow-sm border border-slate-700', content)
content = re.sub(r'focus:ring-amber-500/30 focus:border-amber-500', 'focus:ring-slate-500/30 focus:border-slate-500', content)
content = re.sub(r'text-amber-800 font-bold bg-amber-100 border-amber-300', 'text-slate-700 font-bold bg-slate-200 border-slate-300', content)
content = re.sub(r'text-amber-600', 'text-slate-600', content)
content = re.sub(r'bg-amber-50 border-amber-500 text-amber-950 ring-amber-300', 'bg-slate-100 border-slate-500 text-slate-900 ring-slate-300', content)
content = re.sub(r'text-amber-950', 'text-slate-900', content)
content = re.sub(r'bg-amber-50/80 border border-amber-300', 'bg-slate-50 border border-slate-300', content)
content = re.sub(r'accent-amber-500', 'accent-slate-700', content)

# Change title
content = re.sub(r'Safety Officer Review Decision', 'Formal HSE Officer Review & Sign-Off', content)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/ReviewerModal.jsx", "w") as f:
    f.write(content)

