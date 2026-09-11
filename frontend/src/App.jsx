import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import GovtTicker from './components/GovtTicker';
import AutoProcessingBanner from './components/AutoProcessingBanner';
import TriageFeed from './components/TriageFeed';
import ReportDetailModal from './components/ReportDetailModal';
import ReviewerModal from './components/ReviewerModal';
import PatternDashboard from './components/PatternDashboard';
import ReportIntakeModal from './components/ReportIntakeModal';
import ExemplarStoreModal from './components/ExemplarStoreModal';
import IntakeLogModal from './components/IntakeLogModal';
import HistoricalContextModal from './components/HistoricalContextModal';
import ReviewHistoryModal from './components/ReviewHistoryModal';
import TrainingHubModal from './components/TrainingHubModal';

import { 
  fetchIncidents, 
  fetchPatterns, 
  ingestDemoBatch, 
  ingestSingleReport, 
  submitReview, 
  resetDatabase,
  fetchDatasets,
  loadDataset,
  streamNextTelemetry
} from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('triage');
  const [incidents, setIncidents] = useState([]);
  const [patterns, setPatterns] = useState(null);
  const [latestProcessed, setLatestProcessed] = useState(null);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [reviewingIncident, setReviewingIncident] = useState(null);
  const [showIntakeModal, setShowIntakeModal] = useState(false);
  const [showExemplarModal, setShowExemplarModal] = useState(false);
  const [showSecurityModal, setShowSecurityModal] = useState(false);
  const [showTrainingModal, setShowTrainingModal] = useState(false);
  const [contextIncident, setContextIncident] = useState(null);
  const [showReviewHistory, setShowReviewHistory] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [notification, setNotification] = useState(null);

  // Multi-dataset and live streaming states
  const [availableDatasets, setAvailableDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState('real_historical');
  const [isLiveStreaming, setIsLiveStreaming] = useState(false);
  const streamIntervalRef = useRef(null);

  // Load initial data
  useEffect(() => {
    initApp();
  }, []);

  // Handle live streaming telemetry timer
  useEffect(() => {
    if (isLiveStreaming) {
      streamIntervalRef.current = setInterval(async () => {
        try {
          const res = await streamNextTelemetry();
          setLatestProcessed(res);
          const updated = await fetchIncidents();
          setIncidents(updated);
          const pat = await fetchPatterns();
          setPatterns(pat);
          showToast(`⚡ Telemetry Ingested: ${res.id} (${res.sif_potential_category})`, 'info');
        } catch (err) {
          console.error("Telemetry stream error", err);
        }
      }, 4000);
    } else {
      if (streamIntervalRef.current) {
        clearInterval(streamIntervalRef.current);
        streamIntervalRef.current = null;
      }
    }
    return () => {
      if (streamIntervalRef.current) clearInterval(streamIntervalRef.current);
    };
  }, [isLiveStreaming]);

  const showToast = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const initApp = async () => {
    try {
      setIsLoading(true);
      const dsList = await fetchDatasets();
      setAvailableDatasets(dsList || []);

      let data = await fetchIncidents();
      if (!data || data.length === 0) {
        data = await ingestDemoBatch();
      }
      setIncidents(data);
      if (data.length > 0) {
        setLatestProcessed(data[0]);
      }
      const pat = await fetchPatterns();
      setPatterns(pat);
    } catch (err) {
      console.error("Init failed", err);
      showToast(`Initialization error: ${err.message}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectDataset = async (datasetKey) => {
    try {
      setIsLoading(true);
      setSelectedDataset(datasetKey);
      const data = await loadDataset(datasetKey);
      setIncidents(data);
      if (data.length > 0) setLatestProcessed(data[0]);
      const pat = await fetchPatterns();
      setPatterns(pat);
      showToast(`Switched dataset to: ${datasetKey} (${data.length} records)`, "success");
    } catch (err) {
      showToast(`Dataset switch failed: ${err.message}`, "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetDemo = async () => {
    try {
      setIsLoading(true);
      await resetDatabase();
      const data = await fetchIncidents();
      setIncidents(data);
      if (data.length > 0) setLatestProcessed(data[0]);
      const pat = await fetchPatterns();
      setPatterns(pat);
      showToast("Demo batch reset: 15 calibrated incidents loaded.", "success");
    } catch (err) {
      showToast(`Reset failed: ${err.message}`, "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReportIngested = async (newReportData) => {
    try {
      setIsLoading(true);
      const res = await ingestSingleReport(newReportData);
      setLatestProcessed(res);
      const updated = await fetchIncidents();
      setIncidents(updated);
      const pat = await fetchPatterns();
      setPatterns(pat);
      showToast(`Report ${res.id} processed: ${res.sif_potential_category}`, "success");
    } catch (err) {
      showToast(`Ingestion error: ${err.message}`, "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReviewSubmitted = async (incidentId, reviewData) => {
    try {
      setIsLoading(true);
      const updatedRec = await submitReview(incidentId, reviewData);
      const updatedList = await fetchIncidents();
      setIncidents(updatedList);
      const pat = await fetchPatterns();
      setPatterns(pat);
      showToast(
        reviewData.action === 'override'
          ? `Override applied! Added to Vector Store as ${updatedRec.exemplar_created_id}`
          : `Verdict confirmed for ${incidentId}`,
        "success"
      );
    } catch (err) {
      showToast(`Review error: ${err.message}`, "error");
    } finally {
      setIsLoading(false);
    }
  };

  // Compute summary stats
  const stats = {
    total: incidents.length,
    highSif: incidents.filter(i => i.sif_potential_category === "High SIF Potential").length,
    zeroInjurySif: incidents.filter(i => 
      i.sif_potential_category === "High SIF Potential" && 
      i.actual_injury_severity === "Near Miss / No Injury"
    ).length
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 selection:bg-amber-100 selection:text-amber-900 font-sans antialiased">
      <GovtTicker />
      {/* Toast Notification */}
      {notification && (
        <div className="fixed bottom-6 right-6 z-50 animate-bounce">
          <div className="bg-white border border-slate-300 shadow-xl rounded-xl px-4 py-3 text-xs font-semibold text-slate-800 flex items-center space-x-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-ping" />
            <span>{notification.message}</span>
          </div>
        </div>
      )}

      {/* Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        stats={stats}
        onOpenIntake={() => setShowIntakeModal(true)}
        onResetDemo={handleResetDemo}
        onOpenExemplars={() => setShowExemplarModal(true)}
        onOpenSecurityVault={() => setShowSecurityModal(true)}
        onOpenTrainingHub={() => setShowTrainingModal(true)}
        onOpenReviewHistory={() => setShowReviewHistory(true)}
        selectedDataset={selectedDataset}
        onSelectDataset={handleSelectDataset}
        availableDatasets={availableDatasets}
        isLiveStreaming={isLiveStreaming}
        onToggleLiveStream={() => setIsLiveStreaming(!isLiveStreaming)}
        isLoading={isLoading}
      />

      {/* Main Content Area */}
      <main className="flex-1 w-full max-w-[1700px] mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Screen 2: Real-time Auto-Processing Pipeline Status */}
        <AutoProcessingBanner latestProcessed={latestProcessed} />

        {/* Tab View: Screen 3 (Triage Feed) or Screen 6 (Hazard Pattern Dashboard) */}
        {activeTab === 'triage' ? (
          <TriageFeed
            incidents={incidents}
            onSelectIncident={(inc) => setSelectedIncident(inc)}
            onOpenContext={(inc) => setContextIncident(inc)}
            onReviewIncident={(inc) => setReviewingIncident(inc)}
            selectedId={selectedIncident?.id}
          />
        ) : (
          <PatternDashboard
            patterns={patterns}
            onSelectTheme={(theme) => console.log(theme)}
            onSelectIncidentId={(id) => {
              const inc = incidents.find(i => i.id === id);
              if (inc) setSelectedIncident(inc);
            }}
          />
        )}
      </main>

      {/* Screen 4: Report Detail Modal with Driving Phrase Highlighting & Saliency X-Ray */}
      {selectedIncident && (
        <ReportDetailModal
          incident={selectedIncident}
          onClose={() => setSelectedIncident(null)}
          onOpenReview={(inc) => setReviewingIncident(inc)}
          onOpenContext={(inc) => setContextIncident(inc)}
        />
      )}

      {/* Screen 5: Reviewer Decision Modal (Confirm/Override -> Vector Store) */}
      {reviewingIncident && (
        <ReviewerModal
          incident={reviewingIncident}
          onClose={() => setReviewingIncident(null)}
          onReviewSubmitted={handleReviewSubmitted}
        />
      )}

      {/* Screen 1: Report Intake Modal */}
      {showIntakeModal && (
        <ReportIntakeModal
          onClose={() => setShowIntakeModal(false)}
          onReportIngested={handleReportIngested}
        />
      )}

      {/* Exemplar Vector Store Inspector */}
      {showExemplarModal && (
        <ExemplarStoreModal
          onClose={() => setShowExemplarModal(false)}
        />
      )}

      {/* NLP Translation Intake Log Modal */}
      {showSecurityModal && (
        <IntakeLogModal
          incidents={incidents}
          onClose={() => setShowSecurityModal(false)}
        />
      )}

      {/* Industry Parameters & AI Model Training Hub Modal */}
      {showTrainingModal && (
        <TrainingHubModal
          onClose={() => setShowTrainingModal(false)}
          onTrainingCompleted={() => showToast("AI Model successfully calibrated over industry standards!", "success")}
        />
      )}
      {contextIncident && <HistoricalContextModal incident={contextIncident} onClose={() => setContextIncident(null)} />}
      {showReviewHistory && <ReviewHistoryModal incidents={incidents} onClose={() => setShowReviewHistory(false)} onSelectIncidentId={(id) => { const inc = incidents.find(i => i.id === id); if (inc) setSelectedIncident(inc); }} />}
    </div>
  );
}
