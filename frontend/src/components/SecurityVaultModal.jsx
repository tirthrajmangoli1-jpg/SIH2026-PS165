import React, { useState, useEffect } from 'react';
import { 
  fetchSecurityAuditLedger, 
  simulateLedgerTampering, 
  restoreLedger 
} from '../api';

export default function SecurityVaultModal({ onClose }) {
  const [ledgerData, setLedgerData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState(null);

  const loadLedger = async () => {
    try {
      setIsLoading(true);
      const data = await fetchSecurityAuditLedger();
      setLedgerData(data);
    } catch (err) {
      console.error("Ledger fetch error", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadLedger();
  }, []);

  const handleSimulateTamper = async () => {
    try {
      setIsLoading(true);
      const res = await simulateLedgerTampering();
      setActionMessage({ type: 'danger', text: res.message });
      await loadLedger();
    } catch (err) {
      setActionMessage({ type: 'danger', text: err.message });
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestoreLedger = async () => {
    try {
      setIsLoading(true);
      const res = await restoreLedger();
      setActionMessage({ type: 'success', text: res.message });
      await loadLedger();
    } catch (err) {
      setActionMessage({ type: 'danger', text: err.message });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-5xl bg-white border border-slate-300 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-6 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div className="flex items-center space-x-3.5">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 border border-emerald-300 flex items-center justify-center text-emerald-800 font-black text-xl shadow-xs">
              🛡️
            </div>
            <div>
              <div className="flex items-center space-x-2.5">
                <h2 className="text-lg font-black text-slate-900 tracking-tight">
                  OIL Defense Cryptographic Vault & Merkle Audit Ledger
                </h2>
                <span className="text-[10px] uppercase font-mono font-bold px-2.5 py-0.5 rounded-md bg-emerald-100 text-emerald-900 border border-emerald-300">
                  FIPS-197 AES-256
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">
                Immutable SHA-256 Merkle Blockchain Proof & Field Personnel OPSEC Redaction Engine
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-800 p-2 rounded-xl bg-white border border-slate-200 hover:bg-slate-100 transition shadow-2xs"
          >
            ✕
          </button>
        </div>

        {/* Action notification */}
        {actionMessage && (
          <div className={`p-3.5 text-xs font-mono font-bold flex items-center justify-between ${
            actionMessage.type === 'danger' 
              ? 'bg-rose-100 border-b border-rose-300 text-rose-900' 
              : 'bg-emerald-100 border-b border-emerald-300 text-emerald-900'
          }`}>
            <span>{actionMessage.text}</span>
            <button onClick={() => setActionMessage(null)} className="text-xs opacity-75 hover:opacity-100">✕</button>
          </div>
        )}

        {/* Body content */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-slate-700 text-sm">
          {/* Security Status Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4.5 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between shadow-2xs">
              <span className="text-xs text-slate-500 uppercase font-black">Ledger Integrity</span>
              <div className="flex items-center space-x-2 my-1.5">
                <span className={`w-3 h-3 rounded-full ${
                  ledgerData?.valid ? 'bg-emerald-500 animate-ping' : 'bg-rose-600'
                }`} />
                <span className={`text-sm font-black font-mono ${
                  ledgerData?.valid ? 'text-emerald-800' : 'text-rose-700'
                }`}>
                  {ledgerData?.valid ? '100% UNTAMPERED' : 'CHAIN COMPROMISED'}
                </span>
              </div>
              <span className="text-xs text-slate-600 font-mono font-bold">
                {ledgerData?.total_blocks || 0} Chained Blocks
              </span>
            </div>

            <div className="p-4.5 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between shadow-2xs">
              <span className="text-xs text-slate-500 uppercase font-black">Cipher Architecture</span>
              <div className="text-sm font-black text-amber-800 font-mono my-1.5">
                AES-256-CTR
              </div>
              <span className="text-xs text-slate-600 font-mono">
                Encrypt-then-MAC (HMAC-SHA256)
              </span>
            </div>

            <div className="p-4.5 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between shadow-2xs">
              <span className="text-xs text-slate-500 uppercase font-black">Key Derivation</span>
              <div className="text-sm font-black text-cyan-800 font-mono my-1.5">
                PBKDF2-SHA256
              </div>
              <span className="text-xs text-slate-600 font-mono">
                100,000 Rounds + Salt
              </span>
            </div>

            <div className="p-4.5 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between shadow-2xs">
              <span className="text-xs text-slate-500 uppercase font-black">OPSEC Redaction</span>
              <div className="text-sm font-black text-indigo-800 font-mono my-1.5">
                Salted Tokenization
              </div>
              <span className="text-xs text-slate-600 font-mono">
                Non-Attribution Shield
              </span>
            </div>
          </div>

          {/* Live Anti-Tamper Simulation Box */}
          <div className="p-5 rounded-2xl bg-amber-50/70 border border-amber-300 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-2xs">
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-amber-900 font-black text-sm">🧪 Live Tamper-Evident Test (Judges Demo)</span>
              </div>
              <p className="text-xs text-slate-700 font-medium mt-1">
                Simulate a rogue SQL modification to prove the Merkle hash chain mathematically catches record suppression or byte alteration.
              </p>
            </div>
            <div className="flex space-x-2 w-full sm:w-auto shrink-0">
              <button
                onClick={handleSimulateTamper}
                disabled={isLoading}
                className="px-3.5 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-black font-mono shadow-xs transition"
              >
                ⚡ Simulate Tamper Attack
              </button>
              <button
                onClick={handleRestoreLedger}
                disabled={isLoading}
                className="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-black font-mono shadow-xs transition"
              >
                🔄 Restore Blockchain
              </button>
            </div>
          </div>

          {/* Merkle Blockchain Block Visualizer */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs uppercase font-mono font-black text-slate-700 tracking-wider">
                Blockchain Block Ledger ({ledgerData?.blocks?.length || 0} Blocks)
              </h3>
              <button 
                onClick={loadLedger} 
                className="text-xs font-mono font-bold text-amber-700 hover:underline"
              >
                Refresh Proofs
              </button>
            </div>

            <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
              {ledgerData?.blocks?.map((b) => (
                <div 
                  key={b.block_height}
                  className={`p-3.5 rounded-xl border font-mono text-xs transition ${
                    b.is_tampered_simulation 
                      ? 'bg-rose-50 border-rose-300 text-rose-950'
                      : 'bg-slate-50 border-slate-200 text-slate-800'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <div className="flex items-center space-x-2.5">
                      <span className="px-2 py-0.5 rounded-md bg-white border border-slate-200 text-amber-800 font-black">
                        Block #{b.block_height}
                      </span>
                      <span className="text-slate-700 font-sans font-medium">
                        Incident: <strong className="text-slate-950 font-black">{b.incident_id}</strong>
                      </span>
                    </div>
                    <span className="text-[11px] text-slate-500 font-bold">
                      {new Date(b.timestamp * 1000).toLocaleTimeString()}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs mt-2 pt-2 border-t border-slate-200">
                    <div>
                      <span className="text-slate-500">Prev Hash: </span>
                      <span className="text-slate-800 font-bold break-all">{b.prev_block_hash.slice(0, 24)}...</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Block Hash: </span>
                      <span className="text-cyan-800 font-bold break-all">{b.block_hash.slice(0, 24)}...</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Payload SHA-256: </span>
                      <span className="text-indigo-800 font-bold break-all">{b.payload_hash.slice(0, 24)}...</span>
                    </div>
                    <div>
                      <span className="text-slate-500">HMAC-SHA256 Sig: </span>
                      <span className="text-emerald-800 font-bold break-all">{b.hmac_signature.slice(0, 24)}...</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4.5 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600 font-medium">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
            <span>Sovereign Standard: FIPS-197 AES-256 / FIPS-198-1 HMAC-SHA256</span>
          </div>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-900 text-white font-bold transition shadow-xs"
          >
            Close Vault
          </button>
        </div>
      </div>
    </div>
  );
}
