import re

# 1. Header.jsx - Flatten colors
with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/Header.jsx", "r") as f:
    header = f.read()

# Remove specific color classes and replace with slate
header = re.sub(r'bg-amber-500 text-slate-950', 'bg-slate-800 text-white', header)
header = re.sub(r'bg-amber-50 hover:bg-amber-100 text-amber-900 border-amber-300', 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-300', header)
header = re.sub(r'text-amber-600', 'text-slate-500', header)

header = re.sub(r'bg-indigo-50 hover:bg-indigo-100 text-indigo-800 border-indigo-300', 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-300', header)
header = re.sub(r'text-indigo-600', 'text-slate-500', header)

header = re.sub(r'bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-500 hover:to-blue-500 text-white shadow-sm shadow-blue-500/20', 'bg-slate-800 hover:bg-slate-700 text-white border border-slate-900', header)

# Change Triage/Pattern active state
header = re.sub(r'bg-amber-500 text-slate-950 shadow-sm', 'bg-slate-800 text-white shadow-sm', header)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/Header.jsx", "w") as f:
    f.write(header)

# 2. AutoProcessingBanner.jsx - Flatten colors
with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/AutoProcessingBanner.jsx", "r") as f:
    banner = f.read()

banner = re.sub(r'bg-sky-50 border-sky-200', 'bg-white border-slate-200', banner)
banner = re.sub(r'text-sky-700', 'text-slate-600', banner)
banner = re.sub(r'bg-blue-50 border-blue-200', 'bg-white border-slate-200', banner)
banner = re.sub(r'text-blue-700', 'text-slate-600', banner)
banner = re.sub(r'bg-amber-50 border-amber-300', 'bg-white border-slate-200', banner)
banner = re.sub(r'text-amber-700', 'text-slate-600', banner)
banner = re.sub(r'bg-rose-50 border-rose-300', 'bg-white border-slate-300', banner)
banner = re.sub(r'text-rose-700', 'text-red-700', banner)
banner = re.sub(r'text-emerald-700', 'text-slate-600', banner)
banner = re.sub(r'bg-emerald-50 border-emerald-200', 'bg-white border-slate-200', banner)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/AutoProcessingBanner.jsx", "w") as f:
    f.write(banner)

