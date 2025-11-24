# Quick Start Guide - MobileSec-MS

Guide de démarrage rapide en 5 minutes ⚡

## Installation en 3 commandes

```bash
git clone https://github.com/yourusername/MobileSec-MS.git
cd MobileSec-MS
make install
```

C'est tout ! 🎉

## Votre premier scan

### 1. Préparez un APK

Placez votre fichier APK dans le dossier `examples/apks/` ou utilisez un chemin absolu.

### 2. Lancez le scan

```bash
curl -X POST -F "file=@examples/apks/mon-app.apk" \
  http://localhost:8001/scan
```

Réponse:
```json
{
  "job_id": "job-abc123",
  "status": "done"
}
```

### 3. Récupérez les résultats

```bash
curl http://localhost:8001/scan/job-abc123 | jq '.'
```

## Scan complet (tous les services)

### Script automatique

```bash
#!/bin/bash
APK_FILE="mon-app.apk"

# Scanner avec tous les services
APK_JOB=$(curl -s -X POST -F "file=@$APK_FILE" http://localhost:8001/scan | jq -r '.job_id')
SECRET_JOB=$(curl -s -X POST -F "file=@$APK_FILE" http://localhost:8002/scan | jq -r '.job_id')
CRYPTO_JOB=$(curl -s -X POST -F "file=@$APK_FILE" http://localhost:8003/scan | jq -r '.job_id')

echo "APK Scanner: $APK_JOB"
echo "Secret Hunter: $SECRET_JOB"
echo "Crypto Check: $CRYPTO_JOB"

# Attendre 30 secondes
echo "Analyse en cours..."
sleep 30

# Générer le rapport
curl -X POST http://localhost:8005/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"job_ids\": {
      \"apkscanner\": \"$APK_JOB\",
      \"secrethunter\": \"$SECRET_JOB\",
      \"cryptocheck\": \"$CRYPTO_JOB\"
    }
  }" | jq '.' > report.json

echo "✅ Rapport sauvegardé: report.json"

# Générer le PDF
curl -X POST "http://localhost:8005/generate?format=pdf" \
  -H "Content-Type: application/json" \
  -d "{
    \"job_ids\": {
      \"apkscanner\": \"$APK_JOB\",
      \"secrethunter\": \"$SECRET_JOB\",
      \"cryptocheck\": \"$CRYPTO_JOB\"
    }
  }" -o report.pdf

echo "✅ Rapport PDF sauvegardé: report.pdf"

# Obtenir des suggestions
curl -X POST http://localhost:8006/suggest \
  -H "Content-Type: application/json" \
  -d @report.json | jq '.fixes' > fixes.json

echo "✅ Correctifs suggérés: fixes.json"
```

### Sauvegarder et exécuter

```bash
chmod +x scan-full.sh
./scan-full.sh
```

## Commandes utiles

```bash
# Vérifier l'état
make status

# Voir les logs
make logs

# Health check
make health

# Arrêter
make down

# Redémarrer
make restart

# Nettoyer
make clean
```

## Intégration CI/CD

### GitHub Actions

```bash
make ci-github
```

Cela crée `.github/workflows/security.yml` automatiquement.

### GitLab CI

```bash
make ci-gitlab
```

Cela crée `.gitlab-ci.yml` automatiquement.

## Interpréter les résultats

### Niveaux de sévérité

- 🔴 **CRITICAL**: Action immédiate requise
- 🟠 **HIGH**: Priorité élevée
- 🟡 **MEDIUM**: À corriger rapidement
- 🟢 **LOW**: Information

### Exemples de vulnérabilités

| Type | Sévérité | Action |
|------|----------|--------|
| Clé API hardcodée | CRITICAL | Retirer et utiliser variables d'env |
| Debug actif | HIGH | Désactiver en production |
| allowBackup=true | MEDIUM | Désactiver ou configurer règles |
| SHA-1 | MEDIUM | Migrer vers SHA-256 |

## Troubleshooting

### Les services ne démarrent pas

```bash
# Vérifier Docker
docker --version
docker-compose --version

# Reconstruire
make rebuild
```

### Port déjà utilisé

Modifier dans `docker-compose.yml`:
```yaml
ports:
  - "8001:8001"  # Changer 8001 → 9001
```

### APK invalide

```bash
# Vérifier que c'est un APK valide
file mon-app.apk

# Devrait afficher: "Zip archive data"
```

## Prochaines étapes

1. 📖 Lire le [README complet](README.md)
2. 🔍 Explorer la [documentation API](docs/api/openapi.yaml)
3. 🤝 Contribuer: voir [CONTRIBUTING.md](CONTRIBUTING.md)
4. 💬 Rejoindre la communauté

## Support

- 🐛 [Signaler un bug](https://github.com/yourusername/MobileSec-MS/issues)
- 💡 [Proposer une fonctionnalité](https://github.com/yourusername/MobileSec-MS/discussions)
- 📧 Email: security@example.com

---

**Bon scan ! 🚀**
