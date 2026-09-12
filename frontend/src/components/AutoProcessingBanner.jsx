import React from 'react';
import { CheckCircle2, Cpu, AlertCircle } from 'lucide-react';

export default function AutoProcessingBanner({ latestProcessed }) {
  if (!latestProcessed) {
    return null;
  }

  const stages = [
    {
      name: "1. Intake & Normalization",
      detail: latestProcessed.detected_codeswitch?.length > 0 
        ? `Code-Switch: ${latestProcessed.detected_codeswitch[0].original_phrase}`
        : "Domain Lexicon Applied",
      done: true,
      color: "border-sky-800/50 bg-sky-950/30 text-sky-300"
    },
    {
      name: "2. Feature Extraction",
      detail: latestProcessed.hazard_type || "Energy & Barrier Features",
      done: true,
      color: "border-indigo-800/50 bg-indigo-950/30 text-indigo-300"
    },
    {
      name: "3. Stage A Pre-Filter",
      detail: latestProcessed.stage_a_flagged ? "Flagged (High Recall)" : "Screened Out",
      done: true,
      color: latestProcessed.stage_a_flagged 
        ? "border-amber-800/50 bg-amber-950/30 text-amber-300 font-bold" 
        : "border-slate-800 bg-slate-900 text-slate-400"
    },
    {
      name: "4. Stage B Rubric LLM",
      detail: latestProcessed.stage_b_executed 
        ? `Score: ${latestProcessed.stage_b_score.toFixed(2)} (${latestProcessed.sif_potential_category})` 
        : "Bypassed (Not Flagged)",
      done: latestProcessed.stage_b_executed,
      color: latestProcessed.sif_potential_category === "High SIF Potential"
        ? "border-red-800/50 bg-red-950/30 text-red-300 font-extrabold"
        : "border-emerald-800/50 bg-emerald-950/30 text-emerald-300 font-bold"
    }
  ];

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-2xl p-5 mb-6 shadow-none">
      <div className="flex flex-wrap items-center justify-between mb-3.5 gap-2">
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 rounded-lg bg-amber-900/40 border border-amber-800/50 flex items-center justify-center text-slate-400">
            <Cpu className="w-3.5 h-3.5" />
          </div>
          <span className="text-xs font-black text-slate-200 uppercase tracking-wider">
            Pipeline Execution Monitor
          </span>
          <span className="font-mono text-xs font-bold text-slate-400 bg-amber-950/30 px-2 py-0.5 rounded border border-amber-800/50">
            {latestProcessed.id}
          </span>
        </div>
        <span className="text-xs text-slate-500 font-medium">
          Target Asset: <strong className="text-slate-200 font-bold">{latestProcessed.facility}</strong> ({latestProcessed.location})
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        {stages.map((stage, idx) => (
          <div 
            key={idx} 
            className={`flex items-start space-x-3 p-3.5 rounded-xl border ${stage.color} shadow-none transition`}
          >
            <div className="mt-0.5">
              {stage.done ? (
                <CheckCircle2 className="w-4 h-4 text-current shrink-0" />
              ) : (
                <AlertCircle className="w-4 h-4 text-slate-400 shrink-0" />
              )}
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-black text-slate-100 truncate">{stage.name}</p>
              <p className="text-[11px] text-slate-400 truncate mt-0.5 font-medium">{stage.detail}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
