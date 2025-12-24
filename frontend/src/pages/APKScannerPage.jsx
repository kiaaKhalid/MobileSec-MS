import { useState } from 'react';
import { Upload, FileCheck, AlertCircle, Loader } from 'lucide-react';
import axios from 'axios';
import { useGlobalState } from '../context/GlobalStateContext';

const APKScannerPage = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragging, setDragging] = useState(false);
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

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith('.apk')) {
      setFile(droppedFile);
      setError(null);
    } else {
      setError('Veuillez déposer un fichier APK valide');
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
      const response = await axios.post('http://localhost:8001/scan', formData);
      setResult(response.data);
      if (response.data.job_id) {
        updateJobId('apkscanner', response.data.job_id);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors du scan de l\'APK');
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
        <h1>APK Scanner</h1>
        <p>Analysez vos fichiers APK pour détecter les vulnérabilités</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Télécharger un fichier APK</h2>
        </div>
        <div className="card-body">
          <div
            className={`upload-area ${dragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('file-input').click()}
          >
            <Upload className="upload-icon" />
            <div className="upload-text">
              <h3>Glissez-déposez votre fichier APK ici</h3>
              <p>ou cliquez pour sélectionner un fichier</p>
              {file && (
                <p style={{ marginTop: '1rem', color: 'var(--primary-color)', fontWeight: 500 }}>
                  Fichier sélectionné: {file.name}
                </p>
              )}
            </div>
            <input
              id="file-input"
              type="file"
              accept=".apk"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
          </div>

          {error && (
            <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '0.5rem', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--danger-color)' }}>
                <AlertCircle size={20} />
                <span>{error}</span>
              </div>
            </div>
          )}

          <button
            className="btn btn-primary"
            onClick={handleScan}
            disabled={!file || loading}
            style={{ width: '100%' }}
          >
            {loading ? (
              <>
                <Loader size={20} style={{ animation: 'spin 1s linear infinite' }} />
                Analyse en cours...
              </>
            ) : (
              <>
                <FileCheck size={20} />
                Lancer le scan
              </>
            )}
          </button>
        </div>
      </div>

      {loading && (
        <div className="card">
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyse de l'APK en cours... Cela peut prendre quelques instants.</p>
          </div>
        </div>
      )}

      {result && (
        <div className="results-container">
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">Résultats du Scan</h2>
              <span className={`badge ${result.status === 'done' ? 'badge-low' : 'badge-info'}`}>
                {result.status}
              </span>
            </div>
            <div className="card-body">
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
                <div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Job ID</p>
                  <p style={{ fontWeight: 600, marginTop: '0.25rem' }}>{result.job_id}</p>
                </div>
                <div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Nom du package</p>
                  <p style={{ fontWeight: 600, marginTop: '0.25rem' }}>{result.package_name || 'N/A'}</p>
                </div>
                <div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Version</p>
                  <p style={{ fontWeight: 600, marginTop: '0.25rem' }}>{result.version || 'N/A'}</p>
                </div>
                <div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Problèmes détectés</p>
                  <p style={{ fontWeight: 600, marginTop: '0.25rem', color: 'var(--danger-color)' }}>
                    {result.issues_count || 0}
                  </p>
                </div>
              </div>

              {result.permissions && result.permissions.length > 0 && (
                <div style={{ marginTop: '1.5rem' }}>
                  <h3 style={{ marginBottom: '1rem', fontSize: '1.125rem' }}>Permissions</h3>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {result.permissions.map((perm, idx) => (
                      <span key={idx} className="badge badge-info">
                        {perm}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {result.issues && result.issues.length > 0 && (
                <div style={{ marginTop: '1.5rem' }}>
                  <h3 style={{ marginBottom: '1rem', fontSize: '1.125rem' }}>Vulnérabilités Détectées</h3>
                  {result.issues.map((issue, idx) => (
                    <div key={idx} className="result-item">
                      <div className="result-header">
                        <span className="result-title">{issue.type || issue.title}</span>
                        <span className={`badge ${getSeverityBadge(issue.severity)}`}>
                          {issue.severity}
                        </span>
                      </div>
                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
                        {issue.description}
                      </p>
                      {issue.recommendation && (
                        <p style={{ marginTop: '0.5rem', fontSize: '0.875rem' }}>
                          <strong>Recommandation:</strong> {issue.recommendation}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default APKScannerPage;