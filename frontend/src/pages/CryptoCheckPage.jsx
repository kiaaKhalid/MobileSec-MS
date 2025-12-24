import { useState } from 'react';
import { Upload, Shield, Lock } from 'lucide-react';
import axios from 'axios';
import { useGlobalState } from '../context/GlobalStateContext';

const CryptoCheckPage = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const { updateJobId } = useGlobalState();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.name.endsWith('.apk')) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Veuillez sélectionner un fichier APK valide');
    }
  };

  const handleScan = async () => {
    if (!file) {
      setError('Veuillez sélectionner un fichier APK');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8003/scan', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (response.data.job_id) {
        updateJobId('cryptocheck', response.data.job_id);
        const jobResponse = await axios.get(`http://localhost:8003/scan/${response.data.job_id}`);
        setResult(jobResponse.data);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de l\'analyse cryptographique');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityBadge = (severity) => {
    const badges = {
      CRITICAL: 'badge-critical',
      HIGH: 'badge-high',
      MEDIUM: 'badge-medium',
      LOW: 'badge-low',
    };
    return badges[severity] || 'badge-info';
  };

  return (
    <div>
      <div className="page-header">
        <h1>Crypto Check</h1>
        <p>Analysez les implémentations cryptographiques et détectez les faiblesses</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Analyser un APK</h2>
        </div>
        <div className="card-body">
          <div className="upload-area" onClick={() => document.getElementById('crypto-file-input').click()}>
            <Upload className="upload-icon" />
            <div className="upload-text">
              <h3>Télécharger un fichier APK</h3>
              <p>Cliquez pour sélectionner un fichier</p>
              {file && (
                <p style={{ marginTop: '1rem', color: 'var(--primary-color)', fontWeight: 500 }}>
                  {file.name}
                </p>
              )}
            </div>
            <input
              id="crypto-file-input"
              type="file"
              accept=".apk"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
          </div>

          {error && (
            <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '0.5rem', marginBottom: '1rem' }}>
              <p style={{ color: 'var(--danger-color)' }}>{error}</p>
            </div>
          )}

          <button className="btn btn-primary" onClick={handleScan} disabled={!file || loading} style={{ width: '100%' }}>
            {loading ? 'Analyse en cours...' : 'Analyser la cryptographie'}
          </button>
        </div>
      </div>

      {loading && (
        <div className="card">
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyse cryptographique en cours...</p>
          </div>
        </div>
      )}

      {result && (
        <div className="results-container">
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">Problèmes Cryptographiques</h2>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <span className={`badge ${result.critical_count > 0 ? 'badge-critical' : 'badge-low'}`}>
                  {result.critical_count || 0} critique(s)
                </span>
                <span className={`badge ${result.high_count > 0 ? 'badge-high' : 'badge-low'}`}>
                  {result.high_count || 0} élevé(s)
                </span>
              </div>
            </div>
            <div className="card-body">
              {result.findings && result.findings.length > 0 ? (
                result.findings.map((issue, idx) => (
                  <div key={idx} className="result-item">
                    <div className="result-header">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Lock size={16} />
                        <span className="result-title">{issue.type}</span>
                      </div>
                      <span className={`badge ${getSeverityBadge(issue.severity)}`}>
                        {issue.severity}
                      </span>
                    </div>
                    <div style={{ marginTop: '0.75rem' }}>
                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                        {issue.description}
                      </p>
                      {issue.cwe && (
                        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                          <strong>CWE:</strong> {issue.cwe}
                        </p>
                      )}
                      {issue.location && (
                        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                          <strong>Emplacement:</strong> {issue.location}
                        </p>
                      )}
                      {issue.recommendation && (
                        <div style={{ marginTop: '0.75rem', padding: '0.75rem', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '0.5rem' }}>
                          <p style={{ fontSize: '0.875rem', color: 'var(--success-color)' }}>
                            <strong>✓ Recommandation:</strong> {issue.recommendation}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                  <Shield size={48} style={{ margin: '0 auto 1rem', color: 'var(--success-color)' }} />
                  <p>✅ Aucun problème cryptographique majeur détecté</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CryptoCheckPage;
