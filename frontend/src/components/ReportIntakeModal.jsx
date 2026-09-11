import React, { useState } from 'react';
import { X, Upload, FileText, CheckCircle2, Sparkles, AlertCircle } from 'lucide-react';

const SAMPLE_TEMPLATES = [
  {
    title: "High SIF: Full Kannada (Dropped Object)",
    facility: "ONGC Hazira Rig",
    location: "Hazira Offshore",
    outcome: "Near Miss / No Injury",
    text: "ಡ್ರಿಲ್ಲಿಂಗ್ ಮಾಡುವಾಗ, ಮಂಕಿ ಬೋರ್ಡ್‌ನಿಂದ 500kg ಭಾರವಾದ ಡ್ರಿಲ್ ಕಾಲರ್ ಕೆಳಗೆ ಬಿತ್ತು. ಕೆಳಗಿದ್ದ ಖಲಾಸಿ ಸ್ವಲ್ಪದರಲ್ಲಿಯೇ ತಪ್ಪಿಸಿಕೊಂಡ. ಯಾರಿಗೂ ಗಾಯವಾಗಿಲ್ಲ, ಆದರೆ ಇದು ದೊಡ್ಡ ಅಪಘಾತವಾಗುವ ಸಾಧ್ಯತೆ ಇತ್ತು."
  },
  {
    title: "High SIF: Full Assamese (Confined Space)",
    facility: "Moran Production Station",
    location: "Upper Assam",
    outcome: "First Aid",
    text: "মৰাণ জিজিএছত, এজন ঠিকা কৰ্মীয়ে পাৰ্মিট নোহোৱাকৈ ৩ মিটাৰ দ গাঁতত সোমাইছিল। বিষাক্ত গেছৰ বাবে তাৰ মূৰ ঘূৰাইছিল আৰু সি লৰালৰিকৈ ওলাই আহিল। সি অলপৰ বাবে বাচি গ'ল কিন্তু আঁঠুত অকণমান দুখ পালে।"
  },
  {
    title: "Low SIF: Routine Slip/Trip",
    facility: "Administrative Building",
    location: "Duliajan HQ",
    outcome: "First Aid",
    text: "An executive clerk received a minor paper cut while unboxing newly delivered audit ledger files. Antiseptic wipe applied."
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
      <div className="bg-slate-950 border border-slate-700 rounded-3xl w-full max-w-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-slate-800 bg-slate-900 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-sky-900/40 text-sky-400 border border-sky-800/50 flex items-center justify-center shadow-none">
              <Upload className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-black text-slate-100">
                Layer 1: Safety Incident Intake Feed
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Automatic ingestion into two-stage classification pipeline
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-100 p-1.5 rounded-xl bg-slate-950 border border-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          {/* Quick Pre-fill Templates */}
          <div>
            <span className="text-xs font-bold text-slate-300 uppercase tracking-wider block mb-2">
              Quick Test Templates (Click to Populate)
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              {SAMPLE_TEMPLATES.map((tpl, i) => (
                <button
                  type="button"
                  key={i}
                  onClick={() => applyTemplate(tpl)}
                  className="p-3 text-left rounded-xl bg-slate-900 border border-slate-800 hover:border-amber-400 hover:bg-amber-950/30/50 text-slate-200 text-xs transition shadow-none"
                >
                  <span className="font-bold text-slate-100 block truncate">{tpl.title}</span>
                  <span className="text-[10px] text-slate-500 block font-medium mt-0.5">{tpl.outcome}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1">
                Asset / Rig Facility
              </label>
              <input
                type="text"
                required
                value={facility}
                onChange={(e) => setFacility(e.target.value)}
                placeholder="e.g. Rig OIL-04"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2 text-xs font-semibold text-slate-100 focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1">
                Field Location
              </label>
              <input
                type="text"
                required
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="e.g. Moran Field"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2 text-xs font-semibold text-slate-100 focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1">
                Reported Actual Outcome
              </label>
              <select
                value={outcome}
                onChange={(e) => setOutcome(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 text-slate-100 font-semibold rounded-xl px-3.5 py-2 text-xs focus:outline-none focus:border-amber-500"
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
              <label className="block text-xs font-bold text-slate-300">
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
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs font-medium text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500 font-mono leading-relaxed"
            />
          </div>

          {/* Buttons */}
          <div className="flex items-center justify-end space-x-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-bold text-slate-500 hover:text-slate-200"
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
