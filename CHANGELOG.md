# Changelog - MobileSec-MS

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté
- Guide d'utilisation de l'AI Scanner avec documentation complète
- Documentation d'architecture du système microservices
- Guide de contribution pour les développeurs
- Diagramme d'architecture dans la documentation

### Modifié
- Refonte complète de l'interface utilisateur de l'AI Scanner
- Amélioration de l'affichage des résultats d'analyse
- Simplification des headers HTTP dans APKScanner et NetworkInspector
- Optimisation de la barre de progression du score de risque

### Corrigé
- Formatage des fins de fichiers dans les pages React
- Headers Content-Type redondants dans les appels API

## [1.0.0] - 2025-12-21

### Ajouté
- Service d'analyse IA avec Deep Learning (AI Scanner)
- Service d'analyse APK avec VirusTotal
- Service d'inspection réseau
- Service d'analyse de certificats
- Interface utilisateur React moderne
- Dashboard centralisé
- Système de glisser-déposer pour les fichiers
- Affichage des résultats avec scores de risque
- Recommandations de sécurité contextuelles
- Support Docker et Docker Compose

### Fonctionnalités principales
- Analyse statique des permissions APK
- Détection de malwares par CNN
- Scan multi-moteurs via VirusTotal
- Analyse de trafic réseau
- Validation de certificats SSL/TLS
- Interface responsive et moderne
- Visualisation des résultats en temps réel

### Infrastructure
- Architecture microservices
- Configuration CORS pour développement
- Healthcheck pour tous les services
- Makefile pour faciliter le développement
- Documentation complète

## [0.1.0] - 2025-12-15

### Ajouté
- Structure initiale du projet
- Configuration de base des services
- Frontend React avec Vite
- Services backend Python

---

## Types de changements

- `Ajouté` pour les nouvelles fonctionnalités
- `Modifié` pour les changements aux fonctionnalités existantes
- `Déprécié` pour les fonctionnalités bientôt supprimées
- `Supprimé` pour les fonctionnalités supprimées
- `Corrigé` pour les corrections de bugs
- `Sécurité` pour les vulnérabilités corrigées
