import os
import re

DIR = "/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src"

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Global Backgrounds
    content = re.sub(r'bg-slate-50\b', 'bg-slate-900', content)
    content = re.sub(r'bg-white\b', 'bg-slate-950', content)
    
    # Text colors
    content = re.sub(r'text-slate-900\b', 'text-slate-100', content)
    content = re.sub(r'text-slate-800\b', 'text-slate-200', content)
    content = re.sub(r'text-slate-700\b', 'text-slate-300', content)
    content = re.sub(r'text-slate-600\b', 'text-slate-400', content)
    
    # Borders
    content = re.sub(r'border-slate-200\b', 'border-slate-800', content)
    content = re.sub(r'border-slate-300\b', 'border-slate-700', content)
    content = re.sub(r'border-slate-100\b', 'border-slate-800', content)
    
    # Hover states
    content = re.sub(r'hover:bg-slate-100\b', 'hover:bg-slate-800', content)
    content = re.sub(r'hover:bg-slate-50\b', 'hover:bg-slate-900', content)
    content = re.sub(r'hover:bg-slate-200\b', 'hover:bg-slate-800', content)
    
    # Subtle bg
    content = re.sub(r'bg-slate-100\b', 'bg-slate-800', content)
    content = re.sub(r'bg-slate-200\b', 'bg-slate-800', content)
    
    # Shadows
    content = re.sub(r'shadow-sm\b', 'shadow-none', content)
    content = re.sub(r'shadow-xs\b', 'shadow-none', content)
    content = re.sub(r'shadow-2xs\b', 'shadow-none', content)

    # Some specific fixes for black theme
    content = re.sub(r'bg-amber-50\b', 'bg-amber-950/30', content)
    content = re.sub(r'bg-amber-100\b', 'bg-amber-900/40', content)
    content = re.sub(r'text-amber-800\b', 'text-amber-400', content)
    content = re.sub(r'text-amber-900\b', 'text-amber-300', content)
    content = re.sub(r'text-amber-700\b', 'text-amber-400', content)
    content = re.sub(r'border-amber-300\b', 'border-amber-800/50', content)
    content = re.sub(r'border-amber-200\b', 'border-amber-800/50', content)

    content = re.sub(r'bg-rose-50\b', 'bg-rose-950/30', content)
    content = re.sub(r'bg-rose-100\b', 'bg-rose-900/40', content)
    content = re.sub(r'text-rose-800\b', 'text-rose-400', content)
    content = re.sub(r'text-rose-900\b', 'text-rose-300', content)
    content = re.sub(r'text-rose-700\b', 'text-rose-400', content)
    content = re.sub(r'border-rose-300\b', 'border-rose-800/50', content)

    content = re.sub(r'bg-red-50\b', 'bg-red-950/30', content)
    content = re.sub(r'bg-red-100\b', 'bg-red-900/40', content)
    content = re.sub(r'text-red-800\b', 'text-red-400', content)
    content = re.sub(r'text-red-900\b', 'text-red-300', content)
    content = re.sub(r'text-red-700\b', 'text-red-400', content)
    content = re.sub(r'border-red-300\b', 'border-red-800/50', content)

    content = re.sub(r'bg-emerald-50\b', 'bg-emerald-950/30', content)
    content = re.sub(r'bg-emerald-100\b', 'bg-emerald-900/40', content)
    content = re.sub(r'text-emerald-800\b', 'text-emerald-400', content)
    content = re.sub(r'text-emerald-900\b', 'text-emerald-300', content)
    content = re.sub(r'border-emerald-300\b', 'border-emerald-800/50', content)

    content = re.sub(r'bg-sky-50\b', 'bg-sky-950/30', content)
    content = re.sub(r'bg-sky-100\b', 'bg-sky-900/40', content)
    content = re.sub(r'text-sky-800\b', 'text-sky-400', content)
    content = re.sub(r'text-sky-900\b', 'text-sky-300', content)
    content = re.sub(r'border-sky-300\b', 'border-sky-800/50', content)

    content = re.sub(r'bg-indigo-50\b', 'bg-indigo-950/30', content)
    content = re.sub(r'bg-indigo-100\b', 'bg-indigo-900/40', content)
    content = re.sub(r'text-indigo-800\b', 'text-indigo-400', content)
    content = re.sub(r'text-indigo-900\b', 'text-indigo-300', content)
    content = re.sub(r'border-indigo-300\b', 'border-indigo-800/50', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk(DIR):
    for f in files:
        if f.endswith('.jsx'):
            process_file(os.path.join(root, f))

print("Dark mode applied successfully.")
