import React from 'react';
import { X, Languages, FileText, ArrowRight } from 'lucide-react';

export default function IntakeLogModal({ incidents, onClose }) {
  // Only show incidents that actually have code-switching detected
  const translatedIncidents = incidents.filter(
    (inc) => inc.detected_codeswitch && inc.detected_codeswitch.length > 0
  );

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-3xl w-full max-w-4xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-6 border-b border-slate-200 bg-slate-50 flex items-center justify-between shrink-0">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-indigo-100 text-indigo-800 border border-indigo-300 flex items-center justify-center shadow-xs">
              <Languages className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-black text-slate-900">
                NLP Pipeline Translation Log
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Live view of Regional Language (Kannada/Assamese) to English translation
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-900 p-1.5 rounded-xl bg-white border border-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* List Body */}
        <div className="p-6 overflow-y-auto bg-slate-50 flex-1 space-y-4">
          {translatedIncidents.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-12 h-12 mx-auto text-slate-300 mb-4" />
              <p className="text-slate-500 text-sm font-medium">No regional language incidents detected yet.</p>
              <p className="text-slate-400 text-xs mt-1">Submit a report using Kannada or Assamese to see the NLP translation here.</p>
            </div>
          ) : (
            translatedIncidents.map((inc) => (
              <div key={inc.id} className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
                <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                  <span className="text-xs font-bold text-slate-800">
                    ID: <span className="font-mono text-indigo-700">{inc.id}</span>
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-800 border border-indigo-200">
                    Code-Switching Detected ({inc.detected_codeswitch.length} terms)
                  </span>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Original */}
                  <div className="bg-slate-50 border border-slate-200 rounded-lg p-3">
                    <span className="text-[10px] uppercase font-black tracking-wider text-slate-500 block mb-1.5">
                      Original Field Input (Regional Language)
                    </span>
                    <p className="text-xs text-slate-700 font-medium leading-relaxed italic">
                      "{inc.raw_text}"
                    </p>
                  </div>

                  {/* Translated */}
                  <div className="bg-blue-50/50 border border-blue-200 rounded-lg p-3 relative">
                    <div className="hidden md:flex absolute -left-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-white border border-slate-200 rounded-full items-center justify-center shadow-sm z-10">
                      <ArrowRight className="w-3 h-3 text-slate-400" />
                    </div>
                    <span className="text-[10px] uppercase font-black tracking-wider text-blue-700 block mb-1.5 flex items-center space-x-1.5">
                      <Languages className="w-3 h-3" />
                      <span>NLP Translated Output (English)</span>
                    </span>
                    <p className="text-xs text-slate-900 font-semibold leading-relaxed">
                      "{inc.normalized_text}"
                    </p>
                  </div>
                </div>
                
                {/* Dictionary matches */}
                <div className="mt-3 flex flex-wrap gap-2 pt-3 border-t border-slate-100">
                  <span className="text-[10px] text-slate-500 font-bold mt-1">Translations Applied:</span>
                  {inc.detected_codeswitch.map((term, i) => (
                    <span key={i} className="text-[10px] font-mono font-bold bg-slate-100 border border-slate-200 text-slate-700 px-2 py-1 rounded">
                      <span className="text-red-500">{term.original_phrase}</span> 
                      <span className="mx-1 text-slate-400">→</span> 
                      <span className="text-emerald-600">{term.normalized_meaning}</span>
                    </span>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
