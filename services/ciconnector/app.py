from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PORT = int(os.environ.get("PORT", 8007))

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ciconnector"})

@app.route("/github-action", methods=["GET"])
def generate_github_action():
    """Génère un workflow GitHub Actions YAML"""
    workflow = """name: Mobile Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Build APK
      run: |
        ./gradlew assembleRelease
    
    - name: Run MobileSec-MS Scan
      run: |
        # Scanner l'APK
        SCAN_ID=$(curl -X POST -F "file=@app/build/outputs/apk/release/app-release.apk" \\
          http://mobilesec-ms.example.com:8001/scan | jq -r '.job_id')
        
        echo "Scan ID: $SCAN_ID"
        
        # Attendre les résultats
        sleep 30
        
        # Récupérer le rapport
        curl -X POST http://mobilesec-ms.example.com:8005/generate \\
          -H "Content-Type: application/json" \\
          -d "{\\"job_ids\\": {\\"apkscanner\\": \\"$SCAN_ID\\"}}" \\
          -o security-report.json
    
    - name: Upload Security Report
      uses: actions/upload-artifact@v3
      with:
        name: security-report
        path: security-report.json
    
    - name: Check for Critical Issues
      run: |
        CRITICAL=$(cat security-report.json | jq '.summary.critical')
        if [ "$CRITICAL" -gt 0 ]; then
          echo "::error::$CRITICAL critical security issues found!"
          exit 1
        fi
"""
    return workflow, 200, {'Content-Type': 'text/plain'}

@app.route("/gitlab-ci", methods=["GET"])
def generate_gitlab_ci():
    """Génère un fichier .gitlab-ci.yml"""
    gitlab_ci = """stages:
  - build
  - security
  - report

build:
  stage: build
  image: openjdk:11
  script:
    - ./gradlew assembleRelease
  artifacts:
    paths:
      - app/build/outputs/apk/release/app-release.apk
    expire_in: 1 hour

security_scan:
  stage: security
  image: curlimages/curl:latest
  script:
    - |
      # Scan APK
      SCAN_ID=$(curl -X POST -F "file=@app/build/outputs/apk/release/app-release.apk" \\
        http://mobilesec-ms:8001/scan | jq -r '.job_id')
      
      # Scan secrets
      SECRET_ID=$(curl -X POST -F "file=@app/build/outputs/apk/release/app-release.apk" \\
        http://mobilesec-ms:8002/scan | jq -r '.job_id')
      
      # Scan crypto
      CRYPTO_ID=$(curl -X POST -F "file=@app/build/outputs/apk/release/app-release.apk" \\
        http://mobilesec-ms:8003/scan | jq -r '.job_id')
      
      # Wait for completion
      sleep 60
      
      # Generate report
      curl -X POST http://mobilesec-ms:8005/generate \\
        -H "Content-Type: application/json" \\
        -d "{
          \\"job_ids\\": {
            \\"apkscanner\\": \\"$SCAN_ID\\",
            \\"secrethunter\\": \\"$SECRET_ID\\",
            \\"cryptocheck\\": \\"$CRYPTO_ID\\"
          }
        }" > security-report.json
      
      # Get SARIF for GitLab
      curl -X POST "http://mobilesec-ms:8005/generate?format=sarif" \\
        -H "Content-Type: application/json" \\
        -d "{
          \\"job_ids\\": {
            \\"apkscanner\\": \\"$SCAN_ID\\",
            \\"secrethunter\\": \\"$SECRET_ID\\",
            \\"cryptocheck\\": \\"$CRYPTO_ID\\"
          }
        }" > gl-sast-report.json
  artifacts:
    reports:
      sast: gl-sast-report.json
    paths:
      - security-report.json

security_gate:
  stage: report
  script:
    - |
      CRITICAL=$(cat security-report.json | jq '.summary.critical')
      HIGH=$(cat security-report.json | jq '.summary.high')
      
      echo "Critical issues: $CRITICAL"
      echo "High issues: $HIGH"
      
      if [ "$CRITICAL" -gt 0 ]; then
        echo "FAIL: Critical security issues detected"
        exit 1
      fi
      
      if [ "$HIGH" -gt 5]; then
        echo "WARN: Too many high severity issues"
        exit 1
      fi
  dependencies:
    - security_scan
"""
    return gitlab_ci, 200, {'Content-Type': 'text/plain'}

@app.route("/docker-cli", methods=["GET"])
def generate_docker_cli():
    """Génère des commandes Docker pour exécution locale"""
    commands = {
        "description": "Commandes Docker pour scanner un APK localement",
        "commands": [
            {
                "step": 1,
                "name": "Démarrer les services",
                "command": "docker-compose up -d"
            },
            {
                "step": 2,
                "name": "Scanner l'APK",
                "command": "curl -X POST -F 'file=@/path/to/app.apk' http://localhost:8001/scan"
            },
            {
                "step": 3,
                "name": "Récupérer les résultats",
                "command": "curl http://localhost:8001/scan/{job_id}"
            },
            {
                "step": 4,
                "name": "Générer le rapport complet",
                "command": "curl -X POST http://localhost:8005/generate -H 'Content-Type: application/json' -d '{\"job_ids\": {\"apkscanner\": \"job-xxx\"}}'"
            },
            {
                "step": 5,
                "name": "Générer le rapport PDF",
                "command": "curl -X POST 'http://localhost:8005/generate?format=pdf' -H 'Content-Type: application/json' -d '{\"job_ids\": {\"apkscanner\": \"job-xxx\"}}' -o report.pdf"
            }
        ]
    }
    return jsonify(commands), 200

@app.route("/integration-guide", methods=["GET"])
def integration_guide():
    """Retourne un guide d'intégration complet"""
    guide = {
        "title": "Guide d'intégration MobileSec-MS",
        "platforms": {
            "github_actions": {
                "file": ".github/workflows/security.yml",
                "endpoint": "/github-action",
                "documentation": "https://docs.github.com/en/actions"
            },
            "gitlab_ci": {
                "file": ".gitlab-ci.yml",
                "endpoint": "/gitlab-ci",
                "documentation": "https://docs.gitlab.com/ee/ci/"
            },
            "jenkins": {
                "description": "Utiliser le plugin Docker et exécuter les commandes via shell",
                "endpoint": "/docker-cli"
            },
            "azure_devops": {
                "description": "Utiliser une tâche Docker personnalisée",
                "pipeline": "azure-pipelines.yml"
            }
        },
        "services_endpoints": {
            "apkscanner": "http://localhost:8001",
            "secrethunter": "http://localhost:8002",
            "cryptocheck": "http://localhost:8003",
            "networkinspector": "http://localhost:8004",
            "reportgen": "http://localhost:8005",
            "fixsuggest": "http://localhost:8006"
        },
        "workflow": [
            "1. Build votre APK dans votre pipeline",
            "2. POST /scan sur chaque service d'analyse",
            "3. Attendre la complétion (polling ou webhook)",
            "4. POST /generate sur ReportGen avec tous les job_ids",
            "5. Optionnel: POST /suggest sur FixSuggest",
            "6. Fail le build si critical > 0"
        ]
    }
    return jsonify(guide), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
