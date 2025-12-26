# Guide d'Intégration Jenkins pour MobileSec-MS

Ce guide explique comment configurer un pipeline Jenkins pour analyser automatiquement vos applications Android avec MobileSec-MS.

## Prérequis

1.  **Serveur Jenkins** opérationnel (version 2.x+ recommandée).
2.  **MobileSec-MS** déployé et accessible depuis le serveur Jenkins.
3.  **Plugins Jenkins** installés :
    *   *Pipeline*
    *   *Docker Pipeline* (si vous buildez dans Docker)
    *   *JQ* (installé sur l'agent Jenkins pour parser le JSON)

## Configuration du Pipeline

### 1. Créer un Nouveau Job
1.  Dans Jenkins, cliquez sur **"Nouveau Item"**.
2.  Entrez un nom (ex: `Android-Security-Scan`).
3.  Sélectionnez **"Pipeline"** et cliquez sur OK.

### 2. Configurer le Script Pipeline
Dans la section **"Pipeline"**, choisissez **"Pipeline script from SCM"** si votre `Jenkinsfile` est dans votre repo Git, ou **"Pipeline script"** pour coller le code directement.

Voici le `Jenkinsfile` standard utilisé :

```groovy
pipeline {
    agent any
    
    // Définir l'URL de votre instance MobileSec
    environment {
        MOBILESEC_URL = 'http://votre-serveur-mobilesec:8000' 
    }

    stages {
        stage('Build APK') {
            steps {
                // Votre commande de build Android
                sh './gradlew assembleRelease'
            }
        }

        stage('Security Scan') {
            steps {
                script {
                    // Upload et Scan
                    def response = sh(script: "curl -F 'file=@app/build/outputs/apk/release/app-release.apk' ${MOBILESEC_URL}/scan", returnStdout: true)
                    def jobId = sh(script: "echo '${response}' | jq -r '.job_id'", returnStdout: true).trim()
                    
                    // Attente et Récupération du Rapport
                    sleep 30
                    sh "curl -X POST ${MOBILESEC_URL}/generate -d '{\"job_ids\": {\"apkscanner\": \"${jobId}\"}}' -o report.json"
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                script {
                    // Echec si failles critiques
                    def critical = sh(script: "cat report.json | jq '.summary.critical'", returnStdout: true).trim()
                    if (critical.toInteger() > 0) {
                        error "FAIL: ${critical} failles critiques détectées !"
                    }
                }
            }
        }
    }
}
```

## Automatisations
Pour déclencher le scan à chaque commit :
1.  Allez dans les paramètres du job > **"Ce que déclenche le build"**.
2.  Cochez **"GitHub hook trigger for GITScm polling"**.
3.  Configurez le Webhook dans votre dépôt GitHub vers `http://jenkins-url/github-webhook/`.
