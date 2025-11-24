import { useState } from 'react';
import { Wrench, Lightbulb, CheckCircle } from 'lucide-react';
import axios from 'axios';

const FixSuggestPage = () => {
  const [issueType, setIssueType] = useState('');
  const [issueDescription, setIssueDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState(null);
  const [error, setError] = useState(null);

  const issueTypes = [
    { value: 'CRYPTO_WEAK', label: 'Cryptographie Faible' },
    { value: 'SECRET_HARDCODED', label: 'Secret Hardcodé' },
    { value: 'INSECURE_NETWORK', label: 'Configuration Réseau Non Sécurisée' },
    { value: 'PERMISSION_EXCESSIVE', label: 'Permissions Excessives' },
    { value: 'SSL_VALIDATION', label: 'Validation SSL Désactivée' },
  ];

  const handleGetSuggestions = async () => {
    if (!issueType) {
      setError('Veuillez sélectionner un type de problème');
      return;
    }

    setLoading(true);
    setError(null);
    setSuggestions(null);

    try {
      const response = await axios.post('http://localhost:8006/suggest', {
        issue_type: issueType,
        description: issueDescription,
        context: {}
      });
      setSuggestions(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de la récupération des suggestions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Fix Suggestions</h1>
        <p>Obtenez des suggestions de corrections pour les vulnérabilités détectées</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Obtenir des Suggestions</h2>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                Type de Problème
              </label>
              <select
                value={issueType}
                onChange={(e) => setIssueType(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  background: 'var(--bg-color)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '0.5rem',
                  color: 'var(--text-color)',
                  fontSize: '1rem'
                }}
              >
                <option value="">Sélectionnez un type</option>
                {issueTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                Description (optionnel)
              </label>
              <textarea
                value={issueDescription}
                onChange={(e) => setIssueDescription(e.target.value)}
                placeholder="Décrivez le problème en détail..."
                rows={4}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  background: 'var(--bg-color)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '0.5rem',
                  color: 'var(--text-color)',
                  fontSize: '1rem',
                  resize: 'vertical',
                  fontFamily: 'inherit'
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
            onClick={handleGetSuggestions}
            disabled={loading || !issueType}
            style={{ width: '100%', marginTop: '1.5rem' }}
          >
            {loading ? (
              <>Recherche de solutions...</>
            ) : (
              <>
                <Lightbulb size={20} />
                Obtenir des Suggestions
              </>
            )}
          </button>
        </div>
      </div>

      {suggestions && (
        <div className="results-container">
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">Suggestions de Corrections</h2>
              <span className="badge badge-info">
                {suggestions.fixes?.length || 0} suggestion(s)
              </span>
            </div>
            <div className="card-body">
              {suggestions.issue_type && (
                <div style={{ marginBottom: '1.5rem' }}>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Type de problème</p>
                  <p style={{ fontWeight: 600, marginTop: '0.25rem' }}>{suggestions.issue_type}</p>
                </div>
              )}

              {suggestions.fixes && suggestions.fixes.length > 0 ? (
                suggestions.fixes.map((fix, idx) => (
                  <div key={idx} className="result-item">
                    <div className="result-header">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Wrench size={16} />
                        <span className="result-title">Solution {idx + 1}</span>
                      </div>
                      <span className="badge badge-low">
                        <CheckCircle size={14} />
                      </span>
                    </div>
                    <div style={{ marginTop: '0.75rem' }}>
                      <p style={{ fontSize: '0.875rem', marginBottom: '0.75rem' }}>
                        {fix.description}
                      </p>
                      
                      {fix.code_example && (
                        <div>
                          <p style={{ fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.875rem' }}>
                            Exemple de code:
                          </p>
                          <div className="code-block">
                            <pre>{fix.code_example}</pre>
                          </div>
                        </div>
                      )}

                      {fix.steps && fix.steps.length > 0 && (
                        <div style={{ marginTop: '0.75rem' }}>
                          <p style={{ fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.875rem' }}>
                            Étapes:
                          </p>
                          <ol style={{ paddingLeft: '1.5rem', color: 'var(--text-secondary)' }}>
                            {fix.steps.map((step, stepIdx) => (
                              <li key={stepIdx} style={{ marginBottom: '0.25rem', fontSize: '0.875rem' }}>
                                {step}
                              </li>
                            ))}
                          </ol>
                        </div>
                      )}

                      {fix.references && fix.references.length > 0 && (
                        <div style={{ marginTop: '0.75rem' }}>
                          <p style={{ fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.875rem' }}>
                            Références:
                          </p>
                          {fix.references.map((ref, refIdx) => (
                            <a
                              key={refIdx}
                              href={ref}
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{
                                display: 'block',
                                color: 'var(--primary-color)',
                                fontSize: '0.875rem',
                                marginBottom: '0.25rem',
                                textDecoration: 'none'
                              }}
                            >
                              {ref}
                            </a>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                  <p>Aucune suggestion disponible pour ce type de problème</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FixSuggestPage;
