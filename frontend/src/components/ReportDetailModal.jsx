import React, { useState } from 'react';
import { 
  X, ShieldAlert, Cpu, AlertTriangle, CheckCircle2, UserCheck, 
  Languages, Zap, FileText, Info, Flame, Eye, Lock, ArrowRight, Activity 
} from 'lucide-react';

export default function ReportDetailModal({ incident, onClose, onOpenReview }) {
  const [viewMode, setViewMode] = useState('standard'); // 'standard' | 'saliency_xray' | 'causal_chain'

  if (!incident) return null;

  const isHigh = incident.sif_potential_category === "High SIF Potential";
  const isMedium = incident.sif_potential_category === "Medium SIF Potential";

  // Saliency thermodynamic color generator in bright theme
  const getSaliencyColor = (weight, tag) => {
    if (tag === 'barrier_failure') return 'bg-rose-100 text-rose-900 border-b-2 border-rose-500 font-black';
    if (tag === 'near_miss_indicator') return 'bg-amber-100 text-amber-950 border-b-2 border-amber-500 font-black';
    if (tag === 'energy_source') return 'bg-red-100 text-red-950 border-b-2 border-red-600 font-black';
    if (tag === 'physical_quantity') return 'bg-sky-100 text-sky-950 border-b-2 border-sky-500 font-bold';
    if (tag === 'operational_context') return 'bg-slate-100 text-slate-800 font-medium';
    return 'text-slate-700';
  };

  // Text highlighting logic for driving phrases
  const highlightDrivingPhrases = (text, phrases) => {
    if (!phrases || phrases.length === 0) return text;
    const sorted = [...phrases].filter(p => p && p.length > 2).sort((a, b) => b.length - a.length);
    if (sorted.length === 0) return text;

    const escaped = sorted.map(p => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
    const regex = new RegExp(`(${escaped})`, 'gi');

    const parts = text.split(regex);
    return parts.map((part, i) => {
      const match = sorted.find(p => p.toLowerCase() === part.toLowerCase());
      if (match) {
        return (
          <mark 
            key={i} 
            className="bg-amber-200 text-amber-950 border-b-2 border-amber-500 px-1.5 py-0.5 rounded font-bold cursor-help"
            title="Driving phrase contributing to SIF-potential classification"
          >
            {part}
          </mark>
        );
      }
      return part;
    });
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white border border-slate-300 rounded-3xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Modal Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200 bg-slate-50/80">
          <div className="flex items-center space-x-3.5">
            <div className={`p-2.5 rounded-2xl border ${
              isHigh 
                ? 'bg-rose-100 border-rose-300 text-rose-700' 
                : isMedium 
                ? 'bg-amber-100 border-amber-300 text-amber-700'
                : 'bg-emerald-100 border-emerald-300 text-emerald-700'
            }`}>
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2.5">
                <span className="font-mono text-sm font-black text-slate-900">{incident.id}</span>
                <span className={`px-2.5 py-0.5 rounded-md text-xs font-black ${
                  isHigh 
                    ? 'bg-rose-100 text-rose-800 border border-rose-300' 
                    : isMedium
                    ? 'bg-amber-100 text-amber-900 border border-amber-300'
                    : 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                }`}>
                  {incident.sif_potential_category} (Score: {incident.stage_b_score.toFixed(2)})
                </span>
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
                  {incident.dataset_source || "OIL Upper Assam"}
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium mt-0.5">
                {incident.facility} · {incident.location} · Reported: {incident.date_reported}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => {
                onClose();
                onOpenReview(incident);
              }}
              className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs flex items-center space-x-1.5 transition shadow-sm"
            >
              <UserCheck className="w-4 h-4" />
              <span>Officer Decision</span>
            </button>
            <button 
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-900 hover:bg-slate-100 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* View Mode Switcher Toolbar */}
        <div className="px-6 py-2.5 bg-slate-100/80 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2 text-xs">
          <div className="flex items-center space-x-1.5">
            <button
              onClick={() => setViewMode('standard')}
              className={`px-3 py-1.5 rounded-lg font-bold transition ${
                viewMode === 'standard' 
                  ? 'bg-white text-slate-900 shadow-sm border border-slate-200 font-black' 
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Standard Report View
            </button>
            <button
              onClick={() => setViewMode('saliency_xray')}
              className={`px-3 py-1.5 rounded-lg font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'saliency_xray' 
                  ? 'bg-rose-100 text-rose-900 border border-rose-300 shadow-sm font-black' 
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Flame className="w-3.5 h-3.5 text-rose-600" />
              <span>Thermodynamic Saliency X-Ray</span>
            </button>
            <button
              onClick={() => setViewMode('causal_chain')}
              className={`px-3 py-1.5 rounded-lg font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'causal_chain' 
                  ? 'bg-sky-100 text-sky-900 border border-sky-300 shadow-sm font-black' 
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Activity className="w-3.5 h-3.5 text-sky-600" />
              <span>3-Stage Causal Chain</span>
            </button>
          </div>

          {/* Cryptographic & Merkle Proof Tag */}
          <div className="flex items-center space-x-2 text-xs font-mono font-bold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-300">
            <Lock className="w-3.5 h-3.5 text-emerald-600" />
            <span>Merkle Block #{incident.crypto_metadata?.block_height || 1} Sealed</span>
          </div>
        </div>

        {/* Modal Content */}
        <div className="p-6 overflow-y-auto space-y-6">
          {/* Core Modeling Highlight Notice */}
          <div className="bg-amber-50 border border-amber-300 rounded-2xl p-4.5 flex items-start space-x-3.5 shadow-2xs">
            <Zap className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div className="text-xs text-slate-800 space-y-1">
              <p className="font-black text-amber-900 text-sm">
                Core Modeling Metric: SIF-Potential vs Reported Injury Severity
              </p>
              <p className="text-slate-700 font-medium leading-relaxed">
                Reported Actual Outcome: <strong className="text-slate-900 font-bold">{incident.actual_injury_severity}</strong>. 
                Calculated SIF-Potential: <strong className="text-amber-800 font-bold">{incident.stage_b_score.toFixed(2)} ({incident.sif_potential_category})</strong>.
                {incident.actual_injury_severity === 'Near Miss / No Injury' && isHigh && (
                  <span className="block text-red-700 font-extrabold mt-1">
                    🎯 Weak-Signal Precursor: High energetic capacity was present with degraded barriers. A fatality was averted purely by timing/circumstance.
                  </span>
                )}
              </p>
            </div>
          </div>

          {/* Physical Quantities Badge Bar */}
          {incident.physical_quantities && incident.physical_quantities.length > 0 && (
            <div>
              <h4 className="text-xs font-black uppercase tracking-wider text-slate-700 mb-2.5 flex items-center space-x-1.5">
                <Activity className="w-4 h-4 text-sky-600" />
                <span>Extracted Physical Engineering Quantities</span>
              </h4>
              <div className="flex flex-wrap gap-2.5">
                {incident.physical_quantities.map((q, idx) => (
                  <div key={idx} className="bg-sky-50 border border-sky-300 rounded-xl px-3.5 py-2 flex items-center space-x-2 text-xs text-sky-950 font-mono shadow-2xs">
                    <span className="text-slate-600 font-sans text-xs font-medium">{q.category}:</span>
                    <strong className="text-sky-900 text-sm font-black">{q.raw_string}</strong>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 3-Stage Causal Precursor Chain View */}
          {viewMode === 'causal_chain' && incident.causal_chain && (
            <div className="p-5 rounded-2xl bg-slate-50 border border-sky-300 space-y-4 shadow-xs">
              <div className="flex items-center space-x-2 text-xs font-black text-sky-900 uppercase font-mono">
                <Activity className="w-4 h-4 text-sky-600" />
                <span>3-Stage Neuro-Symbolic Causal Precursor Chain</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
                <div className="p-4 rounded-xl bg-white border border-amber-300 shadow-2xs">
                  <span className="text-[10px] uppercase font-mono font-black text-amber-800 block mb-1.5">
                    1. Root Precursor Trigger
                  </span>
                  <p className="text-xs text-slate-800 font-medium leading-relaxed">
                    {incident.causal_chain.root_precursor || "Initial procedural / physical anomaly"}
                  </p>
                </div>
                <div className="p-4 rounded-xl bg-white border border-rose-300 shadow-2xs">
                  <span className="text-[10px] uppercase font-mono font-black text-rose-800 block mb-1.5">
                    2. Intermediate Barrier Failure
                  </span>
                  <p className="text-xs text-slate-800 font-medium leading-relaxed">
                    {incident.causal_chain.intermediate_barrier_failure || "Engineered defense degraded/bypassed"}
                  </p>
                </div>
                <div className="p-4 rounded-xl bg-white border border-red-300 shadow-2xs">
                  <span className="text-[10px] uppercase font-mono font-black text-red-800 block mb-1.5">
                    3. Credible Catastrophic Consequence
                  </span>
                  <p className="text-xs text-slate-800 font-medium leading-relaxed">
                    {incident.causal_chain.credible_catastrophic_consequence || "Credible fatality prevented by luck"}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Saliency Heatmap X-Ray View */}
          {viewMode === 'saliency_xray' && incident.saliency_heatmap && incident.saliency_heatmap.length > 0 ? (
            <div>
              <div className="flex flex-wrap items-center justify-between mb-2.5 gap-2">
                <h4 className="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center space-x-1.5">
                  <Flame className="w-4 h-4 text-rose-600" />
                  <span>Thermodynamic Attention Saliency (Word-by-Word Risk Weights)</span>
                </h4>
                <div className="flex items-center space-x-2 text-[10px] font-bold">
                  <span className="px-2 py-0.5 rounded bg-red-100 text-red-900 border border-red-300">Energy</span>
                  <span className="px-2 py-0.5 rounded bg-rose-100 text-rose-900 border border-rose-300">Barrier Failure</span>
                  <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-300">Near-Miss</span>
                  <span className="px-2 py-0.5 rounded bg-sky-100 text-sky-900 border border-sky-300">Physical Metric</span>
                </div>
              </div>
              <div className="p-5 rounded-2xl bg-slate-50 border border-rose-200 text-sm leading-loose font-mono flex flex-wrap gap-2 shadow-2xs">
                {incident.saliency_heatmap.map((item, idx) => (
                  <span
                    key={idx}
                    className={`px-2 py-0.5 rounded-md text-xs transition cursor-help ${getSaliencyColor(item.weight, item.tag)}`}
                    title={`Token: "${item.token}" | Saliency Weight: ${item.weight} | Category: ${item.tag}`}
                  >
                    {item.token}
                  </span>
                ))}
              </div>
            </div>
          ) : viewMode === 'standard' && (
            /* Original Incident Text with Rationale Highlighting */
            <div>
              <div className="flex items-center justify-between mb-2.5">
                <h4 className="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center space-x-1.5">
                  <FileText className="w-4 h-4 text-slate-500" />
                  <span>Original Incident Text (Driving Phrases Highlighted)</span>
                </h4>
                <span className="text-[10px] text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-md border border-amber-300 font-bold">
                  Yellow markers = extracted SIF drivers
                </span>
              </div>
              <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 text-sm text-slate-800 leading-relaxed font-sans shadow-2xs">
                {highlightDrivingPhrases(incident.raw_text, incident.key_driving_phrases)}
              </div>
            </div>
          )}

          {/* Model Written Engineering Rationale */}
          <div>
            <h4 className="text-xs font-black uppercase tracking-wider text-slate-700 mb-2 flex items-center space-x-1.5">
              <Cpu className="w-4 h-4 text-amber-600" />
              <span>In-Context LLM Classification Rationale (Stage B)</span>
            </h4>
            <div className="p-4.5 rounded-2xl bg-amber-50/50 border border-slate-200 text-xs text-slate-800 leading-relaxed font-medium">
              <p>{incident.written_rationale}</p>
            </div>
          </div>

          {/* Extracted Structured Features (Layer 3) */}
          <div>
            <h4 className="text-xs font-black uppercase tracking-wider text-slate-700 mb-2.5">
              Extracted Structured Features (Layer 3)
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
              <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                <span className="text-[11px] text-slate-500 block font-semibold">Hazard Category</span>
                <span className="text-xs font-black text-slate-900">{incident.hazard_type || "N/A"}</span>
              </div>
              <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                <span className="text-[11px] text-slate-500 block font-semibold">Energy Source & Capacity</span>
                <span className="text-xs font-black text-amber-800">{incident.energy_source || "N/A"}</span>
              </div>
              <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                <span className="text-[11px] text-slate-500 block font-semibold">Critical Equipment</span>
                <span className="text-xs font-black text-slate-900">{incident.equipment_involved || "N/A"}</span>
              </div>
              <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                <span className="text-[11px] text-slate-500 block font-semibold">Barrier Status</span>
                <span className={`text-xs font-black ${
                  incident.barrier_status?.includes('Failed') || incident.barrier_status?.includes('Missing')
                    ? 'text-red-700' 
                    : 'text-slate-900'
                }`}>
                  {incident.barrier_status || "N/A"}
                </span>
              </div>
            </div>
          </div>

          {/* IOGP Life-Saving Rules */}
          <div>
            <h4 className="text-xs font-black uppercase tracking-wider text-slate-700 mb-2.5">
              Assigned IOGP Life-Saving Rules (9-Rule Reference)
            </h4>
            <div className="flex flex-wrap gap-2.5">
              {incident.iogp_rules && incident.iogp_rules.length > 0 ? (
                incident.iogp_rules.map((rule, idx) => (
                  <div key={idx} className="bg-amber-100 border border-amber-300 rounded-xl px-3.5 py-2 flex items-center space-x-2 text-xs text-amber-950 font-black shadow-2xs">
                    <CheckCircle2 className="w-4 h-4 text-amber-700" />
                    <span>{rule}</span>
                  </div>
                ))
              ) : (
                <span className="text-xs text-slate-400 font-medium">None assigned</span>
              )}
            </div>
          </div>

          {/* Regional Dialect & Code-Switching */}
          {incident.detected_codeswitch && incident.detected_codeswitch.length > 0 && (
            <div>
              <h4 className="text-xs font-black uppercase tracking-wider text-slate-700 mb-2.5 flex items-center space-x-1.5">
                <Languages className="w-4 h-4 text-purple-600" />
                <span>Assam Oilfield Code-Switching Lexicon Normalization</span>
              </h4>
              <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden text-xs shadow-xs">
                <table className="w-full text-left">
                  <thead className="bg-slate-50 text-[10px] uppercase text-slate-600 font-black">
                    <tr>
                      <th className="p-3">Original Field Term</th>
                      <th className="p-3">Language Origin</th>
                      <th className="p-3">Standard Safety Meaning</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {incident.detected_codeswitch.map((item, idx) => (
                      <tr key={idx}>
                        <td className="p-3 font-mono text-purple-700 font-black">{item.original_phrase}</td>
                        <td className="p-3 text-slate-600 font-medium">{item.language_origin}</td>
                        <td className="p-3 text-slate-900 font-bold">{item.normalized_meaning}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* OPSEC Redactions */}
          {incident.opsec_redactions && incident.opsec_redactions.length > 0 && (
            <div className="bg-indigo-50 border border-indigo-200 rounded-2xl p-4.5 text-xs space-y-1 shadow-2xs">
              <span className="text-indigo-900 font-black block flex items-center space-x-1.5">
                <Lock className="w-4 h-4 text-indigo-700" />
                <span>Field Crew OPSEC & Non-Attribution Sanitization</span>
              </span>
              <p className="text-indigo-800 font-medium">
                Identified {incident.opsec_redactions.length} personnel token(s) deterministically masked to protect frontline reporting transparency.
              </p>
            </div>
          )}

          {/* Review Decision Audit Trail */}
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
          )}
        </div>
      </div>
    </div>
  );
}
