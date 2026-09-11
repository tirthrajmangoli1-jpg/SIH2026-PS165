import re

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/ReportDetailModal.jsx", "r") as f:
    content = f.read()

# Replace Review Decision Audit Trail with "Past Officer Reviews"
old_review_trail = """          {/* Review Decision Audit Trail */}
          {incident.review_status !== 'Pending Review' && (
            <div className="bg-slate-50 border border-blue-200 rounded-2xl p-4.5 text-xs space-y-1 shadow-2xs">
              <span className="text-blue-900 font-black block">Safety Officer Review Record:</span>
              <p className="text-slate-800 font-medium">
                Reviewer: <strong>{incident.reviewer_name}</strong> · Decision: <strong className="text-slate-950 font-bold">{incident.review_status}</strong>
              </p>
              {incident.reviewer_notes && (
                <p className="text-slate-600 italic">"{incident.reviewer_notes}"</p>
              )}
              {incident.exemplar_created_id && (
                <p className="text-[11px] text-cyan-800 font-mono font-bold mt-1">
                  ✓ Recorded into Exemplar Vector Store as ID: {incident.exemplar_created_id}
                </p>
              )}
            </div>
          )}"""

new_review_trail = """          {/* Past Officer Reviews */}
          {incident.review_status !== 'pending' && incident.review_status !== 'Pending Review' && (
            <div className="mt-6 pt-6 border-t border-slate-200">
              <h4 className="text-xs font-black uppercase tracking-wider text-slate-700 mb-3 flex items-center space-x-2">
                <UserCheck className="w-4 h-4 text-slate-500" />
                <span>Past Officer Reviews (Historical Context)</span>
              </h4>
              <div className="bg-slate-50 border border-slate-300 rounded-xl p-4 text-xs shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <span className="text-slate-900 font-black block text-sm">{incident.reviewer_name || "Unknown Officer"}</span>
                    <span className="text-slate-500 font-medium">Decision: <strong className="text-slate-800">{incident.review_status.toUpperCase()}</strong></span>
                  </div>
                  {incident.reviewer_override_category && (
                    <span className="px-2 py-1 bg-rose-100 text-rose-800 border border-rose-200 rounded font-bold text-[10px] uppercase">
                      Override: {incident.reviewer_override_category}
                    </span>
                  )}
                </div>
                {incident.reviewer_notes && (
                  <div className="bg-white p-3 rounded-lg border border-slate-200 mt-2">
                    <p className="text-slate-700 font-medium italic">"{incident.reviewer_notes}"</p>
                  </div>
                )}
                {incident.exemplar_created_id && (
                  <p className="text-[10px] text-slate-500 font-mono font-bold mt-3 border-t border-slate-200 pt-2">
                    ✓ Feedback Loop: Recorded into Exemplar Vector Store as [{incident.exemplar_created_id}]
                  </p>
                )}
              </div>
            </div>
          )}"""

content = content.replace(old_review_trail, new_review_trail)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/ReportDetailModal.jsx", "w") as f:
    f.write(content)

