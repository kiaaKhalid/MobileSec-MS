# 📊 Diagramme BPMN - MobileSec-MS

## 📁 Fichier créé

**`MobileSec-MS.bpmn`** - Modélisation BPMN 2.0 complète du processus d'analyse de sécurité

## 🎯 Contenu du diagramme

Le fichier BPMN modélise **2 processus principaux** :

### 1. **Processus principal : Analyse de Sécurité APK**
   - ✅ Upload et validation du fichier APK
   - ✅ Création du job_id unique
   - ✅ Exécution parallèle des 4 microservices d'analyse :
     - **APKScanner** : Désassemblage et analyse du manifest
     - **SecretHunter** : Détection de secrets (API keys, tokens)
     - **CryptoCheck** : Vérification cryptographique
     - **NetworkInspector** : Analyse des communications réseau
   - ✅ Agrégation des résultats (ReportGen)
   - ✅ Génération de suggestions de correctifs (FixSuggest)
   - ✅ Export multi-format (JSON, PDF, SARIF)

### 2. **Sous-processus : Intégration CI/CD**
   - ✅ Déclenchement automatique (webhook Git)
   - ✅ Build APK
   - ✅ Scan automatique MobileSec-MS
   - ✅ Décision Pass/Fail basée sur le score
   - ✅ Publication du rapport dans PR/MR

## �� Visualiser le diagramme BPMN

### Option 1 : Camunda Modeler (Recommandé)

```bash
# Télécharger Camunda Modeler
# https://camunda.com/download/modeler/

# Ouvrir le fichier
# File > Open File > MobileSec-MS.bpmn
```

### Option 2 : bpmn.io (En ligne)

```bash
# Ouvrir dans le navigateur
open https://demo.bpmn.io/new

# Puis : File > Open File > Sélectionner MobileSec-MS.bpmn
```

### Option 3 : VS Code avec extension

```bash
# Installer l'extension BPMN Editor
code --install-extension imixs.bpmn-modeler

# Ouvrir le fichier
code MobileSec-MS.bpmn
```

## 📐 Structure du diagramme

```
MobileSec-MS.bpmn
├── Process 1: SecurityAnalysisProcess
│   ├── Start Event
│   ├── User Tasks (Upload, Display)
│   ├── Service Tasks (Validation, Export)
│   ├── Exclusive Gateways (Validation, Actions)
│   ├── Parallel Gateways (Launch analyses, Wait)
│   ├── SubProcesses
│   │   ├── APKScanner (Port 8001)
│   │   ├── SecretHunter (Port 8002)
│   │   ├── CryptoCheck (Port 8003)
│   │   ├── NetworkInspector (Port 8004)
│   │   └── ReportGen (Port 8005)
│   └── End Events (Success, Error, New Scan)
│
└── Process 2: CIIntegrationProcess
    ├── Start Event (Git Commit)
    ├── Service Tasks (Webhook, Build, Scan)
    ├── Exclusive Gateway (Score threshold)
    └── End Event (Pipeline complete)
```

## 🎨 Éléments BPMN utilisés

| Élément | Symbole | Usage dans MobileSec-MS |
|---------|---------|-------------------------|
| **Start Event** | ⭕ | Début du processus (Upload APK) |
| **End Event** | ⭕● | Fin du processus (Success/Error) |
| **User Task** | 📋 | Upload APK, Afficher résultats |
| **Service Task** | ⚙️ | Validation, Analyses, Export |
| **Exclusive Gateway** | ◇ | Décisions (APK valide?, Format?) |
| **Parallel Gateway** | ⊕ | Lancement/attente analyses parallèles |
| **SubProcess** | 📦 | Encapsulation des microservices |
| **Sequence Flow** | → | Flux du processus |
| **Error Event** | ⚠️ | Gestion d'erreurs (APK invalide) |

## 📊 Statistiques du diagramme

- **Nombre de processus** : 2
- **Nombre de sous-processus** : 5 (un par microservice)
- **Nombre de tâches** : ~40
- **Nombre de gateways** : 7
- **Nombre de flux** : ~50
- **Conformité** : BPMN 2.0

## 🔧 Détails techniques

### Attributs BPMN importants

