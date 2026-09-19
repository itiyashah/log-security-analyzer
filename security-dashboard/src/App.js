import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, Lock, Play, RefreshCw, Terminal } from 'lucide-react';
import './App.css';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [logs, setLogs] = useState([]);
  const [threats, setThreats] = useState([]);
  const [blockedIps, setBlockedIps] = useState([]);
  const [manualIp, setManualIp] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const fetchData = async () => {
    setLoading(true);
    try {
      const logsRes = await fetch(`${API_BASE}/logs?limit=15`);
      const threatsRes = await fetch(`${API_BASE}/threats`);
      const blockedRes = await fetch(`${API_BASE}/blocked-ips`);

      const logsData = await logsRes.json();
      const threatsData = await threatsRes.json();
      const blockedData = await blockedRes.json();

      setLogs(logsData.logs || []);
      setThreats(threatsData.threats || []);
      setBlockedIps(blockedData.blocked_ips || []);
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRunSoar = async () => {
    setMessage("⚡ Executing SOAR Playbook...");
    await fetch(`${API_BASE}/run-soar`, { method: 'POST' });
    setMessage("✅ SOAR Playbook Executed!");
    fetchData();
  };

  const handleManualBlock = async (e) => {
    e.preventDefault();
    if (!manualIp) return;
    try {
      const res = await fetch(`${API_BASE}/block-ip`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ip: manualIp, reason: 'Manual Admin Ban' }),
      });
      if (res.ok) {
        setMessage(`🧱 Successfully blocked ${manualIp}`);
        setManualIp('');
        fetchData();
      } else {
        const err = await res.json();
        setMessage(`⚠️ ${err.detail}`);
      }
    } catch (err) {
      setMessage("⚠️ Action failed.");
    }
  };

  return (
    <div className="dashboard-container">
      <header className="header">
        <h1><Shield className="icon" /> SIEM Security Dashboard & SOAR</h1>
        <div className="header-actions">
          <button onClick={fetchData} className="btn btn-secondary">
            <RefreshCw className={loading ? "spin" : ""} /> Refresh
          </button>
          <button onClick={handleRunSoar} className="btn btn-danger">
            <Play /> Run Automated SOAR
          </button>
        </div>
      </header>

      {message && <div className="banner">{message}</div>}

      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Parsed Logs</h3>
          <p className="metric-value">{logs.length}</p>
        </div>
        <div className="metric-card danger">
          <h3>Active Threat Detections</h3>
          <p className="metric-value">{threats.length}</p>
        </div>
        <div className="metric-card warning">
          <h3>Active Blocked IPs</h3>
          <p className="metric-value">{blockedIps.length}</p>
        </div>
      </div>

      <div className="dashboard-grid">
        {/* Active Threats */}
        <div className="card">
          <h2><AlertTriangle className="icon danger-icon" /> Active Security Threats</h2>
          {threats.length === 0 ? (
            <p className="empty-text">✅ No active threats detected.</p>
          ) : (
            <ul className="threat-list">
              {threats.map((t, idx) => (
                <li key={idx} className="threat-item">
                  <span className={`badge ${t.severity.toLowerCase()}`}>{t.severity}</span>
                  <div>
                    <strong>{t.type}</strong> - IP: <code>{t.ip}</code>
                    <div className="subtext">{t.city}, {t.country} ({t.isp}) | Count: {t.count}</div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Firewall Management */}
        <div className="card">
          <h2><Lock className="icon" /> Active Firewall Blocklist</h2>
          <form onSubmit={handleManualBlock} className="block-form">
            <input
              type="text"
              placeholder="Enter IP (e.g. 192.168.1.50)"
              value={manualIp}
              onChange={(e) => setManualIp(e.target.value)}
            />
            <button type="submit" className="btn btn-primary">Block IP</button>
          </form>
          <ul className="blocked-list">
            {blockedIps.map((b, idx) => (
              <li key={idx} className="blocked-item">
                <code>{b.ip}</code>
                <span className="subtext">{b.reason}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Raw Access Logs */}
      <div className="card full-width">
        <h2><Terminal className="icon" /> Recent Web Access Logs</h2>
        <table className="log-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>IP Address</th>
              <th>Timestamp</th>
              <th>Method</th>
              <th>URL Requested</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td><code>{log.ip}</code></td>
                <td>{log.timestamp}</td>
                <td><span className="method-tag">{log.method}</span></td>
                <td><code>{log.url}</code></td>
                <td><span className={`status-tag status-${log.status}`}>{log.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
