import { useState, useEffect } from 'react';
import { FileText, Download, Send, Zap } from 'lucide-react';
import axios from 'axios';
import { useGlobalState } from '../context/GlobalStateContext';

const ReportGenPage = () => {
  const { jobIds: globalJobIds } = useGlobalState();
  const [jobIds, setJobIds] = useState({
    apk: '',
    secret: '',
    crypto: '',
    network: ''
  });
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Auto-fill from global state if available
    setJobIds(prev => ({
      ...prev,
      apk: globalJobIds.apkscanner || prev.apk,
      secret: globalJobIds.secrethunter || prev.secret,
      crypto: globalJobIds.cryptocheck || prev.crypto,
      network: globalJobIds.networkinspector || prev.network
    }));
  }, [globalJobIds]);

  const [scanHistory, setScanHistory] = useState({
    apk: [],
    secret: [],
    crypto: [],
    network: []
  });

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const [apkRes, secretRes, cryptoRes, networkRes] = await Promise.allSettled([
          axios.get('http://localhost:8001/scans').catch(() => ({ data: [] })),
          axios.get('http://localhost:8002/scans').catch(() => ({ data: [] })),
          axios.get('http://localhost:8003/scans').catch(() => ({ data: [] })),
          axios.get('http://localhost:8004/scans').catch(() => ({ data: [] }))
        ]);

        setScanHistory({
          apk: apkRes.status === 'fulfilled' ? apkRes.value.data : [],
          secret: secretRes.status === 'fulfilled' ? secretRes.value.data : [],
          crypto: cryptoRes.status === 'fulfilled' ? cryptoRes.value.data : [],
          network: networkRes.status === 'fulfilled' ? networkRes.value.data : []
        });
      } catch (e) {
        console.error("Error fetching scan history", e);
      }
    };
    fetchHistory();
  }, []);

  const handleInputChange = (e) => {
    setJobIds({ ...jobIds, [e.target.name]: e.target.value });
  };

  const handleGenerateReport = async () => {
    setLoading(true);
    setError(null);
    setReport(null);

    try {
      const response = await axios.post('http://localhost:8005/generate', {
        job_ids: {
          apkscanner: jobIds.apk || undefined,
          secrethunter: jobIds.secret || undefined,
          cryptocheck: jobIds.crypto || undefined,
          networkinspector: jobIds.network || undefined
        },
        format: 'json'
      });
      setReport(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de la génération du rapport');
    } finally {
      setLoading(false);
    }
  };

  // Check if we have enough data to suggest auto-generation
  const canAutoGenerate = jobIds.apk || jobIds.secret || jobIds.crypto || jobIds.network;

  const downloadReport = () => {
    if (!report) return;

    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `security-report-${new Date().toISOString()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <div className="page-header">
        <h1>Report Generator</h1>
        <p>Générez des rapports de sécurité complets à partir de vos analyses</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Générer un Rapport</h2>
          {canAutoGenerate && (
            <div className="badge badge-success" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success-color)' }}>
              <Zap size={14} />
              Données d'analyse détectées
            </div>
          )}
        </div>
        <div className="card-body">
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Les champs ci-dessous se remplissent automatiquement si vous avez effectué des analyses récemment.
          </p>

          <div style={{ display: 'grid', gap: '1rem' }}>
            {/* APK Scanner Input */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <label style={{ fontWeight: 500 }}>APK Scanner Job ID</label>
                {scanHistory.apk.length > 0 && (
                  <select
                    onChange={(e) => setJobIds({ ...jobIds, apk: e.target.value })}
                    style={{ padding: '0.25rem', borderRadius: '0.25rem', border: '1px solid var(--border-color)', fontSize: '0.8rem' }}
                  >
                    <option value="">-- Historique --</option>
                    {scanHistory.apk.map(scan => (
                      <option key={scan.id} value={scan.id}>
                        {new Date(scan.created_at).toLocaleTimeString()} - {scan.package_name || scan.filename}
                      </option>
                    ))}
                  </select>
                )}
              </div>
              <input
                type="text"
                name="apk"
                value={jobIds.apk}
                onChange={handleInputChange}
                placeholder="apk-123456..."
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  background: 'var(--bg-color)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '0.5rem',
                  color: 'var(--text-color)',
                  fontSize: '1rem'
                }}
              />
            </div>

            {/* Secret Hunter Input */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <label style={{ fontWeight: 500 }}>Secret Hunter Job ID</label>
                {scanHistory.secret.length > 0 && (
                  <select
                    onChange={(e) => setJobIds({ ...jobIds, secret: e.target.value })}
                    style={{ padding: '0.25rem', borderRadius: '0.25rem', border: '1px solid var(--border-color)', fontSize: '0.8rem' }}
                  >
                    <option value="">-- Historique --</option>
                    {scanHistory.secret.map(scan => (
                      <option key={scan.id} value={scan.id}>
                        {new Date(scan.created_at).toLocaleTimeString()} - {scan.filename}
                      </option>
                    ))}
                  </select>
                )}
              </div>
              <input
                type="text"
                name="secret"
                value={jobIds.secret}
                onChange={handleInputChange}
                placeholder="secret-123456..."
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  background: 'var(--bg-color)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '0.5rem',
                  color: 'var(--text-color)',
                  fontSize: '1rem'
                }}
              />
            </div>

            {/* Crypto Check Input */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <label style={{ fontWeight: 500 }}>Crypto Check Job ID</label>
                {scanHistory.crypto.length > 0 && (
                  <select
                    onChange={(e) => setJobIds({ ...jobIds, crypto: e.target.value })}
                    style={{ padding: '0.25rem', borderRadius: '0.25rem', border: '1px solid var(--border-color)', fontSize: '0.8rem' }}
                  >
                    <option value="">-- Historique --</option>
                    {scanHistory.crypto.map(scan => (
                      <option key={scan.id} value={scan.id}>
                        {new Date(scan.created_at).toLocaleTimeString()} - {scan.filename}
                      </option>
                    ))}
                  </select>
                )}
              </div>
              <input
                type="text"
                name="crypto"
                value={jobIds.crypto}
                onChange={handleInputChange}
                placeholder="crypto-123456..."
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  background: 'var(--bg-color)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '0.5rem',
                  color: 'var(--text-color)',
                  fontSize: '1rem'
                }}
              />
            </div>

            {/* Network Inspector Input */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <label style={{ fontWeight: 500 }}>Network Inspector Job ID</label>
                {scanHistory.network.length > 0 && (
                  <select
                    onChange={(e) => setJobIds({ ...jobIds, network: e.target.value })}
                    style={{ padding: '0.25rem', borderRadius: '0.25rem', border: '1px solid var(--border-color)', fontSize: '0.8rem' }}
                  >
                    <option value="">-- Historique --</option>
                    {scanHistory.network.map(scan => (
                      <option key={scan.id} value={scan.id}>
                        {new Date(scan.created_at).toLocaleTimeString()} - {scan.package_name || "Unknown"}
                      </option>
                    ))}
                  </select>
                )}
              </div>
              <input
                type="text"
                name="network"
                value={jobIds.network}
                onChange={handleInputChange}
                placeholder="network-123456..."
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  background: 'var(--bg-color)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '0.5rem',
                  color: 'var(--text-color)',
                  fontSize: '1rem'
                }}
              />
            </div>
          </div>

          {error && (
            <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '0.5rem', marginTop: '1rem' }}>
              <p style={{ color: 'var(--danger-color)' }}>{error}</p>
            </div>
          )}

          <button
            className="btn btn-primary"
            onClick={handleGenerateReport}
            disabled={loading}
            style={{ width: '100%', marginTop: '1.5rem' }}
          >
            {loading ? (
              <>Génération en cours...</>
            ) : (
              <>
                <Send size={20} />
                Générer le Rapport
              </>
            )}
          </button>
        </div>
      </div>

      {report && (
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Rapport Généré</h2>
            <button className="btn btn-secondary" onClick={downloadReport}>
              <Download size={20} />
              Télécharger JSON
            </button>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
              <div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Score de Sécurité</p>
                <p style={{ fontWeight: 700, fontSize: '1.5rem', color: report.security_score >= 70 ? 'var(--success-color)' : 'var(--danger-color)' }}>
                  {report.security_score || 'N/A'}/100
                </p>
              </div>
              <div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Vulnérabilités Totales</p>
                <p style={{ fontWeight: 700, fontSize: '1.5rem' }}>{report.total_issues || 0}</p>
              </div>
              <div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Critiques</p>
                <p style={{ fontWeight: 700, fontSize: '1.5rem', color: 'var(--danger-color)' }}>{report.critical_issues || 0}</p>
              </div>
              <div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Élevées</p>
                <p style={{ fontWeight: 700, fontSize: '1.5rem', color: 'var(--warning-color)' }}>{report.high_issues || 0}</p>
              </div>
            </div>

            <div className="code-block" style={{ maxHeight: '500px', overflowY: 'auto' }}>
              <pre>{JSON.stringify(report, null, 2)}</pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportGenPage;
