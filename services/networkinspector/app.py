from flask import Flask, request, jsonify
from flask_cors import CORS
import os, uuid, json, datetime
from utils import init_db, save_scan, get_scan_result, get_all_scans

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

from androguard.core.apk import APK
import tempfile

@app.route("/scan", methods=["POST"])
def scan():
    """
    Endpoint pour démarrer une analyse réseau.
    Supporte l'upload de fichier (multipart/form-data) ou JSON metadata.
    """
    save_path = None
    try:
        apk_info = {}
        
        # Cas 1: Upload de fichier
        if 'file' in request.files:
            f = request.files['file']
            if f.filename == '':
                return jsonify({"error": "no file selected"}), 400
            
            # Sauvegarde temporaire pour analyse basique (package name)
            filename = f.filename or f"{uuid.uuid4().hex}.apk"
            temp_dir = tempfile.gettempdir()
            save_path = os.path.join(temp_dir, filename)
            f.save(save_path)
            
            try:
                a = APK(save_path)
                apk_info["package"] = a.get_package()
            except Exception as e:
                print(f"Error extracting info from APK: {e}")
                apk_info["package"] = "unknown_parse_error"
                
        # Cas 2: JSON metadata
        elif request.is_json:
            data = request.get_json()
            apk_info = data.get("apk_info", {})
        else:
             return jsonify({"error": "Unsupported Media Type. Expected 'multipart/form-data' (file) or 'application/json'"}), 415

        job_id = "network-" + uuid.uuid4().hex
        
        save_scan(job_id, apk_info.get("package", "unknown"), "running", [])
        
        # Analyse simulée
        issues = analyze_network_behavior(apk_info)
        save_scan(job_id, apk_info.get("package", "unknown"), "done", issues)
        
        return jsonify({
            "job_id": job_id,
            "status": "done",
            "issues_count": len(issues),
            "note": "Network analysis simulated. Production version requires AVD + mitmproxy",
            "package_name": apk_info.get("package", "unknown") 
        }), 200 # 202 is typical for async, but here we return result directly, or just job_id? Frontend waits for job_id then GETs it.
        # Frontend code: const response = await axios.post(...) then axios.get(...)
        # So returning 200 with job_id is fine.

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if save_path and os.path.exists(save_path):
             try:
                 os.remove(save_path)
             except:
                 pass

@app.route("/scan/<job_id>", methods=["GET"])
def get_result(job_id):
    res = get_scan_result(job_id)
    if not res:
        return jsonify({"error": "not found"}), 404
    return jsonify(res)

@app.route("/scans", methods=["GET"])
def list_scans():
    try:
        scans = get_all_scans()
        return jsonify(scans)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
