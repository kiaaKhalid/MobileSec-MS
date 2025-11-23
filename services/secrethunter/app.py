from flask import Flask, request, jsonify
import os, uuid, traceback
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from utils import init_db, save_scan, get_scan_result
from signatures import scan_string

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 8002)) # Port 8002 pour SecretHunter
STORAGE_DIR = "/app/uploads"
os.makedirs(STORAGE_DIR, exist_ok=True)

init_db()

def extract_and_scan(filepath):
    """Extrait les chaînes du DEX et des ressources XML et les scanne."""
    findings = []
    try:
        a = APK(filepath)
        
        # 1. Scan des ressources (strings.xml, etc.)
        # Androguard décrypte le binaire XML automatiquement
        resources_check = ["app_name", "google_api_key", "firebase_database_url"] # Exemples de clés ressources
        pkg = a.get_package()
        
        # On récupère toutes les chaînes définies dans resources.arsc
        res_parser = a.get_android_resources()
        if res_parser:
            try:
                # Récupération brute des strings ressources
                for package_name in res_parser.get_packages_names():
                    pkg_obj = res_parser.get_packages_names()[package_name]
                    # (Simplification pour MVP: on ne parcourt pas tout l'arbre complexe, 
                    # on compte sur le scan des classes DEX qui contiennent souvent les secrets hardcodés)
            except Exception:
                pass

        # 2. Scan du code (Classes.dex) - C'est là que sont les secrets hardcodés
        for dex in a.get_all_dex():
            d = DalvikVMFormat(dex)
            # d.get_strings() retourne toutes les constantes string du code
            for s in d.get_strings():
                if s and len(s) > 5: # Ignore les chaines trop courtes
                    res = scan_string(s)
                    if res:
                        findings.extend(res)
                        
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
        save_scan(job_id, filename, "running", [])

        # Analyse synchrone (pour MVP)
        secrets = extract_and_scan(save_path)
        save_scan(job_id, filename, "done", secrets)

        return jsonify({"job_id": job_id, "status": "done", "secrets_count": len(secrets)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if save_path and os.path.exists(save_path):
            os.remove(save_path)

@app.route("/scan/<job_id>", methods=["GET"])
def get_result(job_id):
    res = get_scan_result(job_id)
    if not res:
        return jsonify({"error": "not found"}), 404
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)