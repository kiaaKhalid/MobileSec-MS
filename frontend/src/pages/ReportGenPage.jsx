import { useState } from 'react';
import { FileText, Download, Send } from 'lucide-react';
import axios from 'axios';

const ReportGenPage = () => {
  const [jobIds, setJobIds] = useState({
    apk: '',
    secret: '',
    crypto: '',
    network: ''
  });
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    setJobIds({ ...jobIds, [e.target.name]: e.target.value });
  };

  const handleGenerateReport = async () => {
    setLoading(true);
    setError(null);
    setReport(null);

    try {
      const response = await axios.post('http://localhost:8005/generate', {
        apk_job_id: jobIds.apk || undefined,
        secret_job_id: jobIds.secret || undefined,
        crypto_job_id: jobIds.crypto || undefined,
        network_job_id: jobIds.network || undefined,
        format: 'json'
      });
      setReport(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de la génération du rapport');
    } finally {
      setLoading(false);
    }
  };

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
        </div>
        <div className="card-body">
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Entrez les Job IDs de vos analyses précédentes pour générer un rapport consolidé.
          </p>

          <div style={{ display: 'grid', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                APK Scanner Job ID
              </label>
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

            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                Secret Hunter Job ID
              </label>
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

            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                Crypto Check Job ID
              </label>
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

            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                Network Inspector Job ID
              </label>
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
