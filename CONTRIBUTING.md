# Guide de contribution - MobileSec-MS

## Bienvenue !

Merci de votre intérêt pour contribuer à MobileSec-MS ! Ce guide vous aidera à démarrer.

## Prérequis

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- Git

## Configuration de l'environnement de développement

### 1. Cloner le projet
```bash
git clone https://github.com/kiaaKhalid/MobileSec-MS.git
cd MobileSec-MS
```

### 2. Installer les dépendances

**Backend (chaque service)**:
```bash
cd services/ai-scanner
pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install
```

### 3. Lancer en mode développement
```bash
make dev
```

## Structure du projet

```
MobileSec-MS/
├── frontend/           # Application React
│   ├── src/
│   │   ├── pages/     # Pages principales
│   │   ├── components/# Composants réutilisables
│   │   └── styles/    # Styles CSS
├── services/          # Services backend
│   ├── ai-scanner/    # Service d'analyse IA
│   ├── apk-scanner/   # Service APK
│   ├── network/       # Service réseau
│   └── certificate/   # Service certificats
├── docs/              # Documentation
└── tests/             # Tests
```

## Standards de code

### Python
- Suivre PEP 8
- Utiliser des type hints
- Documenter les fonctions avec docstrings
- Tests unitaires requis

### JavaScript/React
- Utiliser ESLint
- Composants fonctionnels avec hooks
- Props validation avec PropTypes
- Nommage en camelCase

### Commits
Format: `type(scope): description`

Types:
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage
- `refactor`: Refactorisation
- `test`: Tests
- `chore`: Maintenance

Exemples:
```
feat(ai-scanner): ajout de la détection de ransomware
fix(frontend): correction du bug d'upload
docs(readme): mise à jour des instructions
```

## Processus de contribution

### 1. Créer une branche
```bash
git checkout -b feat/ma-nouvelle-fonctionnalite
```

### 2. Développer
- Écrire du code propre et testé
- Suivre les standards
- Documenter les changements

### 3. Tester
```bash
# Tests backend
pytest

# Tests frontend
npm test
```

### 4. Commit
```bash
git add .
git commit -m "feat(scope): description claire"
```

### 5. Push et Pull Request
```bash
git push origin feat/ma-nouvelle-fonctionnalite
```

Créer une PR sur GitHub avec:
- Description claire des changements
- Screenshots si UI
- Tests effectués
- Breaking changes éventuels

## Tests

### Backend
```bash
cd services/ai-scanner
pytest tests/
```

### Frontend
```bash
cd frontend
npm test
```

### Tests d'intégration
```bash
make test
```

## Documentation

- Documenter toute nouvelle fonctionnalité
- Mettre à jour le README si nécessaire
- Ajouter des exemples d'utilisation
- Commenter le code complexe

## Questions ?

- Ouvrir une issue sur GitHub
- Consulter la documentation existante
- Contacter les mainteneurs

## Code de conduite

- Respecter les autres contributeurs
- Être constructif dans les reviews
- Partager les connaissances
- Maintenir un environnement accueillant

## Licence

En contribuant, vous acceptez que vos contributions soient sous la même licence que le projet.

---

Merci de contribuer à MobileSec-MS ! 🚀
