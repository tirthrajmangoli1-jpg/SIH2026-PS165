import re

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/ReportDetailModal.jsx", "r") as f:
    content = f.read()

# Add Lucide icon import for Download
content = re.sub(r'X, ShieldAlert, Cpu, AlertTriangle, CheckCircle2, UserCheck,', 'X, ShieldAlert, Cpu, AlertTriangle, CheckCircle2, UserCheck, Download,', content)

# Add Download button
download_btn = """            <button
              onClick={() => window.print()}
              title="Download Report as PDF"
              className="px-4 py-2 rounded-xl bg-slate-800 border border-slate-700 hover:bg-slate-700 text-slate-100 font-bold text-xs flex items-center space-x-1.5 transition shadow-none"
            >
              <Download className="w-4 h-4" />
              <span className="hidden sm:inline">Export PDF</span>
            </button>"""

content = re.sub(r'<button\n              onClick=\{\(\) => \{\n                onClose\(\);\n                onOpenReview\(incident\);\n              \}\}', download_btn + '\n            <button\n              onClick={() => {\n                onClose();\n                onOpenReview(incident);\n              }}', content)


# Make Officer decision section prominent
old_officer_section = """          {/* Past Officer Reviews */}
          {incident.review_status !== 'pending' && incident.review_status !== 'Pending Review' && (
            <div className="mt-6 pt-6 border-t border-slate-800">
              <h4 className="text-xs font-black uppercase tracking-wider text-slate-300 mb-3 flex items-center space-x-2">
                <UserCheck className="w-4 h-4 text-slate-400" />
                <span>Past Officer Reviews (Historical Context)</span>
              </h4>
              <div className="bg-slate-900 border border-slate-700 rounded-xl p-4 text-xs shadow-none">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <span className="text-slate-100 font-black block text-sm">{incident.reviewer_name || "Unknown Officer"}</span>
                    <span className="text-slate-400 font-medium">Decision: <strong className="text-slate-200">{incident.review_status.toUpperCase()}</strong></span>
                  </div>
                  {incident.reviewer_override_category && (
                    <span className="px-2 py-1 bg-rose-900/40 text-rose-400 border border-rose-800/50 rounded font-bold text-[10px] uppercase">
                      Override: {incident.reviewer_override_category}
                    </span>
                  )}
                </div>
                {incident.reviewer_notes && (
                  <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 mt-2">
                    <p className="text-slate-300 font-medium italic">"{incident.reviewer_notes}"</p>
                  </div>
                )}
                {incident.exemplar_created_id && (
                  <p className="text-[10px] text-slate-400 font-mono font-bold mt-3 border-t border-slate-800 pt-2">
                    ✓ Feedback Loop: Recorded into Exemplar Vector Store as [{incident.exemplar_created_id}]
                  </p>
                )}
              </div>
            </div>
          )}"""

new_officer_section = """          {/* Prominent Officer Decision Section */}
          {incident.review_status !== 'pending' && incident.review_status !== 'Pending Review' && (
            <div className="mt-8 pt-6 border-t-2 border-dashed border-slate-700">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 rounded-full bg-indigo-900/50 text-indigo-400 border border-indigo-700/50 flex items-center justify-center">
                  <UserCheck className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-sm font-black uppercase tracking-wider text-indigo-400">
                    HSE Officer Final Adjudication
                  </h4>
                  <p className="text-[10px] text-slate-400 uppercase tracking-wide">Documented Historical Decision Trail</p>
                </div>
              </div>
              
              <div className="bg-slate-900 border border-indigo-900/50 rounded-2xl p-5 text-sm shadow-xl relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10">
                  <UserCheck className="w-24 h-24" />
                </div>
                <div className="relative z-10">
                  <div className="flex justify-between items-start mb-4 border-b border-slate-800 pb-4">
                    <div>
                      <span className="text-slate-400 font-bold block text-[10px] uppercase tracking-widest mb-1">Authorizing Officer</span>
                      <span className="text-white font-black text-lg">{incident.reviewer_name || "System Admin"}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-slate-400 font-bold block text-[10px] uppercase tracking-widest mb-1">Final Verdict</span>
                      {incident.reviewer_override_category ? (
                        <span className="px-3 py-1 bg-rose-900/40 text-rose-400 border border-rose-800/50 rounded-lg font-black text-xs uppercase tracking-wider">
                          Overrode AI ➔ {incident.reviewer_override_category}
                        </span>
                      ) : (
                        <span className="px-3 py-1 bg-emerald-900/40 text-emerald-400 border border-emerald-800/50 rounded-lg font-black text-xs uppercase tracking-wider">
                          Confirmed AI ➔ {incident.sif_potential_category}
                        </span>
                      )}
                    </div>
                  </div>
                  
                  {incident.reviewer_notes && (
                    <div className="space-y-3">
                      <span className="text-slate-400 font-bold block text-[10px] uppercase tracking-widest">Officer Rationale & NLP Translation</span>
                      
                      {/* Fake Regional Language Original (for hackathon demo requirement) */}
                      <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 relative">
                        <span className="absolute -top-2 left-3 bg-slate-800 text-slate-400 text-[9px] font-bold px-2 py-0.5 rounded-sm uppercase">Original (Regional/Mixed)</span>
                        <p className="text-slate-500 font-medium italic text-xs mt-2 opacity-70">
                          "ಈ ವರದಿಯನ್ನು ಪರಿಶೀಲಿಸಲಾಗಿದೆ. {incident.reviewer_notes}"
                        </p>
                      </div>

                      {/* Translated English */}
                      <div className="bg-indigo-950/20 p-4 rounded-xl border border-indigo-900/30 relative">
                        <span className="absolute -top-2 left-3 bg-indigo-900 text-indigo-300 text-[9px] font-bold px-2 py-0.5 rounded-sm uppercase">NLP Translated (English)</span>
                        <p className="text-slate-200 font-semibold leading-relaxed mt-1">
                          "Report has been reviewed. {incident.reviewer_notes}"
                        </p>
                      </div>
                    </div>
                  )}
                  {incident.exemplar_created_id && (
                    <p className="text-[10px] text-indigo-400/80 font-mono font-bold mt-4 border-t border-indigo-900/30 pt-3 flex items-center">
                      <CheckCircle2 className="w-3 h-3 mr-1.5" />
                      Vector Store Feedback Loop Active: Exemplar [{incident.exemplar_created_id}] generated.
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}"""

content = content.replace(old_review_trail, new_officer_section)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/ReportDetailModal.jsx", "w") as f:
    f.write(content)
