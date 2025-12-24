from flask import Flask, request, jsonify
from flask_cors import CORS
import os, uuid, re, hashlib, traceback
from androguard.core.apk import APK
from androguard.core.dex import DEX
from utils import init_db, save_result, get_result, get_all_scans
from signatures import scan_string

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PORT = int(os.environ.get("PORT", 8002)) # Port 8002 pour SecretHunter
STORAGE_DIR = "/app/uploads"
os.makedirs(STORAGE_DIR, exist_ok=True)

init_db()

def extract_and_scan(filepath):
    """Extrait les chaînes du DEX et des ressources XML et les scanne."""
    findings = []
    try:
        a = APK(filepath)
        
        # Scan du code (Classes.dex) - C'est là que sont les secrets hardcodés
        for dex_bytes in a.get_all_dex():
            try:
                d = DEX(dex_bytes)
                # d.get_strings() retourne toutes les constantes string du code
                for s in d.get_strings():
                    if s and len(s) > 5: # Ignore les chaines trop courtes
                        res = scan_string(s)
                        if res:
                            findings.extend(res)
            except Exception as e:
                print(f"Error processing DEX: {e}")
                        
    except Exception as e:
        print(f"Error extracting APK: {e}")
        traceback.print_exc()
        
    # Déduplication des résultats
    unique_findings = []
    seen = set()
    for f in findings:
        identifier = f"{f['type']}:{f['value']}"
        if identifier not in seen:
            unique_findings.append(f)
            seen.add(identifier)
            
    return unique_findings

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "secrethunter"})

@app.route("/scan", methods=["POST"])
def scan():
    save_path = None
    try:
        if 'file' not in request.files:
            return jsonify({"error": "no file provided"}), 400
        f = request.files['file']
        filename = f.filename or f"{uuid.uuid4().hex}.apk"
        save_path = os.path.join(STORAGE_DIR, filename)
        f.save(save_path)

        job_id = "secret-" + uuid.uuid4().hex
        save_result(job_id, filename, "running", [])

        # Analyse synchrone (pour MVP)
        secrets = extract_and_scan(save_path)
        save_result(job_id, filename, "done", secrets)

        return jsonify({"job_id": job_id, "status": "done", "secrets_count": len(secrets)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if save_path and os.path.exists(save_path):
            os.remove(save_path)

@app.route("/scan/<job_id>", methods=["GET"])
def get_scan(job_id):
    res = get_result(job_id)
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