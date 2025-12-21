# Sécurité - MobileSec-MS

## Signaler une vulnérabilité

Si vous découvrez une vulnérabilité de sécurité dans MobileSec-MS, merci de nous la signaler de manière responsable.

### Processus de signalement

1. **NE PAS** créer d'issue publique sur GitHub
2. Envoyer un email à : security@mobilesec-ms.com (ou créer une issue privée)
3. Inclure les détails suivants :
   - Description de la vulnérabilité
   - Étapes pour reproduire
   - Impact potentiel
   - Suggestions de correction (optionnel)

### Délai de réponse

- Accusé de réception : 48 heures
- Évaluation initiale : 7 jours
- Correction : selon la gravité (critique < 7 jours, haute < 30 jours)

## Politiques de sécurité

### Versions supportées

| Version | Support de sécurité |
|---------|---------------------|
| 1.0.x   | ✅ Supporté         |
| < 1.0   | ❌ Non supporté     |

### Bonnes pratiques

#### Déploiement

- **Ne jamais** exposer les services backend directement sur Internet
- Utiliser un reverse proxy (Nginx, Traefik)
- Activer HTTPS en production
- Configurer des rate limits
- Implémenter une authentification robuste

#### Configuration

```yaml
# Exemple de configuration sécurisée
services:
  ai-scanner:
    environment:
      - ALLOWED_ORIGINS=https://votre-domaine.com
      - MAX_FILE_SIZE=50MB
      - ENABLE_CORS=false
    networks:
      - internal
```

#### Fichiers uploadés

- Validation stricte des types de fichiers
- Scan antivirus recommandé
- Isolation dans un sandbox
- Suppression automatique après analyse
- Limite de taille de fichier

### Dépendances

#### Backend (Python)

Mettre à jour régulièrement :
```bash
pip install --upgrade -r requirements.txt
```

Vérifier les vulnérabilités :
```bash
pip-audit
```

#### Frontend (Node.js)

Mettre à jour régulièrement :
```bash
npm update
```

Vérifier les vulnérabilités :
```bash
npm audit
npm audit fix
```

### Sécurité du code

#### Validation des entrées

```python
# ✅ BON
def validate_apk(file):
    if not file.filename.endswith('.apk'):
        raise ValueError("Invalid file type")
    if file.size > MAX_SIZE:
        raise ValueError("File too large")
    return True

# ❌ MAUVAIS
def validate_apk(file):
    return True  # Pas de validation
```

#### Gestion des secrets

```python
# ✅ BON
import os
API_KEY = os.getenv('VIRUSTOTAL_API_KEY')

# ❌ MAUVAIS
API_KEY = "hardcoded-api-key-123"
```

### Audit de sécurité

#### Tests de sécurité recommandés

1. **Scan de vulnérabilités**
   - OWASP ZAP
   - Burp Suite
   - Nikto

2. **Analyse statique**
   - Bandit (Python)
   - ESLint security plugins (JavaScript)
   - SonarQube

3. **Tests de pénétration**
   - Upload de fichiers malveillants
   - Injection SQL/NoSQL
   - XSS
   - CSRF

### Checklist de sécurité

- [ ] HTTPS activé en production
- [ ] CORS correctement configuré
- [ ] Rate limiting implémenté
- [ ] Validation des entrées
- [ ] Gestion sécurisée des secrets
- [ ] Logs de sécurité activés
- [ ] Dépendances à jour
- [ ] Authentification/Autorisation
- [ ] Protection contre les attaques DDoS
- [ ] Backup réguliers

### Ressources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Contact

Pour toute question de sécurité :
- Email : security@mobilesec-ms.com
- PGP Key : [À définir]

---

**Note** : La sécurité est une responsabilité partagée. Merci de suivre ces recommandations.
