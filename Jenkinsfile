pipeline {
    agent any

    environment {
        MOBILESEC_URL = 'http://mobilesec-ms:8000' // Base URL of your MobileSec platform
        APP_NAME = 'my-android-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build APK') {
            steps {
                script {
                    echo "Building APK..."
                    // Simulation: In a real project, run ./gradlew assembleRelease
                    sh 'mkdir -p build/outputs/apk/release'
                    sh 'touch build/outputs/apk/release/app-release.apk' 
                    // Ensure you have a real APK for testing or use a dummy file
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
                    
                    echo "Critical Issues Found: ${criticalIssues}"
                    
                    if (criticalIssues.toInteger() > 0) {
                        error "Security Gate Failed: ${criticalIssues} critical issues detected."
                    } else {
                        echo "Security Gate Passed."
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'security_report.json', allowEmptyArchive: true
        }
    }
}
