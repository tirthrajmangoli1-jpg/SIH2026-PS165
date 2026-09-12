import React from 'react';
import { 
  ShieldAlert, Activity, Database, Sparkles, RefreshCw, Upload, 
  BarChart3, ListFilter, ShieldCheck, Radio, Globe, Languages 
} from 'lucide-react';

export default function Header({
  onOpenReviewHistory, 
  activeTab, 
  setActiveTab, 
  stats, 
  onOpenIntake, 
  onResetDemo, 
  onOpenExemplars,
  onOpenSecurityVault,
  onOpenTrainingHub,
  selectedDataset,
  onSelectDataset,
  availableDatasets = [],
  isLiveStreaming,
  onToggleLiveStream,
  isLoading 
}) {
  return (
    <header className="border-b border-slate-800 bg-slate-950 shadow-none sticky top-0 z-40">
      <div className="max-w-[1700px] w-full mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-wrap items-center justify-between py-2.5 gap-3 min-h-[64px]">
          {/* Brand & Title */}
          <div className="flex items-center space-x-3 shrink-0">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br bg-slate-800 flex items-center justify-center shadow-md ">
              <ShieldAlert className="w-6 h-6 text-white font-black" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-black text-lg tracking-tight bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
                  OIL SIF-SENTINEL
                </span>
                <span className="text-[10px] uppercase font-mono font-bold tracking-wider px-2 py-0.5 rounded bg-amber-900/40 text-amber-400 border border-amber-800/50">
                  SIH 2026 · PS 165
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">
                Oil India Limited · Fatality Precursor Surveillance Command Center
              </p>
            </div>
          </div>

          {/* Dataset Switcher & Live Stream Simulator */}
          <div className="flex items-center space-x-2 flex-wrap shrink-0">
            {/* Multi-Source Dataset Dropdown */}
            <div className="flex items-center bg-slate-900 border border-slate-700 hover:border-slate-400 rounded-lg px-2.5 py-1.5 text-xs shadow-none transition">
              <Globe className="w-3.5 h-3.5 text-cyan-600 mr-2 shrink-0" />
              <select
                value={selectedDataset}
                onChange={(e) => onSelectDataset(e.target.value)}
                disabled={isLoading}
                className="bg-transparent text-slate-200 font-semibold text-xs focus:outline-none cursor-pointer max-w-[240px] md:max-w-[320px] truncate"
              >
                {availableDatasets.map((ds) => (
                  <option key={ds.key} value={ds.key} className="bg-slate-950 text-slate-200">
                    {ds.title} ({ds.count} logs)
                  </option>
                ))}
              </select>
            </div>

            {/* Live Streaming Telemetry Pulse Button */}
            <button
              onClick={onToggleLiveStream}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold flex items-center space-x-1.5 border transition shadow-none ${
                isLiveStreaming 
                  ? 'bg-emerald-900/40 border-emerald-400 text-emerald-400 animate-pulse' 
                  : 'bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-slate-100'
              }`}
              title="Toggle Simulated Live Field Telemetry Stream"
            >
              <Radio className={`w-3.5 h-3.5 ${isLiveStreaming ? 'text-emerald-600 animate-spin' : 'text-slate-500'}`} />
              <span>{isLiveStreaming ? 'LIVE STREAMING' : 'START TELEMETRY'}</span>
            </button>
          </div>

          {/* Quick Metrics Bar */}
          <div className="hidden xl:flex items-center space-x-4 text-xs bg-slate-800/90 py-1.5 px-3.5 rounded-lg border border-slate-800 shrink-0">
            <div className="flex items-center space-x-1.5">
              <span className="text-slate-500 font-medium">Total Reports:</span>
              <span className="font-mono font-black text-slate-200">{stats.total}</span>
            </div>
            <div className="w-px h-3.5 bg-slate-300" />
            <div className="flex items-center space-x-1.5">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
              <span className="text-red-400 font-bold">High SIF:</span>
              <span className="font-mono font-black text-red-400 bg-red-900/40 px-1.5 py-0.2 rounded">{stats.highSif}</span>
            </div>
            <div className="w-px h-3.5 bg-slate-300" />
            <div className="flex items-center space-x-1.5">
              <span className="text-amber-400 font-bold">Zero-Injury Precursors:</span>
              <span className="font-mono font-black text-amber-400 bg-amber-900/40 px-1.5 py-0.2 rounded">{stats.zeroInjurySif}</span>
            </div>
          </div>

          {/* Navigation & Action Controls */}
          <div className="flex items-center space-x-2 shrink-0 flex-wrap">
            {/* Tab Navigation */}
            <nav className="flex items-center bg-slate-800 p-1 rounded-lg border border-slate-800 mr-1">
              <button
                onClick={() => setActiveTab('triage')}
                className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition ${
                  activeTab === 'triage'
                    ? 'bg-slate-800 text-white shadow-none'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                }`}
              >
                <ListFilter className="w-3.5 h-3.5" />
                <span>Triage Feed</span>
              </button>
              <button
                onClick={() => setActiveTab('patterns')}
                className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition ${
                  activeTab === 'patterns'
                    ? 'bg-slate-800 text-white shadow-none'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                }`}
              >
                <BarChart3 className="w-3.5 h-3.5" />
                <span>Pattern Radar</span>
              </button>
            
            {/* Officer Decisions Tab */}
            <button
              onClick={() => setActiveTab('decisions')}
              className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition ${
                activeTab === 'decisions'
                  ? 'bg-slate-800 text-white shadow-none'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Decisions</span>
            </button>

            </nav>

            {/* Industry Parameters & AI Training Hub Button */}
            <button
              onClick={onOpenTrainingHub}
              title="Industry Standards & AI Model Calibration Hub"
              className="px-3 py-1.5 rounded-lg border border-amber-800/50 bg-amber-950/30 hover:bg-amber-900/40 text-amber-300 font-bold text-xs flex items-center space-x-1.5 transition shadow-none"
            >
              <Sparkles className="w-3.5 h-3.5 text-slate-500" />
              <span>AI Training & Standards</span>
            </button>

            {/* NLP Translation Log Button */}
            <button
              onClick={onOpenSecurityVault}
              title="View Regional Language to English Translation Pipeline"
              className="px-3 py-1.5 rounded-lg border border-indigo-800/50 bg-indigo-950/30 hover:bg-indigo-900/40 text-indigo-400 font-bold text-xs flex items-center space-x-1.5 transition shadow-none"
            >
              <Languages className="w-3.5 h-3.5 text-slate-500" />
              <span>NLP Intake Log</span>
            </button>

            

            {/* Intake Report Button */}
            <button
              onClick={onOpenIntake}
              className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-500 hover:to-blue-500 text-white font-bold text-xs flex items-center space-x-1.5 shadow-none shadow-blue-500/20 transition"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>Intake</span>
            </button>

            {/* Reset Button */}
            <button
              onClick={onResetDemo}
              disabled={isLoading}
              title="Reset Database to Calibrated Demo Dataset"
              className="p-1.5 rounded-lg border border-slate-700 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-100 transition shadow-none"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-slate-500' : ''}`} />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
