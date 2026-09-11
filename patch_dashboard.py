import re

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/PatternDashboard.jsx", "r") as f:
    content = f.read()

# Add buttons to Cluster cards
cluster_buttons = """                  <span className="text-slate-800 text-[11px] font-semibold truncate max-w-[180px]" title={cluster.facilities_impacted.join(', ')}>
                    {cluster.facilities_impacted.join(', ')}
                  </span>
                </div>
                {cluster.sample_incident_ids && cluster.sample_incident_ids.length > 0 && (
                  <div className="flex justify-between items-center mt-2 pt-2 border-t border-slate-100">
                    <span className="font-medium text-slate-500">View Reports:</span>
                    <div className="flex gap-1">
                      {cluster.sample_incident_ids.map(id => (
                        <button key={id} onClick={() => onSelectIncidentId && onSelectIncidentId(id)} className="px-1.5 py-0.5 rounded bg-slate-200 text-slate-700 hover:bg-slate-300 transition text-[10px] font-mono cursor-pointer underline">{id.substring(0,6)}</button>
                      ))}
                    </div>
                  </div>
                )}"""
content = re.sub(r'<span className="text-slate-800 text-\[11px\] font-semibold truncate max-w-\[180px\]" title=\{cluster\.facilities_impacted\.join\('\'', '\''\)\}>\n                    \{cluster\.facilities_impacted\.join\('\'', '\''\)\}\n                  </span>\n                </div>', cluster_buttons, content)

# Add buttons to Site cards
site_buttons = """                        <p className="text-slate-700 text-xs font-medium leading-relaxed mt-0.5">{site.recommended_hse_action}</p>
                      </div>
                    </div>
                    {site.sample_incident_ids && site.sample_incident_ids.length > 0 && (
                      <div className="mt-2.5 flex items-center justify-between text-[11px]">
                        <span className="font-bold text-slate-500 uppercase tracking-wider">Related Logs:</span>
                        <div className="flex gap-1.5">
                          {site.sample_incident_ids.map(id => (
                            <button key={id} onClick={() => onSelectIncidentId && onSelectIncidentId(id)} className="px-2 py-0.5 rounded bg-slate-200 text-slate-800 hover:bg-slate-300 transition font-mono cursor-pointer underline">{id.substring(0,8)}</button>
                          ))}
                        </div>
                      </div>
                    )}"""
content = re.sub(r'<p className="text-slate-700 text-xs font-medium leading-relaxed mt-0\.5">\{site\.recommended_hse_action\}</p>\n                      </div>\n                    </div>', site_buttons, content)


# Add buttons to Activity cards
activity_buttons = """                        <p className="text-slate-700 text-xs font-medium leading-relaxed mt-0.5">{activity.recommended_hse_action}</p>
                      </div>
                    </div>
                    {activity.sample_incident_ids && activity.sample_incident_ids.length > 0 && (
                      <div className="mt-2.5 flex items-center justify-between text-[11px]">
                        <span className="font-bold text-slate-500 uppercase tracking-wider">Related Logs:</span>
                        <div className="flex gap-1.5">
                          {activity.sample_incident_ids.map(id => (
                            <button key={id} onClick={() => onSelectIncidentId && onSelectIncidentId(id)} className="px-2 py-0.5 rounded bg-slate-200 text-slate-800 hover:bg-slate-300 transition font-mono cursor-pointer underline">{id.substring(0,8)}</button>
                          ))}
                        </div>
                      </div>
                    )}"""
content = re.sub(r'<p className="text-slate-700 text-xs font-medium leading-relaxed mt-0\.5">\{activity\.recommended_hse_action\}</p>\n                      </div>\n                    </div>', activity_buttons, content)


with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/PatternDashboard.jsx", "w") as f:
    f.write(content)
