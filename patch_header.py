import re

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/Header.jsx", "r") as f:
    content = f.read()

# Replace the buttons block
new_buttons = """            {/* Officer Reviews Audit Trail Button */}
            <button
              onClick={onOpenReviewHistory}
              title="View Past Officer Decisions"
              className="px-3 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs flex items-center space-x-1.5 transition shadow-xs"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-slate-500" />
              <span className="hidden sm:inline">Officer Reviews</span>
            </button>

            {/* AI Training & Standards */}
            <button
              onClick={onOpenTrainingHub}
              title="Configure IOGP Life-Saving Rules & Model Training"
              className="px-3 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs flex items-center space-x-1.5 transition shadow-xs"
            >
              <Sparkles className="w-3.5 h-3.5 text-slate-500" />
              <span className="hidden lg:inline">AI Training & Standards</span>
            </button>

            {/* NLP Translation Log Button */}
            <button
              onClick={onOpenSecurityVault}
              title="View Regional Language to English Translation Pipeline"
              className="px-3 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs flex items-center space-x-1.5 transition shadow-xs"
            >
              <Languages className="w-3.5 h-3.5 text-slate-500" />
              <span className="hidden lg:inline">NLP Intake Log</span>
            </button>

            {/* Vector Store Exemplar Inspector */}
            <button
              onClick={onOpenExemplars}
              title="View Versioned Exemplar Store"
              className="px-3 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs flex items-center space-x-1.5 transition shadow-xs"
            >
              <Database className="w-3.5 h-3.5 text-slate-500" />
              <span className="hidden md:inline">Vector Store</span>
            </button>

            {/* Intake Report Button */}
            <button
              onClick={onOpenIntake}
              className="px-4 py-1.5 rounded-lg border border-slate-800 bg-slate-800 hover:bg-slate-900 text-white font-bold text-xs flex items-center space-x-1.5 shadow-sm transition"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>Intake</span>
            </button>"""

content = re.sub(r'\{\/\* AI Training \& Standards \*\/}.*?<span>Intake<\/span>\n            <\/button>', new_buttons, content, flags=re.DOTALL)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/Header.jsx", "w") as f:
    f.write(content)

