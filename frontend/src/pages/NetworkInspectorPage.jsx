import { useState } from 'react';
import { Upload, Wifi, Globe } from 'lucide-react';
import axios from 'axios';

const NetworkInspectorPage = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

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
      const response = await axios.post('http://localhost:8004/scan', formData);
      
      if (response.data.job_id) {
        const jobResponse = await axios.get(`http://localhost:8004/scan/${response.data.job_id}`);
        setResult(jobResponse.data);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de l\'analyse réseau');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Network Inspector</h1>
        <p>Inspectez les configurations réseau et détectez les problèmes de sécurité</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Analyser un APK</h2>
        </div>
        <div className="card-body">
          <div className="upload-area" onClick={() => document.getElementById('network-file-input').click()}>
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
              id="network-file-input"
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
            {loading ? 'Analyse en cours...' : 'Inspecter le réseau'}
          </button>
        </div>
      </div>

      {loading && (
        <div className="card">
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyse des configurations réseau en cours...</p>
          </div>
        </div>
      )}

      {result && (
        <div className="results-container">
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">Résultats de l'Inspection Réseau</h2>
              <span className={`badge ${result.findings?.length > 0 ? 'badge-high' : 'badge-low'}`}>
                {result.findings?.length || 0} problème(s) détecté(s)
              </span>
            </div>
            <div className="card-body">
              {result.package_name && (
                <div style={{ marginBottom: '1.5rem' }}>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Package analysé</p>
                  <p style={{ fontWeight: 600, marginTop: '0.25rem' }}>{result.package_name}</p>
                </div>
              )}

              {result.findings && result.findings.length > 0 ? (
                result.findings.map((finding, idx) => (
                  <div key={idx} className="result-item">
                    <div className="result-header">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Wifi size={16} />
                        <span className="result-title">{finding.type}</span>
                      </div>
                      <span className={`badge ${finding.severity === 'HIGH' ? 'badge-high' : 'badge-medium'}`}>
                        {finding.severity}
                      </span>
                    </div>
                    <div style={{ marginTop: '0.75rem' }}>
                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                        {finding.description}
                      </p>
                      {finding.urls && finding.urls.length > 0 && (
                        <div style={{ marginTop: '0.75rem' }}>
                          <p style={{ fontSize: '0.875rem', fontWeight: 600, marginBottom: '0.5rem' }}>
                            URLs détectées:
                          </p>
                          <div className="code-block">
                            <pre>{finding.urls.join('\n')}</pre>
                          </div>
                        </div>
                      )}
                      {finding.recommendation && (
                        <p style={{ marginTop: '0.75rem', fontSize: '0.875rem', color: 'var(--success-color)' }}>
                          <strong>Recommandation:</strong> {finding.recommendation}
                        </p>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                  <Globe size={48} style={{ margin: '0 auto 1rem', color: 'var(--success-color)' }} />
                  <p>✅ Configuration réseau sécurisée</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NetworkInspectorPage;