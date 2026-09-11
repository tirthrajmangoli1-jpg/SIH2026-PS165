import React from 'react';
import { 
  ShieldAlert, Activity, Database, Sparkles, RefreshCw, Upload, 
  BarChart3, ListFilter, ShieldCheck, Radio, Globe, Languages 
} from 'lucide-react';

export default function Header({ 
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
    <header className="border-b border-slate-200 bg-white shadow-sm sticky top-0 z-40">
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
                <span className="text-[10px] uppercase font-mono font-bold tracking-wider px-2 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-300">
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
            <div className="flex items-center bg-slate-50 border border-slate-300 hover:border-slate-400 rounded-lg px-2.5 py-1.5 text-xs shadow-xs transition">
              <Globe className="w-3.5 h-3.5 text-cyan-600 mr-2 shrink-0" />
              <select
                value={selectedDataset}
                onChange={(e) => onSelectDataset(e.target.value)}
                disabled={isLoading}
                className="bg-transparent text-slate-800 font-semibold text-xs focus:outline-none cursor-pointer max-w-[240px] md:max-w-[320px] truncate"
              >
                {availableDatasets.map((ds) => (
                  <option key={ds.key} value={ds.key} className="bg-white text-slate-800">
                    {ds.title} ({ds.count} logs)
                  </option>
                ))}
              </select>
            </div>

            {/* Live Streaming Telemetry Pulse Button */}
            <button
              onClick={onToggleLiveStream}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold flex items-center space-x-1.5 border transition shadow-xs ${
                isLiveStreaming 
                  ? 'bg-emerald-100 border-emerald-400 text-emerald-800 animate-pulse' 
                  : 'bg-slate-50 border-slate-300 text-slate-700 hover:bg-slate-100 hover:text-slate-900'
              }`}
              title="Toggle Simulated Live Field Telemetry Stream"
            >
              <Radio className={`w-3.5 h-3.5 ${isLiveStreaming ? 'text-emerald-600 animate-spin' : 'text-slate-500'}`} />
              <span>{isLiveStreaming ? 'LIVE STREAMING' : 'START TELEMETRY'}</span>
            </button>
          </div>

          {/* Quick Metrics Bar */}
          <div className="hidden xl:flex items-center space-x-4 text-xs bg-slate-100/90 py-1.5 px-3.5 rounded-lg border border-slate-200 shrink-0">
            <div className="flex items-center space-x-1.5">
              <span className="text-slate-500 font-medium">Total Reports:</span>
              <span className="font-mono font-black text-slate-800">{stats.total}</span>
            </div>
            <div className="w-px h-3.5 bg-slate-300" />
            <div className="flex items-center space-x-1.5">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
              <span className="text-red-700 font-bold">High SIF:</span>
              <span className="font-mono font-black text-red-700 bg-red-100 px-1.5 py-0.2 rounded">{stats.highSif}</span>
            </div>
            <div className="w-px h-3.5 bg-slate-300" />
            <div className="flex items-center space-x-1.5">
              <span className="text-amber-700 font-bold">Zero-Injury Precursors:</span>
              <span className="font-mono font-black text-amber-800 bg-amber-100 px-1.5 py-0.2 rounded">{stats.zeroInjurySif}</span>
            </div>
          </div>

          {/* Navigation & Action Controls */}
          <div className="flex items-center space-x-2 shrink-0 flex-wrap">
            {/* Tab Navigation */}
            <nav className="flex items-center bg-slate-100 p-1 rounded-lg border border-slate-200 mr-1">
              <button
                onClick={() => setActiveTab('triage')}
                className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition ${
                  activeTab === 'triage'
                    ? 'bg-amber-500 text-slate-950 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
                }`}
              >
                <ListFilter className="w-3.5 h-3.5" />
                <span>Triage Feed</span>
              </button>
              <button
                onClick={() => setActiveTab('patterns')}
                className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition ${
                  activeTab === 'patterns'
                    ? 'bg-amber-500 text-slate-950 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
                }`}
              >
                <BarChart3 className="w-3.5 h-3.5" />
                <span>Pattern Radar</span>
              </button>
            </nav>

            {/* Industry Parameters & AI Training Hub Button */}
            <button
              onClick={onOpenTrainingHub}
              title="Industry Standards & AI Model Calibration Hub"
              className="px-3 py-1.5 rounded-lg border border-amber-300 bg-amber-50 hover:bg-amber-100 text-amber-900 font-bold text-xs flex items-center space-x-1.5 transition shadow-xs"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-600" />
              <span>AI Training & Standards</span>
            </button>

            {/* NLP Translation Log Button */}
            <button
              onClick={onOpenSecurityVault}
              title="View Regional Language to English Translation Pipeline"
              className="px-3 py-1.5 rounded-lg border border-indigo-300 bg-indigo-50 hover:bg-indigo-100 text-indigo-800 font-bold text-xs flex items-center space-x-1.5 transition shadow-xs"
            >
              <Languages className="w-3.5 h-3.5 text-indigo-600" />
              <span>NLP Intake Log</span>
            </button>

            {/* Vector Store Exemplar Inspector */}
            <button
              onClick={onOpenExemplars}
              title="View Versioned Exemplar Store"
              className="px-2.5 py-1.5 rounded-lg border border-slate-300 bg-slate-50 hover:bg-slate-100 text-slate-700 font-semibold text-xs flex items-center space-x-1.5 transition shadow-xs"
            >
              <Database className="w-3.5 h-3.5 text-cyan-600" />
              <span className="hidden sm:inline">Vector Store</span>
            </button>

            {/* Intake Report Button */}
            <button
              onClick={onOpenIntake}
              className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-500 hover:to-blue-500 text-white font-bold text-xs flex items-center space-x-1.5 shadow-sm shadow-blue-500/20 transition"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>Intake</span>
            </button>

            {/* Reset Button */}
            <button
              onClick={onResetDemo}
              disabled={isLoading}
              title="Reset Database to Calibrated Demo Dataset"
              className="p-1.5 rounded-lg border border-slate-300 bg-slate-50 hover:bg-slate-100 text-slate-600 hover:text-slate-900 transition shadow-xs"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-amber-600' : ''}`} />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
