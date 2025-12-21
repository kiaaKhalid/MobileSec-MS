# Architecture du Système MobileSec-MS

## Vue d'ensemble

MobileSec-MS est une plateforme de sécurité mobile basée sur une architecture microservices.

## Services Backend

### 1. AI Scanner Service (Port 5005)
**Technologie**: Python + TensorFlow/PyTorch
**Fonction**: Analyse Deep Learning des APK
- Extraction des permissions
- Analyse par CNN
- Détection de malwares

### 2. APK Scanner Service (Port 8001)
**Technologie**: Python + VirusTotal API
**Fonction**: Analyse multi-moteurs
- Scan VirusTotal
- Agrégation des résultats
- Scoring de risque

### 3. Network Inspector Service (Port 8004)
**Technologie**: Python + Scapy
**Fonction**: Analyse réseau
- Capture de paquets
- Détection d'anomalies
- Analyse de trafic

### 4. Certificate Analyzer Service (Port 8003)
**Technologie**: Python + OpenSSL
**Fonction**: Validation de certificats
- Vérification de signatures
- Analyse de chaînes de confiance
- Détection de certificats frauduleux

## Frontend

**Technologie**: React + Vite
**Port**: 5173
**Fonctionnalités**:
- Interface utilisateur moderne
- Upload de fichiers
- Visualisation des résultats
- Dashboard centralisé

## Architecture de Communication

```
┌─────────────┐
│   Frontend  │
│  (React)    │
└──────┬──────┘
       │
       ├──────────┐
       │          │
┌──────▼──────┐  ┌▼──────────────┐
│ AI Scanner  │  │  APK Scanner  │
│  (Port 5005)│  │  (Port 8001)  │
└─────────────┘  └───────────────┘
       │
       ├──────────┐
       │          │
┌──────▼──────┐  ┌▼──────────────┐
│  Network    │  │  Certificate  │
│  Inspector  │  │   Analyzer    │
│  (Port 8004)│  │  (Port 8003)  │
└─────────────┘  └───────────────┘
```

## Flux de données

1. **Upload**: Frontend → Service spécifique
2. **Traitement**: Service analyse le fichier
3. **Réponse**: Service → Frontend (JSON)
4. **Affichage**: Frontend affiche les résultats

## Sécurité

- CORS configuré pour localhost
- Validation des fichiers côté serveur
- Isolation des services
- Pas de stockage permanent des fichiers uploadés

## Déploiement

### Développement
```bash
make dev
```

### Production
```bash
docker-compose up -d
```

## Technologies utilisées

**Backend**:
- Python 3.9+
- FastAPI
- TensorFlow/PyTorch
- Scapy
- OpenSSL

**Frontend**:
- React 18
- Vite
- Axios
- Lucide Icons

**Infrastructure**:
- Docker
- Docker Compose
- Nginx (production)
