from flask import Flask, request, jsonify
from flask_cors import CORS
import os, uuid, json, datetime
from utils import init_db, save_scan, get_scan_result

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PORT = int(os.environ.get("PORT", 8004))

init_db()

# Simulateur d'analyse réseau (en production, utiliser mitmproxy avec AVD)
def analyze_network_behavior(apk_info):
    """
    Simule l'analyse du comportement réseau.
    En production, ceci lancerait un émulateur Android avec mitmproxy.
    """
    findings = []
    
    # Analyse basique basée sur les permissions et manifest
    network_issues = [
        {
            "type": "CLEARTEXT_TRAFFIC",
            "severity": "HIGH",
            "cwe": "CWE-319",
            "description": "Application autorise le trafic HTTP non chiffré",
            "recommendation": "Désactiver cleartextTrafficPermitted dans network_security_config.xml",
            "detected": False
        },
        {
            "type": "WEAK_TLS",
            "severity": "MEDIUM",
            "cwe": "CWE-326",
            "description": "Versions TLS faibles potentiellement supportées",
            "recommendation": "Forcer TLS 1.2+ dans la configuration réseau",
            "detected": False
        },
        {
            "type": "CERTIFICATE_PINNING_MISSING",
            "severity": "MEDIUM",
            "cwe": "CWE-295",
            "description": "Absence de certificate pinning",
            "recommendation": "Implémenter le certificate pinning pour les domaines critiques",
            "detected": True
        },
        {
            "type": "HTTP_ENDPOINTS",
            "severity": "HIGH",
            "cwe": "CWE-319",
            "description": "URLs HTTP détectées dans le code",
            "recommendation": "Migrer tous les endpoints vers HTTPS",
            "detected": False,
            "urls": []
        }
    ]
    
    # En production, mitmproxy analyserait le trafic réel
    # Ici on simule avec des heuristiques
    
    return [issue for issue in network_issues if issue.get("detected", True)]

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "networkinspector"})

@app.route("/scan", methods=["POST"])
def scan():
    """
    Endpoint pour démarrer une analyse réseau.
    En production, ceci lancerait:
    1. Un émulateur Android (AVD)
    2. mitmproxy configuré
    3. Installation et exécution de l'APK
    4. Capture du trafic
    """
    try:
        # Récupération des métadonnées depuis APKScanner
        data = request.get_json()
        if not data:
            return jsonify({"error": "no data provided"}), 400
        
        apk_info = data.get("apk_info", {})
        job_id = "network-" + uuid.uuid4().hex
        
        save_scan(job_id, apk_info.get("package", "unknown"), "running", [])
        
        # Analyse simulée
        issues = analyze_network_behavior(apk_info)
        save_scan(job_id, apk_info.get("package", "unknown"), "done", issues)
        
        return jsonify({
            "job_id": job_id,
            "status": "done",
            "issues_count": len(issues),
            "note": "Network analysis simulated. Production version requires AVD + mitmproxy"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/scan/<job_id>", methods=["GET"])
def get_result(job_id):
    res = get_scan_result(job_id)
    if not res:
        return jsonify({"error": "not found"}), 404
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
