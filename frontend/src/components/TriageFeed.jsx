import React, { useState } from 'react';
import { 
  ShieldAlert, AlertTriangle, CheckCircle2, ChevronRight, Eye, 
  Filter, Search, UserCheck, Languages, Zap, ArrowUpDown, Clock
} from 'lucide-react';

export default function TriageFeed({ 
  incidents, 
  onSelectIncident, 
  onReviewIncident,
  selectedId 
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('ALL');
  const [nearMissOnly, setNearMissOnly] = useState(false);
  const [facilityFilter, setFacilityFilter] = useState('ALL');

  // Extract distinct facilities
  const facilities = ['ALL', ...Array.from(new Set(incidents.map(i => i.facility)))];

  // Filtering logic
  const filtered = incidents.filter(item => {
    const matchesSearch = 
      !searchTerm ||
      item.raw_text.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.facility.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.hazard_type && item.hazard_type.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesCat = 
      categoryFilter === 'ALL' ||
      (categoryFilter === 'HIGH' && item.sif_potential_category === 'High SIF Potential') ||
      (categoryFilter === 'MEDIUM' && item.sif_potential_category === 'Medium SIF Potential') ||
      (categoryFilter === 'LOW' && item.sif_potential_category === 'Low / Non-SIF');

    const matchesNearMiss = !nearMissOnly || item.actual_injury_severity === 'Near Miss / No Injury';
    const matchesFacility = facilityFilter === 'ALL' || item.facility === facilityFilter;

    return matchesSearch && matchesCat && matchesNearMiss && matchesFacility;
  });

  // Sort by highest SIF potential score first to push critical items to the top
  const sortedAndFiltered = filtered.sort((a, b) => b.stage_b_score - a.stage_b_score);

  return (
    <div className="space-y-5">
      {/* Filter and Control Bar */}
      <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Search */}
        <div className="relative w-full md:w-88">
          <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
          <input
            type="text"
            placeholder="Search reports, rigs, or hazard keywords..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-10 pr-4 py-2 text-xs font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500 transition"
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
          {/* SIF Category Buttons */}
          <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-bold">
            <button
              onClick={() => setCategoryFilter('ALL')}
              className={`px-3 py-1.5 rounded-lg transition ${
                categoryFilter === 'ALL' 
                  ? 'bg-white text-slate-900 shadow-sm border border-slate-200 font-extrabold' 
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              All ({incidents.length})
            </button>
            <button
              onClick={() => setCategoryFilter('HIGH')}
              className={`px-3 py-1.5 rounded-lg flex items-center space-x-1.5 transition ${
                categoryFilter === 'HIGH' 
                  ? 'bg-rose-100 text-rose-800 border border-rose-300 font-extrabold shadow-sm' 
                  : 'text-slate-600 hover:text-rose-700'
              }`}
            >
              <span className="w-2 h-2 rounded-full bg-red-600" />
              <span>High SIF</span>
            </button>
            <button
              onClick={() => setCategoryFilter('MEDIUM')}
              className={`px-3 py-1.5 rounded-lg flex items-center space-x-1.5 transition ${
                categoryFilter === 'MEDIUM' 
                  ? 'bg-amber-100 text-amber-900 border border-amber-300 font-extrabold shadow-sm' 
                  : 'text-slate-600 hover:text-amber-800'
              }`}
            >
              <span className="w-2 h-2 rounded-full bg-amber-500" />
              <span>Medium SIF</span>
            </button>
            <button
              onClick={() => setCategoryFilter('LOW')}
              className={`px-3 py-1.5 rounded-lg flex items-center space-x-1.5 transition ${
                categoryFilter === 'LOW' 
                  ? 'bg-emerald-100 text-emerald-900 border border-emerald-300 font-extrabold shadow-sm' 
                  : 'text-slate-600 hover:text-emerald-800'
              }`}
            >
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>Low</span>
            </button>
          </div>

          {/* Near-Miss Weak Signal Toggle */}
          <button
            onClick={() => setNearMissOnly(!nearMissOnly)}
            className={`px-3.5 py-1.5 rounded-xl border text-xs font-bold flex items-center space-x-1.5 transition shadow-xs ${
              nearMissOnly
                ? 'bg-amber-500 text-slate-950 border-amber-500 shadow-md shadow-amber-500/20'
                : 'bg-slate-50 border-slate-300 text-slate-700 hover:bg-slate-100'
            }`}
          >
            <Zap className="w-3.5 h-3.5 text-amber-600" />
            <span>Near-Misses Only (0 Injury)</span>
          </button>

          {/* Facility Select */}
          <select
            value={facilityFilter}
            onChange={(e) => setFacilityFilter(e.target.value)}
            className="bg-slate-50 border border-slate-300 text-slate-800 font-semibold rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-amber-500/30 focus:border-amber-500"
          >
            {facilities.map((fac, idx) => (
              <option key={idx} value={fac}>{fac === 'ALL' ? 'All Facilities' : fac}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Primary Triage Feed Table */}
      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50/80 text-[11px] uppercase tracking-wider text-slate-600 font-black">
                <th className="py-3.5 px-5">Rank / SIF Potential</th>
                <th className="py-3.5 px-5">Reported Injury Outcome</th>
                <th className="py-3.5 px-5">Facility / Location</th>
                <th className="py-3.5 px-5">Hazard Synopsis & Extract</th>
                <th className="py-3.5 px-5">IOGP Life-Saving Rules</th>
                <th className="py-3.5 px-5">Review Status</th>
                <th className="py-3.5 px-5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 text-xs">
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan="7" className="py-16 text-center text-slate-500 font-medium">
                    No safety reports match current filter criteria.
                  </td>
                </tr>
              ) : (
                sortedAndFiltered.map((item, idx) => {
                  const isHigh = item.sif_potential_category === "High SIF Potential";
                  const isMedium = item.sif_potential_category === "Medium SIF Potential";
                  const isNearMiss = item.actual_injury_severity === "Near Miss / No Injury";
                  const isSelected = selectedId === item.id;

                  return (
                    <tr 
                      key={item.id}
                      className={`hover:bg-amber-50/40 transition cursor-pointer ${
                        isSelected ? 'bg-amber-50 border-l-4 border-l-amber-500' : ''
                      }`}
                      onClick={() => onSelectIncident(item)}
                    >
                      {/* SIF Potential Column */}
                      <td className="py-4 px-5 whitespace-nowrap">
                        <div className="flex items-center space-x-2.5">
                          <div className="text-slate-400 font-mono text-xs font-bold w-5">
                            #{idx + 1}
                          </div>
                          <div>
                            <div className="flex items-center space-x-1.5">
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-[11px] font-black tracking-wide ${
                                isHigh
                                  ? 'bg-rose-100 text-rose-800 border border-rose-300 shadow-xs'
                                  : isMedium
                                  ? 'bg-amber-100 text-amber-900 border border-amber-300 shadow-xs'
                                  : 'bg-emerald-100 text-emerald-900 border border-emerald-300 shadow-xs'
                              }`}>
                                {isHigh && <span className="w-1.5 h-1.5 rounded-full bg-red-600 animate-ping mr-1" />}
                                {item.sif_potential_category}
                              </span>
                            </div>
                            <div className="flex items-center space-x-2 mt-1.5">
                              <div className="w-20 bg-slate-200 rounded-full h-2 overflow-hidden">
                                <div 
                                  className={`h-full rounded-full transition-all duration-300 ${
                                    isHigh ? 'bg-red-600' : isMedium ? 'bg-amber-500' : 'bg-emerald-500'
                                  }`} 
                                  style={{ width: `${Math.round(item.stage_b_score * 100)}%` }}
                                />
                              </div>
                              <span className="font-mono text-xs font-black text-slate-800">
                                {item.stage_b_score.toFixed(2)}
                              </span>
                            </div>
                          </div>
                        </div>
                      </td>

                      {/* Reported Outcome (Demonstrates the Disparity) */}
                      <td className="py-4 px-5 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-bold ${
                          isNearMiss 
                            ? 'bg-amber-100 text-amber-900 border border-amber-300'
                            : item.actual_injury_severity.includes('Lost')
                            ? 'bg-red-100 text-red-900 border border-red-300'
                            : 'bg-slate-100 text-slate-800 border border-slate-200'
                        }`}>
                          {item.actual_injury_severity}
                        </span>
                        {isNearMiss && isHigh && (
                          <p className="text-[10px] text-red-700 mt-1 font-extrabold flex items-center space-x-1">
                            <span>⚠ High SIF Weak Signal</span>
                          </p>
                        )}
                      </td>

                      {/* Facility & Location & Data Source */}
                      <td className="py-4 px-5 whitespace-nowrap">
                        <p className="font-black text-slate-900 text-sm">{item.facility}</p>
                        <p className="text-[11px] text-slate-500 font-medium">{item.location} · {item.date_reported}</p>
                        <button onClick={(e) => { e.stopPropagation(); onOpenContext && onOpenContext(item); }} title="Click to view historical context & authenticity" className="mt-1.5 inline-flex items-center px-1.5 py-0.5 rounded text-[9px] font-bold tracking-wide uppercase bg-slate-100 text-slate-600 hover:bg-slate-200 border border-slate-300 cursor-pointer transition">
                           Source: {item.dataset_source || "Historical Database"}
                        </button>
                      </td>

                      {/* Hazard, Raw Text, & AI Rationale Preview */}
                      <td className="py-4 px-5 max-w-xs md:max-w-md">
                        <div className="flex items-center space-x-2">
                          <span className="font-bold text-slate-900 truncate text-xs">
                            {item.hazard_type || "Rig Incident"}
                          </span>
                          {item.detected_codeswitch && item.detected_codeswitch.length > 0 && (
                            <span 
                              title={`Code-switch detected: ${item.detected_codeswitch.map(c => c.original_phrase).join(', ')}`}
                              className="px-2 py-0.5 text-[10px] font-extrabold rounded-md bg-purple-100 text-purple-800 border border-purple-300 flex items-center space-x-1"
                            >
                              <Languages className="w-3 h-3" />
                              <span>Assam Dialect</span>
                            </span>
                          )}
                        </div>
                        <p className="text-slate-600 text-[11px] line-clamp-2 mt-1.5 leading-relaxed italic border-l-2 border-slate-300 pl-2">
                          "{item.raw_text}"
                        </p>
                        {/* Show tiny preview of the AI's logic/decision */}
                        {item.written_rationale && (
                          <div className="mt-2 bg-slate-50 border border-slate-200 rounded p-1.5 line-clamp-2">
                            <span className="text-[10px] font-bold text-indigo-700 mr-1">AI Decision:</span>
                            <span className="text-[10px] text-slate-600">{item.written_rationale.replace(/⚠️ \*\*.*?\*\*\\n/, '').replace(/✅ \*\*.*?\*\*\\n/, '')}</span>
                          </div>
                        )}
                      </td>

                      {/* IOGP Tags */}
                      <td className="py-4 px-5">
                        <div className="flex flex-wrap gap-1.5">
                          {item.iogp_rules && item.iogp_rules.length > 0 ? (
                            item.iogp_rules.map((rule, rIdx) => (
                              <span 
                                key={rIdx}
                                className="px-2 py-0.5 text-[10px] font-bold bg-slate-100 border border-slate-300 text-slate-800 rounded-md shadow-2xs"
                              >
                                {rule}
                              </span>
                            ))
                          ) : (
                            <span className="text-slate-400 text-xs">—</span>
                          )}
                        </div>
                      </td>

                      {/* Review Status */}
                      <td className="py-4 px-5 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold ${
                          item.review_status === 'Confirmed'
                            ? 'bg-blue-100 text-blue-900 border border-blue-300'
                            : item.review_status === 'Overridden'
                            ? 'bg-purple-100 text-purple-900 border border-purple-300'
                            : 'bg-slate-100 text-slate-600 border border-slate-200'
                        }`}>
                          {item.review_status}
                        </span>
                        {item.exemplar_created_id && (
                          <p className="text-[10px] text-cyan-700 mt-1 font-mono font-bold">
                            Vector Store Active
                          </p>
                        )}
                      </td>

                      {/* Actions */}
                      <td className="py-4 px-5 text-right whitespace-nowrap">
                        <div className="flex items-center justify-end space-x-2" onClick={(e) => e.stopPropagation()}>
                          <button
                            onClick={() => onSelectIncident(item)}
                            className="p-2 rounded-lg border border-slate-300 bg-white hover:bg-slate-100 text-slate-700 hover:text-slate-900 transition shadow-xs"
                            title="View Full Report Details & Highlighting"
                          >
                            <Eye className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => onReviewIncident(item)}
                            className="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs flex items-center space-x-1 transition shadow-xs"
                            title="Officer Decision: Confirm or Override"
                          >
                            <UserCheck className="w-3.5 h-3.5" />
                            <span>Review</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
