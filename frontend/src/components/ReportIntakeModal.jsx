import React, { useState } from 'react';
import { X, Upload, FileText, CheckCircle2, Sparkles, AlertCircle } from 'lucide-react';

const SAMPLE_TEMPLATES = [
  {
    title: "Near-Miss Dropped Bushing (0 Injury)",
    facility: "Rig OIL-04",
    location: "Moran Field",
    outcome: "Near Miss / No Injury",
    text: "During tripping out at Rig OIL-04, the 85 kg Kelly bushing detached from the hoist hook at 14 meters elevation and crashed down onto the rig floor drill collar rack. The khalasi bach goli [roughneck narrowly escaped] by stepping backwards 2 seconds earlier. Hoist safety latch pin was sheared. Zero injury."
  },
  {
    title: "H2S Cellar Pit Entry (0 Injury)",
    facility: "Moran Production Station",
    location: "Moran",
    outcome: "Near Miss / No Injury",
    text: "At Moran GGS cellar pit, a thekedaar worker entered the 3.5m deep chatai without obtaining a valid PTW or conducting an atmospheric gas test with explosimeter. Felt dizzy from H2S hawa and scrambled out. Standby sentry and SCBA were absent. Zero reported injury."
  },
  {
    title: "Routine Office Slip (Reported First Aid)",
    facility: "Administrative Building",
    location: "Duliajan Headquarters",
    outcome: "First Aid",
    text: "An executive clerk in the Finance & Accounts section received a minor 1 cm paper cut on the left index finger while unboxing newly delivered audit ledger files. Antiseptic wipe and adhesive bandage applied by camp first aider."
  }
];

export default function ReportIntakeModal({ onClose, onReportIngested }) {
  const [facility, setFacility] = useState('Rig OIL-04');
  const [location, setLocation] = useState('Moran Field');
  const [outcome, setOutcome] = useState('Near Miss / No Injury');
  const [rawText, setRawText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const applyTemplate = (tpl) => {
    setFacility(tpl.facility);
    setLocation(tpl.location);
    setOutcome(tpl.outcome);
    setRawText(tpl.text);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!rawText.trim()) return;
    setIsSubmitting(true);
    try {
      await onReportIngested({
        facility,
        location,
        actual_injury_severity: outcome,
        raw_text: rawText
      });
      onClose();
    } catch (err) {
      alert(`Intake failed: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-3xl w-full max-w-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-sky-100 text-sky-800 border border-sky-300 flex items-center justify-center shadow-xs">
              <Upload className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-black text-slate-900">
                Layer 1: Safety Incident Intake Feed
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Automatic ingestion into two-stage classification pipeline
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-900 p-1.5 rounded-xl bg-white border border-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          {/* Quick Pre-fill Templates */}
          <div>
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider block mb-2">
              Quick Test Templates (Click to Populate)
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              {SAMPLE_TEMPLATES.map((tpl, i) => (
                <button
                  type="button"
                  key={i}
                  onClick={() => applyTemplate(tpl)}
                  className="p-3 text-left rounded-xl bg-slate-50 border border-slate-200 hover:border-amber-400 hover:bg-amber-50/50 text-slate-800 text-xs transition shadow-2xs"
                >
                  <span className="font-bold text-slate-900 block truncate">{tpl.title}</span>
                  <span className="text-[10px] text-slate-500 block font-medium mt-0.5">{tpl.outcome}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Asset / Rig Facility
              </label>
              <input
                type="text"
                required
                value={facility}
                onChange={(e) => setFacility(e.target.value)}
                placeholder="e.g. Rig OIL-04"
                className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-xs font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Field Location
              </label>
              <input
                type="text"
                required
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="e.g. Moran Field"
                className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-xs font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Reported Actual Outcome
              </label>
              <select
                value={outcome}
                onChange={(e) => setOutcome(e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 text-slate-900 font-semibold rounded-xl px-3.5 py-2 text-xs focus:outline-none focus:border-amber-500"
              >
                <option value="Near Miss / No Injury">Near Miss / No Injury</option>
                <option value="First Aid">First Aid</option>
                <option value="Medical Treatment Case">Medical Treatment Case</option>
                <option value="Lost Time Injury">Lost Time Injury</option>
                <option value="Fatality">Fatality</option>
              </select>
            </div>
          </div>

          {/* Incident Text */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="block text-xs font-bold text-slate-700">
                Incident Description Text (Field Narrative)
              </label>
              <span className="text-[10px] text-purple-700 font-bold bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                Supports English, Assamese & Hindi field jargon
              </span>
            </div>
            <textarea
              rows={5}
              required
              placeholder="Describe incident: operations in progress, equipment, energy sources, barriers, and line of fire..."
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500 font-mono leading-relaxed"
            />
          </div>

          {/* Buttons */}
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
              disabled={isSubmitting || !rawText.trim()}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-500 hover:to-blue-500 text-white font-black text-xs shadow-md shadow-sky-500/20 transition disabled:opacity-50 flex items-center space-x-1.5"
            >
              <Upload className="w-4 h-4" />
              <span>{isSubmitting ? "Processing Through Pipeline..." : "Submit to Pipeline"}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
