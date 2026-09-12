import React, { useState } from 'react';
import { Search, Filter, ShieldCheck, CheckCircle2, FileText, ChevronDown, Calendar, User, MapPin } from 'lucide-react';
import { mockDecisions } from '../mock/decisions';

export default function OfficerDecisions() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('All');

  const filteredDecisions = mockDecisions.filter(d => {
    const matchesSearch = d.site.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          d.incident_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          d.officer_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'All' || d.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="flex-1 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-black text-slate-100 flex items-center space-x-3">
              <ShieldCheck className="w-8 h-8 text-emerald-500" />
              <span>Officer Decisions & Audit Trail</span>
            </h1>
            <p className="text-slate-400 mt-1">Review historical calibrations, escalations, and system overrides across all sites.</p>
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center space-x-4 bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-500" />
            <input 
              type="text"
              placeholder="Search by ID, Site, or Officer Name..."
              className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-emerald-500/50"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-500" />
            <select 
              className="bg-slate-950 border border-slate-800 rounded-lg pl-10 pr-8 py-2 text-sm text-slate-200 appearance-none focus:outline-none focus:border-emerald-500/50"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="All">All Statuses</option>
              <option value="Reviewed">Reviewed</option>
              <option value="Calibrated">Calibrated (AI Updated)</option>
              <option value="Action Taken">Action Taken</option>
              <option value="Archived">Archived</option>
            </select>
            <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
          </div>
        </div>

        {/* Table */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-950/50 border-b border-slate-800">
                  <th className="p-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Decision ID</th>
                  <th className="p-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Officer / Date</th>
                  <th className="p-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Site</th>
                  <th className="p-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Action Taken</th>
                  <th className="p-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Justification</th>
                  <th className="p-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {filteredDecisions.map(decision => (
                  <tr key={decision.id} className="hover:bg-slate-800/20 transition group">
                    <td className="p-4 align-top">
                      <div className="flex flex-col">
                        <span className="font-bold text-emerald-400">{decision.id}</span>
                        <span className="text-xs text-slate-500 mt-1 flex items-center"><FileText className="w-3 h-3 mr-1"/>{decision.incident_id}</span>
                      </div>
                    </td>
                    <td className="p-4 align-top">
                      <div className="flex flex-col">
                        <span className="text-sm font-medium text-slate-200 flex items-center"><User className="w-3.5 h-3.5 mr-1.5 text-slate-500"/>{decision.officer_name}</span>
                        <span className="text-xs text-slate-500 mt-1 flex items-center"><Calendar className="w-3 h-3 mr-1"/>{decision.date}</span>
                      </div>
                    </td>
                    <td className="p-4 align-top text-sm text-slate-300">
                      <span className="flex items-center"><MapPin className="w-3.5 h-3.5 mr-1.5 text-slate-500"/>{decision.site}</span>
                    </td>
                    <td className="p-4 align-top">
                      <span className={`inline-block px-2.5 py-1 rounded-md text-xs font-bold ${
                        decision.action.includes('High') ? 'bg-rose-900/40 text-rose-400 border border-rose-800/50' : 
                        decision.action.includes('Medium') ? 'bg-amber-900/40 text-amber-400 border border-amber-800/50' :
                        'bg-sky-900/40 text-sky-400 border border-sky-800/50'
                      }`}>
                        {decision.action}
                      </span>
                    </td>
                    <td className="p-4 align-top">
                      <p className="text-sm text-slate-300 mb-2">{decision.comments}</p>
                      <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                        Input: {decision.language}
                      </span>
                    </td>
                    <td className="p-4 align-top">
                      <span className="flex items-center text-xs font-medium text-slate-400">
                        <CheckCircle2 className="w-4 h-4 mr-1.5 text-emerald-500" />
                        {decision.status}
                      </span>
                    </td>
                  </tr>
                ))}
                
                {filteredDecisions.length === 0 && (
                  <tr>
                    <td colSpan="6" className="p-8 text-center text-slate-500">
                      No decisions found matching your criteria.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  );
}
