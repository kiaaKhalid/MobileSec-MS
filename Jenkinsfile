pipeline {
    agent any

    environment {
        // Jenkins tourne sur Mac, MobileSec aussi (ports 8001, 8005...) -> localhost est parfait.
        MOBILESEC_URL = 'http://localhost:8000' 
    }

    parameters {
        string(name: 'APK_PATH', defaultValue: '/Users/kiaakhalidgmail/Project/MobileSec-MS/examples/apks/Hunter.apk', description: 'Chemin ABSOLU vers votre APK local. Par défaut: Hunter.apk')
    }

    stages {
        // --- PAS D'ETAPE CHECKOUT (car on est en mode Script direct) ---

        stage('Build APK') {
            steps {
                script {
                    if (params.APK_PATH != '' && fileExists(params.APK_PATH)) {
                        echo "Utilisation de l'APK réel : ${params.APK_PATH}"
                        sh "mkdir -p build/outputs/apk/release"
                        sh "cp '${params.APK_PATH}' build/outputs/apk/release/app-release.apk"
                    } else {
                        echo "⚠️ FICHIER NON TROUVÉ : ${params.APK_PATH}"
                        echo "-> Création d'un APK vide pour simuler le pipeline."
                        sh 'mkdir -p build/outputs/apk/release'
                        sh 'touch build/outputs/apk/release/app-release.apk' 
                    }
                }
            }
        }

        stage('Code Quality') {
            steps {
                script {
                    echo "🚀 Lancement de l'Analyse SonarQube..."
                    // Utilisation de l'image sonar-scanner pour analyser le code
                    // On connecte le conteneur au réseau mobilesec-network pour qu'il voit le serveur sonarqube
                    // On pointe vers http://sonarqube:9000 car ils sont sur le même réseau Docker
                    sh """
                        docker run --rm \
                        --network mobilesec-network \
                        -e SONAR_HOST_URL=http://sonarqube:9000 \
                        -e SONAR_LOGIN=\${SONAR_TOKEN} \
                        -v "\$(pwd):/usr/src" \
                        sonarsource/sonar-scanner-cli \
                        -Dsonar.projectKey=mobilesec-ms
                    """
                }
            }
        }

        stage('Security Scan') {
            steps {
                script {
                    echo "Lancement du Scan MobileSec..."
                    
                    // 1. Envoyer l'APK au Scanner via LOCALHOST
                    def scanResponse = sh(script: """
                        curl -s -X POST -F "file=@build/outputs/apk/release/app-release.apk" \
                        http://localhost:8001/scan
                    """, returnStdout: true).trim()
                    
                    echo "Réponse du Scan: ${scanResponse}"
                    
                    def jobId = sh(script: "echo '${scanResponse}' | jq -r '.job_id'", returnStdout: true).trim()
                    
                    if (jobId == "null" || jobId == "") {
                        error "Erreur: Impossible de récupérer le Job ID."
                    }
                    
                    echo "Job ID: ${jobId}"
                    
                    echo "Analyse en cours..."
                    sleep 10 
                    
                    // 3. Générer le rapport via ReportGen (LOCALHOST)
                     def reportResponse = sh(script: """
                        curl -s -X POST http://localhost:8005/generate \
                        -H "Content-Type: application/json" \
                        -d '{"job_ids": {"apkscanner": "${jobId}"}}'
                    """, returnStdout: true).trim()
                    echo "Rapport Généré."
                    
                    writeFile file: 'security_report.json', text: reportResponse
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    def criticalIssues = sh(script: "cat security_report.json | jq '.summary.critical'", returnStdout: true).trim()
                    
                    echo "Failles Critiques: ${criticalIssues}"
                    
                    if (criticalIssues.toInteger() > 0) {
                        error "ECHEC: ${criticalIssues} failles critiques détectées !"
                    } else {
                        echo "SUCCES: Aucune faille critique."
                    }
                }
            }
        }
    }
}
