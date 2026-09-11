import React, { useEffect, useState } from 'react';
import { X, Database, ShieldAlert, Sparkles, CheckCircle2, UserCheck } from 'lucide-react';
import { fetchExemplars } from '../api';

export default function ExemplarStoreModal({ onClose }) {
  const [exemplars, setExemplars] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadExemplars();
  }, []);

  const loadExemplars = async () => {
    try {
      setLoading(true);
      const data = await fetchExemplars();
      setExemplars(data);
    } catch (err) {
      console.error("Failed to load exemplars", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-950 border border-slate-800 rounded-2xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 bg-slate-900/80 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-indigo-950/30 text-indigo-600 border border-indigo-200 shadow-none">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-100">
                Layer 5: Versioned Exemplar Vector Store
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                FAISS Dense Index · Powering Stage A & Stage B in-context few-shot learning
              </p>
            </div>
          </div>
          <button 
            onClick={onClose} 
            className="p-2 rounded-lg text-slate-400 hover:text-slate-300 hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-4">
          <div className="bg-indigo-950/30/60 border border-indigo-200/80 rounded-xl p-4 text-xs text-slate-300 leading-relaxed shadow-none">
            <strong className="text-indigo-300 font-semibold">Continuous Decision-Support Architecture:</strong> Human safety officer overrides write directly into this index with active versioning. Stage B retrieves the top semantic nearest-neighbors to guide classification rationales without requiring full retraining.
          </div>

          {loading ? (
            <div className="p-12 text-center text-slate-400 text-xs font-medium">Loading vector store exemplars...</div>
          ) : (
            <div className="space-y-3">
              {exemplars.map((item, idx) => {
                const isOverride = item.source === "human_override";
                const isHigh = item.sif_potential === "High";

                return (
                  <div 
                    key={item.id || idx}
                    className={`p-4 rounded-xl border text-xs transition ${
                      isOverride 
                        ? 'bg-purple-50/60 border-purple-200 shadow-none' 
                        : 'bg-slate-950 border-slate-800 hover:border-slate-700 shadow-none'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2.5 flex-wrap gap-2">
                      <div className="flex items-center space-x-2">
                        <span className="font-mono font-bold text-indigo-600 bg-indigo-950/30 px-2 py-0.5 rounded border border-indigo-100">{item.id}</span>
                        <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                          isHigh ? 'bg-red-950/30 text-red-400 border border-red-200' : 'bg-emerald-950/30 text-emerald-700 border border-emerald-200'
                        }`}>
                          {item.sif_potential} SIF ({item.sif_score})
                        </span>
                        <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-800 font-medium">
                          {item.iogp_rule}
                        </span>
                      </div>
                      <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${
                        isOverride 
                          ? 'bg-purple-100 text-purple-800 border border-purple-200' 
                          : 'bg-slate-800 text-slate-400 border border-slate-800'
                      }`}>
                        {isOverride ? "Human-in-the-Loop Override" : "Curated Exemplar"}
                      </span>
                    </div>

                    <p className="text-slate-200 font-sans leading-relaxed mb-3">
                      {item.text}
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] text-slate-400 bg-slate-900 p-3 rounded-lg border border-slate-800/80">
                      <div>
                        <span className="text-slate-400 font-medium">Energy Source:</span> <span className="text-amber-400 font-semibold">{item.energy_source}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 font-medium">Barrier:</span> <span className="text-slate-300 font-medium">{item.barrier_status}</span>
                      </div>
                      <div className="col-span-full pt-1 border-t border-slate-800/60">
                        <span className="text-slate-400 font-medium">Rubric Rationale:</span> <span className="text-slate-300 italic">{item.rationale}</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
