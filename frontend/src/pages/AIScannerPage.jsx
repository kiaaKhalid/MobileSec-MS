import React, { useState } from 'react';
import { Upload, AlertTriangle, CheckCircle, Brain, Loader, FileText, Shield, Activity } from 'lucide-react';

const AIScannerPage = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handleScan = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Simulation de l'appel API (remplacez par votre fetch réel vers localhost:5005)
      // const response = await fetch('http://localhost:5005/scan', { method: 'POST', body: formData });
      
      // Pour la démo visuelle, je simule une réponse après 2 secondes
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Exemple de fausse réponse pour visualiser le design (à supprimer pour la prod)
      const mockResponse = {
        file: file.name,
        status: 'SECURE', // Changez ceci en 'MALWARE' ou 'SUSPICIOUS' pour tester les couleurs
        risk_score: 0.1187,
        engine: 'MobileSec-DeepLearning-v3'
      };
      
      // En production, décommentez ceci :
      /*
      if (!response.ok) throw new Error('Erreur analyse');
      const data = await response.json();
      setResult(data);
      */
     
      setResult(mockResponse); // À remplacer par data

    } catch (err) {
      setError("Impossible de contacter le service IA. Vérifiez la connexion.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Configuration des couleurs selon le statut pour le mode sombre
  const getStatusConfig = (status) => {
    switch (status) {
      case 'MALWARE': 
        return {
          bg: 'bg-red-500/10',
          border: 'border-red-500/50',
          text: 'text-red-400',
          icon: <AlertTriangle className="w-6 h-6 text-red-500" />,
          label: 'MALVEILLANT DÉTECTÉ',
          gradient: 'from-red-600 to-orange-600'
        };
      case 'SUSPICIOUS': 
        return {
          bg: 'bg-yellow-500/10',
          border: 'border-yellow-500/50',
          text: 'text-yellow-400',
          icon: <AlertTriangle className="w-6 h-6 text-yellow-500" />,
          label: 'COMPORTEMENT SUSPECT',
          gradient: 'from-yellow-600 to-orange-500'
        };
      case 'SECURE': 
        return {
          bg: 'bg-emerald-500/10',
          border: 'border-emerald-500/50',
          text: 'text-emerald-400',
          icon: <CheckCircle className="w-6 h-6 text-emerald-500" />,
          label: 'FICHIER SÉCURISÉ',
          gradient: 'from-emerald-600 to-teal-600'
        };
      default: return {};
    }
  };

  return (
    <div className="main-content">
      <div className="page-header">
        <h1 className="flex items-center gap-3"><Brain className="text-primary" size={36} /> Analyse Deep Learning</h1>
        <p className="text-secondary">Utilisez notre modèle de réseau de neurones convolutifs pour détecter les malwares Android basés sur l'analyse statique des permissions.</p>
      </div>

      <div className="card" style={{ maxWidth: 600, margin: '0 auto' }}>
        <div className="card-header">
          <h2 className="card-title flex items-center gap-2"><Upload size={20} className="text-primary"/> Scanner un APK</h2>
        </div>
        <div className="card-body">
          <div className="upload-area" onClick={() => document.getElementById('ai-file-input').click()} style={{ cursor: loading ? 'not-allowed' : 'pointer' }}>
            <input
              id="ai-file-input"
              type="file"
              accept=".apk"
              onChange={handleFileChange}
              style={{ display: 'none' }}
              disabled={loading}
            />
            <div className="upload-icon-box">
              {file ? <FileText size={32} className="text-primary" /> : <Upload size={32} className="text-secondary" />}
            </div>
            <div className="upload-text">
              <h3>{file ? file.name : "Cliquez pour sélectionner un fichier APK"}</h3>
              <p className="text-secondary mt-1">{file ? "Prêt pour l'analyse" : "Fichiers .apk uniquement"}</p>
            </div>
          </div>

          {error && (
            <div className="alert alert-danger mt-4 flex items-center gap-2">
              <AlertTriangle size={18} /> <span>{error}</span>
            </div>
          )}

          <button
            className="btn btn-primary mt-6 w-full flex items-center justify-center gap-2"
            onClick={handleScan}
            disabled={!file || loading}
          >
            {loading ? (<><Loader className="animate-spin" size={20} /> Analyse en cours...</>) : (<>Rechercher les menaces</>)}
          </button>
        </div>
      </div>

      {result && (
        <div className="results-container mt-8">
          <div className="card" style={{ maxWidth: 700, margin: '0 auto' }}>
            <div className="card-header flex items-center gap-3">
              {getStatusConfig(result.status).icon}
              <h2 className="card-title mb-0">{getStatusConfig(result.status).label}</h2>
              <span className={`badge ${result.status === 'MALWARE' ? 'badge-critical' : result.status === 'SUSPICIOUS' ? 'badge-warning' : 'badge-success'}`}>{(result.risk_score * 100).toFixed(2)}%</span>
            </div>
            <div className="card-body grid md:grid-cols-2 gap-8 items-center">
              <div>
                <p className="text-secondary text-sm mb-2">Fichier analysé :</p>
                <p className="font-bold mb-2">{result.file}</p>
                <p className="text-xs text-secondary mb-2">Moteur IA : <span className="font-mono text-primary font-bold">{result.engine}</span></p>
                <div className="progress-bar mt-4 mb-2">
                  <div className={`progress ${result.status === 'MALWARE' ? 'bg-danger' : result.status === 'SUSPICIOUS' ? 'bg-warning' : 'bg-success'}`}
                    style={{ width: `${result.risk_score * 100}%` }}></div>
                </div>
                <p className="text-xs text-secondary mt-2">* Un score proche de 100% indique une très forte probabilité de malware.</p>
              </div>
              <div className={`p-4 rounded-lg ${getStatusConfig(result.status).bg} ${getStatusConfig(result.status).border}`}> 
                <h4 className={`font-bold mb-2 flex items-center gap-2 ${getStatusConfig(result.status).text}`}><Shield size={18} /> Analyse terminée</h4>
                <p className="text-sm">
                  {result.status === 'SECURE' && "L'analyse approfondie des permissions n'a révélé aucun schéma correspondant aux malwares connus dans notre base de données neuronale."}
                  {result.status === 'SUSPICIOUS' && "L'IA a détecté une combinaison de permissions qui est rarement vue dans les applications légitimes. Procédez avec prudence."}
                  {result.status === 'MALWARE' && "Attention ! Ce fichier demande des permissions critiques souvent associées aux chevaux de Troie bancaires ou aux spywares."}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIScannerPage;