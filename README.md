# MobileSec-MS 🔒📱

**Plateforme modulaire d'analyse de sécurité pour applications mobiles Android/iOS**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![OWASP MASVS](https://img.shields.io/badge/OWASP-MASVS-green.svg)](https://mobile-security.gitbook.io/masvs/)

## 📋 Vue d'ensemble

MobileSec-MS est une plateforme DevSecOps complète qui automatise la détection de vulnérabilités dans les applications mobiles. Elle détecte les failles OWASP MAS (Mobile Application Security), propose des correctifs et s'intègre dans vos pipelines CI/CD.

## 🏗️ Architecture

La plateforme est composée de 7 microservices indépendants :

### 1. **APKScanner** (Port 8001)
- Désassemble et analyse les APK
- Extrait le manifest, permissions, composants exportés
- Détecte : `debuggable`, `allowBackup`, `cleartextTraffic`
- Technologies : Python, Androguard, SQLite

### 2. **SecretHunter** (Port 8002)
- Recherche les secrets exposés dans le code
- Détecte : API keys, tokens OAuth, mots de passe hardcodés
- Technologies : Python, Regex, Androguard

### 3. **CryptoCheck** (Port 8003)
- Vérifie l'utilisation correcte des API cryptographiques
- Détecte : AES/ECB, MD5/SHA1, clés hardcodées, Random non sécurisé
- Technologies : Python, SAST, CWE mapping

### 4. **NetworkInspector** (Port 8004)
- Analyse les communications réseau (simulation)
- Détecte : HTTP cleartext, TLS faible, certificate pinning manquant
- Technologies : Python, mitmproxy (en production : AVD + proxy)

### 5. **ReportGen** (Port 8005)
- Agrège les résultats de tous les services
- Génère des rapports : JSON, PDF, SARIF (pour CI/CD)
- Technologies : Node.js, jsPDF

### 6. **FixSuggest** (Port 8006)
- Propose des correctifs conformes OWASP MASVS
- Mapping vulnérabilités → solutions concrètes
- Technologies : Python, YAML knowledge base

### 7. **CIConnector** (Port 8007)
- Génère les configurations CI/CD
- Supporte : GitHub Actions, GitLab CI, Jenkins
- Technologies : Python, templates YAML

## 🚀 Installation rapide

### Prérequis
- Docker & Docker Compose
- 4 GB RAM minimum
- 10 GB espace disque

### Démarrage

```bash
# Cloner le dépôt
git clone https://github.com/yourusername/MobileSec-MS.git
cd MobileSec-MS

# Démarrer tous les services
docker-compose up -d

# Vérifier l'état des services
docker-compose ps

# Voir les logs
docker-compose logs -f
```

### Test rapide

```bash
# Scanner un APK
curl -X POST -F "file=@examples/apks/test-app.apk" \
  http://localhost:8001/scan

# Résultat : {"job_id": "job-abc123", "status": "done"}

# Récupérer les résultats
curl http://localhost:8001/scan/job-abc123

# Générer un rapport complet
curl -X POST http://localhost:8005/generate \
  -H "Content-Type: application/json" \
  -d '{"job_ids": {"apkscanner": "job-abc123"}}'

# Rapport PDF
curl -X POST "http://localhost:8005/generate?format=pdf" \
  -H "Content-Type: application/json" \
  -d '{"job_ids": {"apkscanner": "job-abc123"}}' \
  -o report.pdf
```

## 📊 Workflow complet

```bash
# 1. Analyse APK
APK_JOB=$(curl -X POST -F "file=@app.apk" http://localhost:8001/scan | jq -r '.job_id')

# 2. Recherche de secrets
SECRET_JOB=$(curl -X POST -F "file=@app.apk" http://localhost:8002/scan | jq -r '.job_id')

# 3. Vérification crypto
CRYPTO_JOB=$(curl -X POST -F "file=@app.apk" http://localhost:8003/scan | jq -r '.job_id')

# 4. Attendre la fin des analyses
sleep 30

# 5. Générer le rapport agrégé
curl -X POST http://localhost:8005/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"job_ids\": {
      \"apkscanner\": \"$APK_JOB\",
      \"secrethunter\": \"$SECRET_JOB\",
      \"cryptocheck\": \"$CRYPTO_JOB\"
    }
  }" | jq '.'

# 6. Obtenir des suggestions de correctifs
curl -X POST http://localhost:8006/suggest \
  -H "Content-Type: application/json" \
  -d @report.json | jq '.fixes'
```

## 🔄 Intégration CI/CD

### GitHub Actions

```bash
# Télécharger le template
curl http://localhost:8007/github-action > .github/workflows/security.yml
```

### GitLab CI

```bash
# Télécharger le template
curl http://localhost:8007/gitlab-ci > .gitlab-ci.yml
```

### Guide complet

```bash
curl http://localhost:8007/integration-guide | jq '.'
```

## 📈 Conformité et Standards

- ✅ **OWASP MASVS** - Mobile Application Security Verification Standard
- ✅ **CWE** - Common Weakness Enumeration
- ✅ **CIS Mobile Benchmark**
- ✅ **NIST Mobile Security Guidelines**

## 🎯 Détection de vulnérabilités

### Catégories couvertes

| Catégorie | Exemples | Sévérité |
|-----------|----------|----------|
| **Stockage** | allowBackup, fichiers non chiffrés | MEDIUM-HIGH |
| **Crypto** | MD5, SHA1, DES, ECB, clés hardcodées | CRITICAL |
| **Réseau** | HTTP cleartext, TLS faible, no pinning | HIGH |
| **Code** | Debug actif, composants exportés | HIGH |
| **Secrets** | API keys, tokens, passwords | CRITICAL |

## 🛠️ Développement

### Structure du projet

```
MobileSec-MS/
├── services/
│   ├── apkscanner/      # Analyse APK
│   ├── secrethunter/    # Détection secrets
│   ├── cryptocheck/     # Vérification crypto
│   ├── networkinspector/# Analyse réseau
│   ├── reportgen/       # Génération rapports
│   ├── fixsuggest/      # Suggestions correctifs
│   └── ciconnector/     # Intégration CI/CD
├── examples/
│   └── apks/            # APK de test
├── docs/
│   ├── api/             # Documentation API
│   └── swagger-ui/      # Interface Swagger
└── docker-compose.yml   # Orchestration
```

### Développer un nouveau service

```bash
cd services
mkdir myservice
cd myservice

# Créer app.py, requirements.txt, Dockerfile
# Ajouter au docker-compose.yml
# Documenter dans docs/api/
```

## 📚 API Documentation

### Swagger UI

```bash
# Accéder à la documentation interactive
open http://localhost:8080
```

Ou consulter `docs/api/openapi.yaml`

## 🧪 Tests

```bash
# Lancer les tests unitaires
docker-compose run apkscanner pytest

# Test d'intégration
./tests/integration-test.sh
```

## 📊 Exemples de rapports

### JSON
```json
{
  "summary": {
    "package_name": "com.example.app",
    "total_issues": 12,
    "critical": 2,
    "high": 5,
    "medium": 3,
    "low": 2
  },
  "findings": {
    "apk_analysis": {...},
    "secrets": [...],
    "crypto_issues": [...],
    "network_issues": [...]
  },
  "recommendations": [...]
}
```

### SARIF (pour GitHub/GitLab)
Format standardisé pour intégration dans les Security tabs

## 🤝 Contribution

Contributions bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License - voir [LICENSE](LICENSE)

## 🔗 Ressources

- [OWASP MASVS](https://mobile-security.gitbook.io/masvs/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Androguard Docs](https://androguard.readthedocs.io/)
- [SARIF Spec](https://sarifweb.azurewebsites.net/)

## 📧 Support

- Issues : [GitHub Issues](https://github.com/yourusername/MobileSec-MS/issues)
- Discussions : [GitHub Discussions](https://github.com/yourusername/MobileSec-MS/discussions)

## ✅ État du projet

| Service | Status | Complétude |
|---------|--------|------------|
| APKScanner | ✅ Opérationnel | 100% |
| SecretHunter | ✅ Opérationnel | 100% |
| CryptoCheck | ✅ Opérationnel | 100% |
| NetworkInspector | ✅ Opérationnel | 100% (simulation) |
| ReportGen | ✅ Opérationnel | 100% |
| FixSuggest | ✅ Opérationnel | 100% |
| CIConnector | ✅ Opérationnel | 100% |

**Projet complété à 100% ✅**

---

Développé avec ❤️ pour la communauté DevSecOps mobile

