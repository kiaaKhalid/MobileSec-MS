# APKScanner — Microservice d'Analyse Statique Android

**APKScanner** est le premier module de la plateforme **MobileSec-MS**. Ce microservice est responsable de l'analyse statique automatisée des fichiers Android (`.apk`). Il extrait les métadonnées essentielles et détecte les premières failles de configuration directement depuis le fichier *Manifest*.

## 🚀 Fonctionnalités

Ce service analyse un APK uploadé et retourne un rapport JSON contenant :

* 📦 **Identité :** Nom du package.
* 🛡️ **Permissions :** Liste complète des permissions demandées.
* ⚠️ **Surface d'attaque :** Liste des composants **exportés** (Activités, Services, Receivers, Providers) accessibles par d'autres applications.
* 🚩 **Flags de Sécurité :**
    * `debuggable` : L'application peut-elle être débuggée ? (Critique pour la prod).
    * `allowBackup` : Les données peuvent-elles être sauvegardées/volées via ADB ?
    * `usesCleartextTraffic` : Le trafic HTTP non chiffré est-il autorisé ?

> **Note :** Ce service inclut un système de nettoyage automatique. Les fichiers APK sont supprimés immédiatement après l'analyse pour préserver l'espace disque du serveur.

---

## 🛠️ Architecture Technique

* **Langage :** Python 3.11
* **Framework Web :** Flask / Gunicorn
* **Analyseur :** Androguard + Parsing XML natif (pour la robustesse)
* **Base de données :** SQLite (via SQLAlchemy)
* **Conteneurisation :** Docker (Image `python:3.11-slim`)

---

## 🐳 Installation et Démarrage (Docker)

C'est la méthode recommandée pour éviter les problèmes de dépendances système (`libmagic`, `build-essential`).

### 1. Construire l'image
```bash
Endpoints:
- GET  /health
- POST /scan  (multipart/form-data, field `file`)
- GET  /scan/{job_id}

Usage local:
1. Build:
   docker build -t mobilesec/apkscanner:dev .
2. Run:
   docker run --rm -p 8001:8001 -v $(pwd)/storage.db:/app/storage.db mobilesec/apkscanner:dev
3. Test:
   curl http://localhost:8001/health

