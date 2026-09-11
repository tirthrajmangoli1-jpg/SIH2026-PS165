import React, { useState } from 'react';
import { X, UserCheck, ShieldAlert, Check, ArrowUpRight, Database, AlertTriangle } from 'lucide-react';

export default function ReviewerModal({ incident, onClose, onReviewSubmitted }) {
  if (!incident) return null;

  const [reviewerName, setReviewerName] = useState('Chief Safety Officer Borah');
  const [action, setAction] = useState('confirm'); // 'confirm' or 'override'
  const [overrideCategory, setOverrideCategory] = useState(incident.sif_potential_category);
  const [overrideScore, setOverrideScore] = useState(incident.stage_b_score);
  const [notes, setNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await onReviewSubmitted(incident.id, {
        reviewer_name: reviewerName,
        action: action,
        override_category: action === 'override' ? overrideCategory : null,
        override_score: action === 'override' ? parseFloat(overrideScore) : null,
        notes: notes || (action === 'confirm' ? 'Safety officer confirmed model evaluation.' : 'Officer classification override.')
      });
      onClose();
    } catch (err) {
      alert(`Review submission failed: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-3xl w-full max-w-xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-slate-200 text-slate-800 border border-slate-300 flex items-center justify-center shadow-xs">
              <UserCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-black text-slate-900">
                Formal HSE Officer Review & Sign-Off
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Incident Ref: <span className="font-mono text-slate-900 font-bold">{incident.id}</span> ({incident.facility})
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-900 p-1.5 rounded-xl bg-white border border-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          {/* Current AI Verdict Snapshot */}
          <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200 text-xs shadow-2xs">
            <span className="text-slate-500 uppercase tracking-wider font-bold block text-[10px] mb-1">
              Current Model Verdict
            </span>
            <div className="flex items-center justify-between">
              <div>
                <span className="font-black text-slate-900">{incident.sif_potential_category}</span>
                <span className="text-slate-600 ml-2 font-mono font-bold">(Score: {incident.stage_b_score.toFixed(2)})</span>
              </div>
              <span className="text-amber-800 font-bold bg-amber-100 px-2.5 py-0.5 rounded-md border border-amber-300">
                {incident.iogp_rules?.[0] || "General"}
              </span>
            </div>
          </div>

          {/* Reviewer Name */}
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">
              Reviewer / Safety Officer Name
            </label>
            <input
              type="text"
              required
              value={reviewerName}
              onChange={(e) => setReviewerName(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-xs font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-500/30 focus:border-slate-500"
            />
          </div>

          {/* Action Choice: Confirm or Override */}
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-2">
              Decision Action
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setAction('confirm')}
                className={`p-3.5 rounded-2xl border text-xs font-black flex flex-col items-center space-y-1.5 transition ${
                  action === 'confirm'
                    ? 'bg-blue-50 border-blue-500 text-blue-900 ring-2 ring-blue-300 shadow-xs'
                    : 'bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100'
                }`}
              >
                <Check className="w-5 h-5 text-blue-600" />
                <span>Confirm Model Verdict</span>
              </button>
              <button
                type="button"
                onClick={() => setAction('override')}
                className={`p-3.5 rounded-2xl border text-xs font-black flex flex-col items-center space-y-1.5 transition ${
                  action === 'override'
                    ? 'bg-amber-50 border-amber-500 text-slate-900 ring-2 ring-amber-300 shadow-xs'
                    : 'bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100'
                }`}
              >
                <ArrowUpRight className="w-5 h-5 text-slate-600" />
                <span>Override Classification</span>
              </button>
            </div>
          </div>

          {/* Override Details */}
          {action === 'override' && (
            <div className="bg-slate-50 border border-slate-300 p-4.5 rounded-2xl space-y-4 shadow-2xs">
              <div className="flex items-start space-x-2 text-xs text-slate-900 font-medium">
                <Database className="w-4 h-4 text-cyan-700 shrink-0 mt-0.5" />
                <span>
                  <strong>Live Vector Feedback:</strong> Overriding writes this incident and rationale directly into the versioned Exemplar Vector Store, improving future Stage B similarity retrieval without retraining!
                </span>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-800 mb-1">
                  Adjust SIF Category
                </label>
                <select
                  value={overrideCategory}
                  onChange={(e) => {
                    setOverrideCategory(e.target.value);
                    if (e.target.value === 'High SIF Potential' && overrideScore < 0.7) {
                      setOverrideScore(0.85);
                    } else if (e.target.value === 'Medium SIF Potential') {
                      setOverrideScore(0.55);
                    } else if (e.target.value === 'Low / Non-SIF') {
                      setOverrideScore(0.15);
                    }
                  }}
                  className="w-full bg-white border border-slate-300 text-slate-900 font-semibold rounded-xl px-3.5 py-2 text-xs focus:outline-none focus:border-amber-500"
                >
                  <option value="High SIF Potential">High SIF Potential</option>
                  <option value="Medium SIF Potential">Medium SIF Potential</option>
                  <option value="Low / Non-SIF">Low / Non-SIF</option>
                </select>
              </div>

              <div>
                <div className="flex justify-between text-xs text-slate-700 font-bold mb-1">
                  <span>Calibrated Score</span>
                  <span className="font-mono font-black text-amber-800">{parseFloat(overrideScore).toFixed(2)}</span>
                </div>
                <input
                  type="range"
                  min="0.05"
                  max="0.99"
                  step="0.01"
                  value={overrideScore}
                  onChange={(e) => setOverrideScore(e.target.value)}
                  className="w-full accent-slate-700 cursor-pointer"
                />
              </div>
            </div>
          )}

          {/* Rationale & Notes */}
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">
              Officer Rationale / Justification Notes
            </label>
            <textarea
              rows={3}
              required={action === 'override'}
              placeholder={action === 'override' ? "Explain why energy level or barrier degradation dictates this change..." : "Optional verification comments..."}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-xs font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-500/30 focus:border-slate-500"
            />
          </div>

          {/* Submit Buttons */}
          <div className="flex items-center justify-end space-x-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-bold text-slate-500 hover:text-slate-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs shadow-md shadow-amber-500/20 transition disabled:opacity-50"
            >
              {isSubmitting ? "Submitting..." : action === "override" ? "Apply Override & Update Vector Store" : "Confirm Verdict"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
