import React from 'react';
import { X, History, UserCheck, AlertTriangle } from 'lucide-react';

export default function ReviewHistoryModal({ incidents, onClose, onSelectIncidentId }) {
  // Filter incidents that have been reviewed
  const reviewedIncidents = incidents.filter(i => 
    i.review_status && 
    i.review_status !== 'pending' && 
    i.review_status !== 'Pending Review'
  );

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-2xl w-full max-w-4xl max-h-[85vh] shadow-2xl overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-5 border-b border-slate-200 bg-slate-50 flex items-center justify-between shrink-0">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-slate-200 text-slate-800 border border-slate-300 flex items-center justify-center">
              <History className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-black text-slate-900 uppercase">
                Past Officer Reviews Audit Trail
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Showing all historical HSE Officer decisions and overrides.
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-900 p-1.5 rounded-lg bg-white border border-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="overflow-y-auto p-6 bg-white space-y-4">
          {reviewedIncidents.length === 0 ? (
            <div className="text-center p-12 bg-slate-50 rounded-xl border border-slate-200">
              <UserCheck className="w-8 h-8 mx-auto text-slate-400 mb-3" />
              <p className="text-slate-600 font-bold">No officer reviews recorded yet.</p>
              <p className="text-slate-500 text-xs mt-1">Review some reports in the Triage Feed to populate this audit trail.</p>
            </div>
          ) : (
            reviewedIncidents.map(incident => (
              <div key={incident.id} className="border border-slate-200 rounded-xl p-4 bg-slate-50 flex flex-col space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-black text-slate-900 flex items-center space-x-2">
                      <span>{incident.reviewer_name || "Unknown Officer"}</span>
                      {incident.review_status === "override" ? (
                        <span className="px-1.5 py-0.5 bg-rose-100 text-rose-800 border border-rose-300 rounded text-[9px] uppercase tracking-wide">
                          Overrode AI
                        </span>
                      ) : (
                        <span className="px-1.5 py-0.5 bg-emerald-100 text-emerald-800 border border-emerald-300 rounded text-[9px] uppercase tracking-wide">
                          Confirmed AI
                        </span>
                      )}
                    </h4>
                    <p className="text-[10px] text-slate-500 font-mono mt-1">
                      Incident Ref: {incident.id.substring(0, 8)} · {incident.facility}
                    </p>
                  </div>
                  <button 
                    onClick={() => {
                      onClose();
                      onSelectIncidentId && onSelectIncidentId(incident.id);
                    }}
                    className="px-3 py-1 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-md text-[11px] font-bold transition"
                  >
                    View Report
                  </button>
                </div>
                
                <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-sm text-xs space-y-2">
                  <div className="flex items-center justify-between text-[11px] border-b border-slate-100 pb-2 mb-2">
                    <span className="text-slate-500 font-bold uppercase">Final Classification:</span>
                    <span className="font-black text-slate-900">{incident.reviewer_override_category || incident.sif_potential_category}</span>
                  </div>
                  <p className="text-slate-700 italic font-medium">
                    "{incident.reviewer_notes || "No rationale provided."}"
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
