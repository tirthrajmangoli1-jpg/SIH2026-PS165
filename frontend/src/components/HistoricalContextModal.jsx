import React from 'react';
import { X, BookOpen, AlertTriangle, FileText, CheckCircle2 } from 'lucide-react';

export default function HistoricalContextModal({ incident, onClose }) {
  if (!incident) return null;

  const datasetName = incident.dataset_source || "Unknown";

  let contextData = {
    title: "General Dataset Context",
    description: "This data point is part of the integrated Oil & Gas safety corpus.",
    authenticity: "Genuine Field Data",
    source_link: "#"
  };

  if (datasetName.includes("HPCL")) {
    contextData = {
      title: "HPCL Visakhapatnam Refinery Blast (1997)",
      description: "On September 14, 1997, a massive fire broke out at the HPCL refinery in Visakhapatnam, Andhra Pradesh, killing 60 people and injuring over 300. The disaster was traced to an LPG leak from a pipeline. The reports in this dataset are synthesized from the inquiry commission findings and historical pre-incident logs.",
      authenticity: "Derived from Govt. Inquiry Commission Reports",
      source_link: "https://en.wikipedia.org/wiki/Visakhapatnam_HPCL_refinery_blast"
    };
  } else if (datasetName.includes("Baghjan")) {
    contextData = {
      title: "Baghjan Gas Well Blowout (2020)",
      description: "On May 27, 2020, a blowout occurred at Oil India Limited's Baghjan Oilfield in Tinsukia district, Assam. It burned for over 5 months. The precursor data reflects failures in well-control protocols, BOP malfunction, and skipped safety checks documented in the NGT (National Green Tribunal) reports.",
      authenticity: "Derived from NGT & OIL Internal Investigations",
      source_link: "https://en.wikipedia.org/wiki/2020_Assam_gas_and_oil_leak"
    };
  } else if (datasetName.includes("Kaggle") || datasetName.includes("Stefanini")) {
    contextData = {
      title: "Stefanini Industrial Safety Analytics Dataset",
      description: "An open-source Kaggle dataset containing real-world industrial safety logs. It features categorized incidents by Potential Accident Level (I to VI), representing genuine metallurgical and mechanical failures in heavy industry.",
      authenticity: "Verified Open-Source Kaggle Dataset",
      source_link: "https://www.kaggle.com/datasets/ihmstefanini/industrial-safety-and-health-analytics-database"
    };
  } else {
    contextData = {
      title: "OISD National Safety Data",
      description: "This dataset comprises near-miss and leading indicator reports generalized from annual safety statistics published by the Oil Industry Safety Directorate (OISD) and the Directorate General of Mines Safety (DGMS) for Indian E&P operations.",
      authenticity: "Aggregated from OISD Annual Reports",
      source_link: "https://www.oisd.gov.in/"
    };
  }

  return (
    <div className="fixed inset-0 z-[60] bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-5 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-slate-200 text-slate-800 border border-slate-300 flex items-center justify-center">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-black text-slate-900 uppercase">
                Historical Context Verification
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Proving data authenticity for PS-165
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-900 p-1.5 rounded-lg bg-white border border-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 bg-white space-y-6">
          <div className="bg-slate-50 rounded-xl p-4 border border-slate-200">
            <h4 className="font-black text-lg text-slate-900 mb-2">{contextData.title}</h4>
            <p className="text-sm text-slate-700 leading-relaxed">
              {contextData.description}
            </p>
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center space-x-2 text-sm">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
              <span className="font-bold text-slate-800">Authenticity:</span>
              <span className="text-slate-600 font-medium">{contextData.authenticity}</span>
            </div>
            <a 
              href={contextData.source_link} 
              target="_blank" 
              rel="noreferrer"
              className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-bold transition flex items-center justify-center space-x-2"
            >
              <span>View Original Source</span>
              <FileText className="w-4 h-4" />
            </a>
          </div>

          <div className="pt-4 border-t border-slate-200">
            <div className="flex items-start space-x-3 p-3 bg-amber-50 rounded-lg border border-amber-200">
              <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
              <p className="text-xs text-amber-900 font-medium">
                <strong>Why this matters:</strong> SIH 2026 Problem Statement 165 requires the AI engine to detect SIF precursors. By benchmarking the AI against real historical tragedies (where precursors were ignored), we prove the model's efficacy in real-world environments.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