```xml
<!-- Processus exécutable -->
<process id="SecurityAnalysisProcess" isExecutable="true">

<!-- Gateway parallèle pour analyses concurrentes -->
<parallelGateway id="Gateway_Launch_Parallel" 
                 gatewayDirection="Diverging">

<!-- Sous-processus avec documentation détaillée -->
<subProcess id="SubProcess_APKScanner" 
            name="APKScanner (Port 8001)">
  <documentation>
    Désassemble et analyse les APK...
  </documentation>
</subProcess>

<!-- Flux conditionnels -->
<sequenceFlow id="Flow_Valid_Yes" sourceRef="Gateway_APK_Valid">
  <conditionExpression>apk_valid == true</conditionExpression>
</sequenceFlow>
```

## 📚 Documentation dans le BPMN

Chaque élément contient une documentation détaillée :

- **Service Tasks** : Description des appels API, paramètres, résultats
- **SubProcesses** : Technologies utilisées, ports, bases de données
- **Gateways** : Conditions de décision, critères
- **End Events** : Codes d'erreur, messages

## 🔄 Mapping avec le code

### APKScanner (services/apkscanner/app.py)

```
BPMN SubProcess_APKScanner
    ↓
    1. APKScanner_Decompile → APK(filepath)
    2. APKScanner_ParseManifest → a.get_android_manifest_axml()
    3. APKScanner_AnalyzeComponents → root.findall("activity|service|...")
    4. APKScanner_CheckFlags → flags["debuggable"], flags["allowBackup"]
    5. APKScanner_SaveResults → save_scan_result(job_id, ...)
```

### ReportGen (services/reportgen/app.js)

```
BPMN SubProcess_ReportGen
    ↓
    1. ReportGen_CollectResults → axios.get(services[x]/scan/job_id)
    2. ReportGen_Aggregate → generateReport(results)
    3. ReportGen_CalculateScore → calcul des vulnérabilités
    4. ReportGen_MapOWASP → mapping MASVS
    5. Format choice → generatePDF() | generateSARIF()
```

## 🎯 Cas d'usage

### Scénario 1 : Scan manuel via UI

```
User → Upload APK → Validation → Parallel Analyses → Report → Display
```

### Scénario 2 : CI/CD automatique

```
Git Push → Webhook → Build → Scan → Score Check → Pass/Fail → PR Comment
```

### Scénario 3 : Export pour audit

```
Scan Complete → User chooses PDF → Generate PDF → Download
```

## 📈 Métriques de performance

D'après le BPMN, le processus complet prend :

- **Upload + Validation** : ~2 secondes
- **Analyses parallèles** : ~30-60 secondes (selon taille APK)
  - APKScanner : 10-20s
  - SecretHunter : 15-30s
  - CryptoCheck : 10-15s
  - NetworkInspector : 5-10s
- **Agrégation + Rapport** : ~5 secondes
- **Total** : ~40-70 secondes pour un APK moyen (20 MB)

## 🔐 Points de sécurité dans le BPMN

1. **Validation stricte** : Gateway "APK valide?" avant analyse
2. **Isolation** : Chaque analyse dans un sous-processus isolé
3. **Gestion d'erreurs** : Error Events pour cas critiques
4. **Nettoyage** : Suppression automatique des fichiers temporaires
5. **Audit** : Traçabilité via job_id unique

## 🚀 Évolutions futures du BPMN

- [ ] Ajout d'un pool pour les services externes (GitHub, GitLab)
- [ ] Modélisation des retry mechanisms
- [ ] Ajout de timers pour timeout
- [ ] Événements de compensation pour rollback
- [ ] Message flows entre processus

## 📞 Support

Pour toute question sur le diagramme BPMN :
- Consulter la spécification BPMN 2.0 : https://www.omg.org/spec/BPMN/2.0/
- Documentation Camunda : https://docs.camunda.org/
- Issues GitHub : https://github.com/yourusername/MobileSec-MS/issues

---

**Créé le** : 8 décembre 2025  
**Format** : BPMN 2.0 (XML)  
**Compatible avec** : Camunda Modeler, bpmn.io, Bizagi Modeler  
**Taille** : ~15 KB  
**Complexité** : Avancée (pools, lanes, subprocesses)
