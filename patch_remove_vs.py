import re
with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/Header.jsx", "r") as f:
    content = f.read()

# Remove the block:
#            {/* Vector Store Exemplar Inspector */}
#            <button
#              onClick={onOpenExemplars}
#              title="View Versioned Exemplar Store"
#              className="px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-950 hover:bg-slate-900 text-slate-300 font-bold text-xs flex items-center space-x-1.5 transition shadow-none"
#            >
#              <Database className="w-3.5 h-3.5 text-slate-500" />
#              <span className="hidden md:inline">Vector Store</span>
#            </button>

content = re.sub(r'\{\/\* Vector Store Exemplar Inspector \*\/}.*?<\/button>', '', content, flags=re.DOTALL)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/Header.jsx", "w") as f:
    f.write(content)
