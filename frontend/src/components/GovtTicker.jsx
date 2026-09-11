import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function GovtTicker() {
  return (
    <div className="w-full bg-slate-900 text-slate-200 text-[11px] font-medium py-1.5 px-4 flex items-center justify-center space-x-4 border-b border-slate-700">
      <div className="flex items-center space-x-1.5 text-amber-400 font-bold shrink-0">
        <AlertCircle className="w-3.5 h-3.5" />
        <span>OISD LIVE BULLETIN:</span>
      </div>
      <div className="overflow-hidden relative w-full max-w-4xl whitespace-nowrap">
        <div className="animate-[ticker_20s_linear_infinite] inline-block">
          <span className="mx-4">DGMS Alert (Circular 04/2026): Enforce double block & bleed for all high-pressure H2S manifold isolations.</span>
          <span className="mx-4 text-slate-500">•</span>
          <span className="mx-4">OISD-STD-114 Update: Mandatory AI-assisted review for hot work permits in Zone 1 areas.</span>
          <span className="mx-4 text-slate-500">•</span>
          <span className="mx-4">MoPNG Directive: Enhance surveillance on contractor (thekedaar) near-miss reporting compliance.</span>
        </div>
      </div>
    </div>
  );
}
