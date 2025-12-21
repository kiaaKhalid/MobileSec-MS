import React, { useState } from 'react';
import { Upload, AlertTriangle, CheckCircle, Brain, Loader, FileText, Shield, Activity, Zap } from 'lucide-react';
import axios from 'axios';

const AIScannerPage = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragging, setDragging] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && selectedFile.name.endsWith('.apk')) {
      setFile(selectedFile);
      setResult(null);
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
      // Appel API réel vers le service IA
      const response = await axios.post('http://localhost:5005/scan', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResult({
        ...response.data,
        file: file.name,
        analysisTime: new Date().toLocaleTimeString('fr-FR')
      });
    } catch (err) {
      // Fallback démo en cas d'erreur
      console.error('Erreur analyse:', err);
      // Décommentez pour tester le design avec une réponse fictive
      /*
      const mockResponse = {
        file: file.name,
        status: 'SUSPICIOUS',
        risk_score: 0.65,
        engine: 'MobileSec-DeepLearning-v3',
        confidence: 0.92,
        analysisTime: new Date().toLocaleTimeString('fr-FR')
      };
      setResult(mockResponse);
      */
      setError(err.response?.data?.error || 'Erreur lors de l\'analyse IA. Vérifiez la connexion au service.');
    } finally {
      setLoading(false);
    }
  };

  // Configuration des badges selon le statut
  const getStatusConfig = (status) => {
    switch (status) {
      case 'MALWARE': 
        return 'badge-critical';
      case 'SUSPICIOUS': 
        return 'badge-warning';
      case 'SECURE': 
        return 'badge-success';
      default: 
        return 'badge-info';
    }
  };

  // Configuration complète du statut avec labels et icons
  const getStatusDetails = (status) => {
    switch (status) {
      case 'MALWARE': 
        return {
          label: 'MALVEILLANT DÉTECTÉ',
          icon: <AlertTriangle size={20} className="text-red-500" />,
          description: 'Attention ! Ce fichier contient une activité malveillante. Ne pas installer.',
          color: 'text-red-500'
        };
      case 'SUSPICIOUS': 
        return {
          label: 'COMPORTEMENT SUSPECT',
          icon: <AlertTriangle size={20} className="text-yellow-500" />,
          description: 'Des schémas suspects ont été détectés. Procédez avec prudence.',
          color: 'text-yellow-500'
        };
      case 'SECURE': 
        return {
          label: 'FICHIER SÉCURISÉ',
          icon: <CheckCircle size={20} className="text-emerald-500" />,
          description: 'L\'analyse n\'a détecté aucune menace. Fichier sûr pour l\'installation.',
          color: 'text-emerald-500'
        };
      default: 
        return {
          label: 'ANALYSE EN ATTENTE',
          icon: <Brain size={20} />,
          description: 'En attente de traitement...',
          color: 'text-primary'
        };
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="flex items-center gap-3">
          <Brain className="text-primary" size={32} />
          Analyse Deep Learning
        </h1>
        <p>Utilisez notre modèle de réseau de neurones convolutifs pour détecter les malwares Android basés sur l'analyse statique des permissions.</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title flex items-center gap-2">
            <Zap size={20} className="text-primary" />
            Scanner un APK
          </h2>
        </div>
        <div className="card-body">
          <div
            className={`upload-area ${dragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('ai-file-input').click()}
            style={{ cursor: loading ? 'not-allowed' : 'pointer' }}
          >
            <Upload className="upload-icon" />
            <div className="upload-text">
              <h3>Glissez-déposez votre fichier APK ici</h3>
              <p>ou cliquez pour sélectionner un fichier</p>
              {file && (
                <p style={{ marginTop: '1rem', color: 'var(--primary-color)', fontWeight: 500 }}>
                  ✓ Fichier sélectionné: {file.name}
                </p>
              )}
            </div>
            <input
              id="ai-file-input"
              type="file"
              accept=".apk"
              onChange={handleFileChange}
              style={{ display: 'none' }}
              disabled={loading}
            />
          </div>

          {error && (
            <div style={{ 
              padding: '1rem', 
              background: 'rgba(239, 68, 68, 0.1)', 
              borderRadius: '0.5rem', 
              marginTop: '1rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              color: 'var(--danger-color)'
            }}>
              <AlertTriangle size={18} />
              <span>{error}</span>
            </div>
          )}

          <button
            className="btn btn-primary"
            onClick={handleScan}
            disabled={!file || loading}
            style={{ width: '100%', marginTop: '1.5rem' }}
          >
            {loading ? (
              <>
                <Loader size={20} style={{ animation: 'spin 1s linear infinite' }} />
                Analyse en cours...
              </>
            ) : (
              <>
                <Brain size={20} />
                Analyser l'APK
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
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                {getStatusDetails(result.status).icon}
                <h2 className="card-title mb-0">{getStatusDetails(result.status).label}</h2>
              </div>
              <span className={`badge ${getStatusConfig(result.status)}`}>
                {result.risk_score ? (result.risk_score * 100).toFixed(2) : result.risk_score || 'N/A'}%
              </span>
            </div>

            <div className="card-body">
              {/* Informations du fichier */}
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                gap: '1rem', 
                marginBottom: '1.5rem' 
              }}>
                <div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Fichier analysé</p>
                  <p style={{ fontWeight: 600, wordBreak: 'break-all' }}>{result.file}</p>
                </div>
                <div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Moteur d'analyse</p>
                  <p style={{ fontWeight: 600, fontFamily: 'monospace', color: 'var(--primary-color)' }}>
                    {result.engine || 'MobileSec-DeepLearning-v3'}
                  </p>
                </div>
                <div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Score de confiance</p>
                  <p style={{ fontWeight: 600, color: 'var(--success-color)' }}>
                    {result.confidence ? (result.confidence * 100).toFixed(1) : 'N/A'}%
                  </p>
                </div>
                <div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Heure d'analyse</p>
                  <p style={{ fontWeight: 600 }}>{result.analysisTime}</p>
                </div>
              </div>

              {/* Barre de progression du risque */}
              <div style={{ marginBottom: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <p style={{ fontSize: '0.875rem', fontWeight: 600 }}>Score de risque</p>
                  <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    {result.risk_score ? (result.risk_score * 100).toFixed(1) : 0}%
                  </p>
                </div>
                <div className="progress-bar">
                  <div 
                    className={`progress ${
                      result.status === 'MALWARE' ? 'bg-danger' : 
                      result.status === 'SUSPICIOUS' ? 'bg-warning' : 
                      'bg-success'
                    }`}
                    style={{ width: `${Math.max(result.risk_score * 100, 5)}%` }}
                  />
                </div>
              </div>

              {/* Résumé du statut */}
              <div style={{ 
                padding: '1rem', 
                borderRadius: '0.5rem',
                background: result.status === 'MALWARE' ? 'rgba(239, 68, 68, 0.1)' : 
                           result.status === 'SUSPICIOUS' ? 'rgba(234, 179, 8, 0.1)' : 
                           'rgba(34, 197, 94, 0.1)',
                borderLeft: `4px solid ${
                  result.status === 'MALWARE' ? '#ef4444' : 
                  result.status === 'SUSPICIOUS' ? '#eab308' : 
                  '#22c55e'
                }`
              }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
                  <Shield size={18} style={{ marginTop: '0.125rem', flexShrink: 0 }} />
                  <div>
                    <h4 style={{ fontWeight: 600, marginBottom: '0.5rem', marginTop: 0 }}>Résumé de l'analyse</h4>
                    <p style={{ margin: 0, fontSize: '0.875rem', lineHeight: 1.6 }}>
                      {result.status === 'SECURE' && 
                        "L'analyse approfondie des permissions n'a révélé aucun schéma correspondant aux malwares connus. Ce fichier est sûr pour l'installation."}
                      {result.status === 'SUSPICIOUS' && 
                        "L'IA a détecté une combinaison de permissions inhabituellement rare dans les applications légitimes. Procédez avec prudence et vérifiez la source."}
                      {result.status === 'MALWARE' && 
                        "Attention ! Ce fichier contient des schémas caractéristiques des malwares. La présence de permissions critiques et de comportements suspects indique une menace probable."}
                      {!result.status && "Analyse complétée. Vérifiez les détails ci-dessus."}
                    </p>
                  </div>
                </div>
              </div>

              {/* Informations supplémentaires si disponibles */}
              {result.permissions && result.permissions.length > 0 && (
                <div style={{ marginTop: '1.5rem' }}>
                  <h3 style={{ marginBottom: '1rem', fontSize: '1.125rem', fontWeight: 600 }}>Permissions détectées</h3>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {result.permissions.slice(0, 10).map((perm, idx) => (
                      <span key={idx} className="badge badge-info" style={{ fontSize: '0.8rem' }}>
                        {perm}
                      </span>
                    ))}
                    {result.permissions.length > 10 && (
                      <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', alignSelf: 'center' }}>
                        +{result.permissions.length - 10} autres
                      </span>
                    )}
                  </div>
                </div>
              )}

              {/* Recommandations */}
              <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(59, 130, 246, 0.05)', borderRadius: '0.5rem' }}>
                <h4 style={{ fontWeight: 600, marginBottom: '0.5rem', marginTop: 0 }}>
                  💡 Recommandations
                </h4>
                <ul style={{ margin: 0, paddingLeft: '1.25rem', fontSize: '0.875rem', lineHeight: 1.6 }}>
                  {result.status === 'SECURE' ? (
                    <li>Ce fichier peut être installé en toute confiance</li>
                  ) : result.status === 'SUSPICIOUS' ? (
                    <>
                      <li>Vérifiez la source de l'application</li>
                      <li>Consultez les avis utilisateurs avant d'installer</li>
                      <li>Envisagez d'utiliser une sandbox de test</li>
                    </>
                  ) : (
                    <>
                      <li>N'installez PAS ce fichier</li>
                      <li>Isolez l'appareil si vous l'avez déjà installé</li>
                      <li>Signalez l'APK aux autorités de sécurité</li>
                      <li>Scannez votre appareil avec un antivirus</li>
                    </>
                  )}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIScannerPage;