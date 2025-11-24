import { useState } from 'react';
import { Upload, Search, AlertTriangle, Key } from 'lucide-react';
import axios from 'axios';

const SecretHunterPage = () => {
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
      const response = await axios.post('http://localhost:8002/scan', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      if (response.data.job_id) {
        const jobResponse = await axios.get(`http://localhost:8002/scan/${response.data.job_id}`);
        setResult(jobResponse.data);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de la recherche de secrets');
    } finally {
      setLoading(false);
    }
  };

  const getSecretIcon = (type) => {
    if (type.includes('API') || type.includes('KEY')) return <Key size={16} />;
    if (type.includes('PASSWORD')) return <AlertTriangle size={16} />;
    return <Search size={16} />;
  };

  return (
    <div>
      <div className="page-header">
        <h1>Secret Hunter</h1>
        <p>Détectez les secrets, clés API et mots de passe hardcodés dans vos APK</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Scanner un APK</h2>
        </div>
        <div className="card-body">
          <div className="upload-area" onClick={() => document.getElementById('secret-file-input').click()}>
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
              id="secret-file-input"
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
            {loading ? 'Analyse en cours...' : 'Rechercher les secrets'}
          </button>
        </div>
      </div>

      {loading && (
        <div className="card">
          <div className="loading">
            <div className="spinner"></div>
            <p>Recherche de secrets en cours...</p>
          </div>
        </div>
      )}

      {result && (
        <div className="results-container">
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">Secrets Détectés</h2>
              <span className={`badge ${result.findings?.length > 0 ? 'badge-critical' : 'badge-low'}`}>
                {result.findings?.length || 0} secret(s) trouvé(s)
              </span>
            </div>
            <div className="card-body">
              {result.findings && result.findings.length > 0 ? (
                result.findings.map((secret, idx) => (
                  <div key={idx} className="result-item">
                    <div className="result-header">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        {getSecretIcon(secret.type)}
                        <span className="result-title">{secret.type}</span>
                      </div>
                      <span className="badge badge-critical">CRITIQUE</span>
                    </div>
                    <div style={{ marginTop: '0.75rem' }}>
                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                        Valeur détectée:
                      </p>
                      <div className="code-block">
                        <pre>{secret.value}</pre>
                      </div>
                      {secret.location && (
                        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                          <strong>Emplacement:</strong> {secret.location}
                        </p>
                      )}
                      <p style={{ marginTop: '0.5rem', fontSize: '0.875rem', color: 'var(--warning-color)' }}>
                        ⚠️ Ne jamais hardcoder de secrets dans le code source. Utilisez des variables d'environnement ou un gestionnaire de secrets sécurisé.
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                  <p>✅ Aucun secret détecté dans cet APK</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SecretHunterPage;
