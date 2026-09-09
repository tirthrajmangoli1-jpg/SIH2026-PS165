import React, { useState } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, Legend, LineChart, Line, CartesianGrid 
} from 'recharts';
import { 
  ShieldAlert, AlertTriangle, Layers, TrendingUp, Sparkles, 
  Building2, Anchor, Activity, CheckCircle2, Flame, Wrench, 
  HardHat, ArrowRight, ShieldCheck, ChevronRight, Grid, Filter
} from 'lucide-react';

const BARRIER_COLORS = {
  'Failed': '#ef4444',
  'Bypassed / Defeated': '#f97316',
  'Missing / None': '#dc2626',
  'Degraded': '#f59e0b',
  'Intact / Effective': '#10b981',
  'Intact / Controlled': '#10b981'
};

export default function PatternDashboard({ patterns, onSelectTheme }) {
  const [rankingTab, setRankingTab] = useState('sites'); // 'sites' or 'activities'
  const [selectedCell, setSelectedCell] = useState(null);

  if (!patterns) {
    return (
      <div className="p-16 text-center text-slate-500 font-medium">
        Loading pattern clustering data...
      </div>
    );
  }

  const { 
    clusters = [], 
    rig_distribution = [], 
    barrier_distribution = [], 
    sif_vs_injury_matrix = [], 
    timeline_trends = [],
    site_density_ranking = [],
    activity_density_ranking = [],
    risk_matrix_5x5 = { energy_levels: [], barrier_levels: [], cells: [] }
  } = patterns;

  // Color generator for 5x5 matrix cells in bright theme
  const getCellBg = (yIdx, xIdx, count) => {
    const risk = (5 - yIdx) * (5 - xIdx); // 1 to 25
    if (count > 0) {
      if (risk >= 16) return 'bg-rose-600 text-white font-black ring-2 ring-rose-300 shadow-md';
      if (risk >= 10) return 'bg-amber-500 text-slate-950 font-black ring-1 ring-amber-300 shadow-xs';
      if (risk >= 6) return 'bg-yellow-400 text-slate-950 font-bold';
      return 'bg-emerald-500 text-white font-bold';
    }
    // Empty cells
    if (risk >= 16) return 'bg-rose-50/80 border-rose-200 text-slate-400';
    if (risk >= 10) return 'bg-amber-50/80 border-amber-200 text-slate-400';
    return 'bg-slate-50 border-slate-200 text-slate-400';
  };

  return (
    <div className="space-y-6">
      {/* Top Banner Explaining Unsupervised Clustering */}
      <div className="bg-gradient-to-r from-amber-50 via-white to-sky-50 border border-slate-200 rounded-2xl p-6 shadow-sm">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2.5">
              <div className="w-8 h-8 rounded-xl bg-amber-500 text-slate-950 flex items-center justify-center font-bold shadow-xs">
                <Layers className="w-4 h-4" />
              </div>
              <h2 className="text-sm font-black text-slate-900 uppercase tracking-wide">
                Layer 6: HDBSCAN Hazard Pattern Surveillance & 5x5 Process Safety Matrix
              </h2>
            </div>
            <p className="text-xs text-slate-600 mt-2 max-w-4xl leading-relaxed font-medium">
              Unsupervised semantic clustering across Oil India Limited's operational assets in Upper Assam and global benchmark databases. 
              Surfaces systemic failure modes and latent precursor clusters across rigs, locations, and time independent of individual report triage.
            </p>
          </div>
          <div className="text-right">
            <span className="text-[10px] text-slate-500 uppercase font-black tracking-wider block">Active Clusters</span>
            <span className="text-3xl font-black text-amber-600">{clusters.length}</span>
          </div>
        </div>
      </div>

      {/* Cluster Theme Cards */}
      <div>
        <h3 className="text-xs font-black text-slate-700 uppercase tracking-wider mb-3.5">
          Surfaced Hazard Clusters (Aggregated by Semantic Embedding)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {clusters.map((cluster, idx) => (
            <div 
              key={idx}
              className="bg-white border border-slate-200 hover:border-amber-400 hover:shadow-md rounded-2xl p-5 transition shadow-xs flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between">
                  <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
                    Cluster #{cluster.cluster_id >= 0 ? cluster.cluster_id : 'Misc'}
                  </span>
                  {cluster.high_sif_count > 0 && (
                    <span className="text-[10px] font-black px-2.5 py-0.5 rounded-md bg-rose-100 text-rose-800 border border-rose-300">
                      {cluster.high_sif_count} High SIF
                    </span>
                  )}
                </div>
                <h4 className="font-black text-sm text-slate-900 mt-2.5 leading-snug">
                  {cluster.theme_name}
                </h4>
                <p className="text-xs text-amber-700 font-bold mt-1.5 flex items-center space-x-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Dominant Rule: {cluster.dominant_iogp_rule}</span>
                </p>
              </div>

              <div className="mt-4 pt-3.5 border-t border-slate-100 text-xs text-slate-600 space-y-2">
                <div className="flex justify-between">
                  <span className="font-medium">Incident Count:</span>
                  <span className="font-black text-slate-900">{cluster.incident_count} reports</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Facilities:</span>
                  <span className="text-slate-800 text-[11px] font-semibold truncate max-w-[180px]" title={cluster.facilities_impacted.join(', ')}>
                    {cluster.facilities_impacted.join(', ')}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Interactive 5x5 Process-Safety Risk Heatmap Matrix */}
      {risk_matrix_5x5.cells && risk_matrix_5x5.cells.length > 0 && (
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center space-x-2.5">
              <div className="w-8 h-8 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center font-bold">
                <Grid className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-black text-slate-900 uppercase tracking-wide">
                  5x5 Process-Safety Risk Heatmap Matrix (Energy × Barrier Degradation)
                </h3>
                <p className="text-xs text-slate-500 font-medium">
                  Interactive cross-tabulation mapping energetic hazard capacity (Y-axis) vs engineered barrier vulnerability (X-axis).
                </p>
              </div>
            </div>
            {selectedCell && (
              <button
                onClick={() => setSelectedCell(null)}
                className="text-xs text-amber-700 font-bold hover:underline font-mono"
              >
                Clear Matrix Filter
              </button>
            )}
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-center border-collapse">
              <thead>
                <tr>
                  <th className="p-3 text-[10px] text-slate-500 font-mono text-left uppercase">Energy / Barrier</th>
                  {risk_matrix_5x5.barrier_levels.map((b, idx) => (
                    <th key={idx} className="p-3 text-[11px] font-black text-slate-800 uppercase tracking-tight bg-slate-100 border-b border-slate-200">
                      {b}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {risk_matrix_5x5.energy_levels.map((e, yIdx) => (
                  <tr key={yIdx}>
                    <td className="p-3 text-[11px] font-mono text-left text-slate-800 bg-slate-50 border-r border-slate-200 font-bold truncate max-w-[220px]" title={e}>
                      {e}
                    </td>
                    {risk_matrix_5x5.barrier_levels.map((b, xIdx) => {
                      const cell = risk_matrix_5x5.cells.find(c => c.y_index === yIdx && c.x_index === xIdx) || {};
                      const isSelected = selectedCell?.y_index === yIdx && selectedCell?.x_index === xIdx;
                      return (
                        <td key={xIdx} className="p-1.5">
                          <button
                            onClick={() => setSelectedCell(cell)}
                            className={`w-full h-14 rounded-xl border text-xs font-mono transition flex flex-col items-center justify-center p-1 ${
                              getCellBg(yIdx, xIdx, cell.incident_count)
                            } ${isSelected ? 'ring-3 ring-slate-900 scale-105' : 'hover:scale-102'}`}
                          >
                            <span className="text-base font-black">{cell.incident_count || 0}</span>
                            <span className="text-[10px] opacity-80 font-bold">SIF: {cell.theoretical_sif}</span>
                          </button>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {selectedCell && selectedCell.incident_count > 0 && (
            <div className="p-4 rounded-xl bg-amber-50 border border-amber-300 text-xs text-slate-800 flex flex-wrap items-center justify-between gap-2 shadow-xs">
              <div>
                <span className="text-amber-900 font-black">Selected Intersection: </span>
                <span className="font-bold">{selectedCell.energy_level} × {selectedCell.barrier_status} ({selectedCell.incident_count} reports)</span>
              </div>
              <span className="font-mono text-slate-700 font-bold">Incident IDs: {selectedCell.incident_ids.join(', ')}</span>
            </div>
          )}
        </div>
      )}

      {/* SIF-Precursor Density & HSE Intervention Priorities (SIH 2026 Core Deliverable) */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
          <div>
            <div className="flex items-center space-x-2.5">
              <div className="w-8 h-8 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-bold">
                <ShieldCheck className="w-4 h-4" />
              </div>
              <h3 className="text-sm font-black text-slate-900 uppercase tracking-wide">
                HSE Intervention Radar: SIF-Precursor Density & Life-Saving Rule Auto-Mapping
              </h3>
            </div>
            <p className="text-xs text-slate-600 mt-1 max-w-4xl font-medium">
              Ranks operational assets and critical activities by SIF-precursor concentration (High SIF / Total Logs).
              Auto-maps to IOGP Life-Saving Rules to guide where safety inspections, stand-downs, and barrier rectifications must focus.
            </p>
          </div>

          {/* Switcher Tabs */}
          <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 self-start md:self-auto shrink-0">
            <button
              onClick={() => setRankingTab('sites')}
              className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-black transition ${
                rankingTab === 'sites'
                  ? 'bg-amber-500 text-slate-950 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Building2 className="w-3.5 h-3.5" />
              <span>By Rig / Site ({site_density_ranking.length})</span>
            </button>
            <button
              onClick={() => setRankingTab('activities')}
              className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-black transition ${
                rankingTab === 'activities'
                  ? 'bg-amber-500 text-slate-950 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Activity className="w-3.5 h-3.5" />
              <span>By Activity ({activity_density_ranking.length})</span>
            </button>
          </div>
        </div>

        {/* Content for Sites Tab */}
        {rankingTab === 'sites' && (
          <div className="mt-5 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {site_density_ranking.map((site, idx) => {
                const isHighDensity = site.sif_density_pct >= 50;
                return (
                  <div 
                    key={idx}
                    className={`rounded-2xl p-5 border transition ${
                      isHighDensity 
                        ? 'bg-rose-50/60 border-rose-300 hover:border-rose-400 hover:shadow-md' 
                        : 'bg-slate-50 border-slate-200 hover:border-slate-300'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-center space-x-3">
                        <span className={`w-7 h-7 rounded-xl flex items-center justify-center text-xs font-mono font-black ${
                          idx === 0 ? 'bg-red-600 text-white shadow-sm' :
                          idx === 1 ? 'bg-amber-500 text-slate-950' : 'bg-slate-200 text-slate-700'
                        }`}>
                          #{idx + 1}
                        </span>
                        <div>
                          <h4 className="font-black text-sm text-slate-900">{site.facility}</h4>
                          <span className="text-xs text-slate-500 font-medium">{site.location} · {site.total_reports} logs</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className={`text-base font-black font-mono ${isHighDensity ? 'text-red-700' : 'text-amber-700'}`}>
                          {site.sif_density_pct}%
                        </span>
                        <span className="text-[10px] text-slate-500 block uppercase font-bold">SIF Density</span>
                      </div>
                    </div>

                    {/* Progress density bar */}
                    <div className="w-full bg-slate-200 rounded-full h-2.5 mt-3.5 overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${
                          isHighDensity ? 'bg-gradient-to-r from-red-600 to-amber-500' : 'bg-amber-500'
                        }`}
                        style={{ width: `${Math.min(site.sif_density_pct, 100)}%` }}
                      />
                    </div>

                    {/* Details row */}
                    <div className="grid grid-cols-2 gap-2.5 mt-3.5 text-xs">
                      <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
                        <span className="text-slate-500 block text-[10px] uppercase font-bold">Mapped IOGP Rule</span>
                        <span className="font-black text-amber-800 flex items-center space-x-1 truncate mt-0.5">
                          <CheckCircle2 className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                          <span className="truncate">{site.dominant_iogp_rule}</span>
                        </span>
                      </div>
                      <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
                        <span className="text-slate-500 block text-[10px] uppercase font-bold">Dominant Barrier Mode</span>
                        <span className="font-black text-red-700 truncate block mt-0.5">
                          {site.dominant_barrier_failure}
                        </span>
                      </div>
                    </div>

                    {/* Recommended HSE Intervention */}
                    <div className="mt-3.5 p-3 rounded-xl bg-white border border-amber-300 text-xs flex items-start space-x-2.5 shadow-2xs">
                      <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                      <div>
                        <span className="text-[10px] uppercase font-black text-amber-800 tracking-wider block">Recommended HSE Intervention:</span>
                        <p className="text-slate-700 text-xs font-medium leading-relaxed mt-0.5">{site.recommended_hse_action}</p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Content for Activities Tab */}
        {rankingTab === 'activities' && (
          <div className="mt-5 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {activity_density_ranking.map((act, idx) => {
                const isHighDensity = act.sif_density_pct >= 50;
                return (
                  <div 
                    key={idx}
                    className={`rounded-2xl p-5 border transition ${
                      isHighDensity 
                        ? 'bg-rose-50/60 border-rose-300 hover:border-rose-400 hover:shadow-md' 
                        : 'bg-slate-50 border-slate-200 hover:border-slate-300'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-center space-x-3">
                        <span className={`w-7 h-7 rounded-xl flex items-center justify-center text-xs font-mono font-black ${
                          idx === 0 ? 'bg-red-600 text-white shadow-sm' :
                          idx === 1 ? 'bg-amber-500 text-slate-950' : 'bg-slate-200 text-slate-700'
                        }`}>
                          #{idx + 1}
                        </span>
                        <div>
                          <h4 className="font-black text-sm text-slate-900">{act.activity}</h4>
                          <span className="text-xs text-slate-500 font-medium">{act.high_sif_count} High SIF out of {act.total_reports} events</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className={`text-base font-black font-mono ${isHighDensity ? 'text-red-700' : 'text-amber-700'}`}>
                          {act.sif_density_pct}%
                        </span>
                        <span className="text-[10px] text-slate-500 block uppercase font-bold">SIF Density</span>
                      </div>
                    </div>

                    {/* Progress density bar */}
                    <div className="w-full bg-slate-200 rounded-full h-2.5 mt-3.5 overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${
                          isHighDensity ? 'bg-gradient-to-r from-red-600 to-amber-500' : 'bg-amber-500'
                        }`}
                        style={{ width: `${Math.min(act.sif_density_pct, 100)}%` }}
                      />
                    </div>

                    {/* Details row */}
                    <div className="grid grid-cols-2 gap-2.5 mt-3.5 text-xs">
                      <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
                        <span className="text-slate-500 block text-[10px] uppercase font-bold">Auto-Mapped IOGP Rule</span>
                        <span className="font-black text-amber-800 flex items-center space-x-1 truncate mt-0.5">
                          <CheckCircle2 className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                          <span className="truncate">{act.dominant_iogp_rule}</span>
                        </span>
                      </div>
                      <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
                        <span className="text-slate-500 block text-[10px] uppercase font-bold">Precursor Barrier Failure</span>
                        <span className="font-black text-red-700 truncate block mt-0.5">
                          {act.key_barrier_failure}
                        </span>
                      </div>
                    </div>

                    {/* Targeted HSE Focus */}
                    <div className="mt-3.5 p-3 rounded-xl bg-white border border-amber-300 text-xs flex items-start space-x-2.5 shadow-2xs">
                      <HardHat className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                      <div>
                        <span className="text-[10px] uppercase font-black text-amber-800 tracking-wider block">Targeted HSE Focus:</span>
                        <p className="text-slate-700 text-xs font-medium leading-relaxed mt-0.5">{act.hse_focus_intervention}</p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Recharts Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: The Core Thesis Chart: SIF vs Reported Injury */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="text-xs font-black text-slate-900 uppercase tracking-wide flex items-center space-x-1.5">
                <ShieldAlert className="w-4 h-4 text-red-600" />
                <span>SIF-Potential vs Reported Injury Disparity</span>
              </h4>
              <p className="text-xs text-slate-500 font-medium mt-0.5">
                Proves that weak-signal near-misses (0 injury) contain high fatality potential.
              </p>
            </div>
          </div>
          <div className="h-68">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sif_vs_injury_matrix} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="reported_severity" stroke="#64748b" tick={{ fontSize: 10, fill: '#334155' }} interval={0} angle={-15} textAnchor="end" />
                <YAxis stroke="#64748b" tick={{ fontSize: 10, fill: '#334155' }} allowDecimals={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)', fontSize: '11px' }} 
                  itemStyle={{ color: '#0f172a' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="high_sif" name="High SIF Potential" fill="#ef4444" radius={[4, 4, 0, 0]} />
                <Bar dataKey="medium_sif" name="Medium SIF" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                <Bar dataKey="low_sif" name="Low / Non-SIF" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Hotspot Rigs & Facilities */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="text-xs font-black text-slate-900 uppercase tracking-wide flex items-center space-x-1.5">
                <Building2 className="w-4 h-4 text-amber-600" />
                <span>Precursor Distribution Across OIL Facilities</span>
              </h4>
              <p className="text-xs text-slate-500 font-medium mt-0.5">
                Surfaces active drilling rigs and production installations requiring intervention.
              </p>
            </div>
          </div>
          <div className="h-68">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={rig_distribution.slice(0, 6)} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="facility" stroke="#64748b" tick={{ fontSize: 10, fill: '#334155' }} interval={0} angle={-15} textAnchor="end" />
                <YAxis stroke="#64748b" tick={{ fontSize: 10, fill: '#334155' }} allowDecimals={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)', fontSize: '11px' }} 
                  itemStyle={{ color: '#0f172a' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="high_sif" name="High SIF" fill="#ef4444" stackId="a" radius={[0, 0, 0, 0]} />
                <Bar dataKey="medium_sif" name="Medium SIF" fill="#f59e0b" stackId="a" radius={[0, 0, 0, 0]} />
                <Bar dataKey="low_sif" name="Low SIF" fill="#10b981" stackId="a" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 3: Barrier Degradation Breakdown */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="text-xs font-black text-slate-900 uppercase tracking-wide flex items-center space-x-1.5">
                <Anchor className="w-4 h-4 text-sky-600" />
                <span>Barrier Status Breakdown</span>
              </h4>
              <p className="text-xs text-slate-500 font-medium mt-0.5">
                Distribution of failed, bypassed, and degraded engineered controls.
              </p>
            </div>
          </div>
          <div className="h-68">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barrier_distribution} layout="vertical" margin={{ top: 10, right: 20, left: 40, bottom: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis type="number" stroke="#64748b" tick={{ fontSize: 10, fill: '#334155' }} allowDecimals={false} />
                <YAxis type="category" dataKey="status" stroke="#64748b" tick={{ fontSize: 10, fill: '#334155' }} width={110} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', fontSize: '11px' }} />
                <Bar dataKey="count" name="Incidents" fill="#0284c7" radius={[0, 6, 6, 0]}>
                  {barrier_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={BARRIER_COLORS[entry.status] || '#38bdf8'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 4: Timeline Trends */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="text-xs font-black text-slate-900 uppercase tracking-wide flex items-center space-x-1.5">
                <TrendingUp className="w-4 h-4 text-emerald-600" />
                <span>Chronological Incident & Precursor Trends</span>
              </h4>
              <p className="text-xs text-slate-500 font-medium mt-0.5">
                Monthly trajectory of reported incidents and SIF-potential precursors.
              </p>
            </div>
          </div>
          <div className="h-68">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timeline_trends} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" stroke="#64748b" tick={{ fontSize: 10, fill: '#334155' }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10, fill: '#334155' }} allowDecimals={false} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', fontSize: '11px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Line type="monotone" dataKey="high_sif" name="High SIF" stroke="#ef4444" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="total" name="Total Reports" stroke="#0284c7" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
