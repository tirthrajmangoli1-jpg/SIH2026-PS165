import re
with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/ReportDetailModal.jsx", "r") as f:
    content = f.read()

# Add Lucide icon import for Download
content = re.sub(r'X, ShieldAlert, Cpu, AlertTriangle, CheckCircle2, UserCheck, Lock, Activity, Flame', 'X, ShieldAlert, Cpu, AlertTriangle, CheckCircle2, UserCheck, Lock, Activity, Flame, Download', content)

download_btn = """            <button
              onClick={() => window.print()}
              title="Download Report as PDF"
              className="px-4 py-2 rounded-xl bg-slate-800 border border-slate-700 hover:bg-slate-700 text-slate-100 font-bold text-xs flex items-center space-x-1.5 transition shadow-none print:hidden"
            >
              <Download className="w-4 h-4" />
              <span className="hidden sm:inline">Export PDF</span>
            </button>"""

content = re.sub(r'<button\n              onClick=\{\(\) => \{\n                onClose\(\);\n                onOpenReview\(incident\);\n              \}\}', download_btn + '\n            <button\n              onClick={() => {\n                onClose();\n                onOpenReview(incident);\n              }}', content)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/ReportDetailModal.jsx", "w") as f:
    f.write(content)
