from flask import Flask, request, jsonify, send_file
import os, tempfile, uuid, traceback
from androguard.core.bytecodes.apk import APK
from xml.etree import ElementTree as ET
from utils import init_db, save_scan_result, update_status, get_scan

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 8001))
STORAGE_DIR = os.environ.get("APK_STORAGE_DIR", "/app/uploads")
os.makedirs(STORAGE_DIR, exist_ok=True)

# Initialisation de la base de données au démarrage
init_db()

def analyze_apk(filepath):
    """
    Retourne un dict avec: package, permissions, exported components, flags.
    Gère le parsing XML de manière robuste.
    """
    a = APK(filepath)
    package = a.get_package()
    permissions = sorted(list(a.get_permissions() or []))
    
    # --- 1. Extraction des composants via les méthodes natives Androguard ---
    # (Utilisé pour la structure de base, mais on préfère le XML pour l'attribut 'exported')
    # Note: on ne remplit pas 'comps' ici, on le fera via le parsing XML ci-dessous pour plus de précision.

    # --- 2. Parsing XML Robuste pour 'exported' ---
    manifest_xml = ""
    try:
        axml = a.get_android_manifest_axml()
        if axml:
            manifest_xml = axml.toxml()
    except Exception:
        print("Warning: Could not extract raw XML from AXML")

    exported_components = []
    
    if manifest_xml:
        try:
            # Namespace Android standard
            ANDROID_NS = '{http://schemas.android.com/apk/res/android}'
            
            root = ET.fromstring(manifest_xml)
            component_tags = ["activity", "service", "receiver", "provider"]
            
            for tag in component_tags:
                # Recherche récursive sécurisée
                for elem in root.findall(f".//{tag}"):
                    name = elem.get(f"{ANDROID_NS}name")
                    exported_val = elem.get(f"{ANDROID_NS}exported")
                    
                    if name:
                        is_exported = None
                        if exported_val is not None:
                            is_exported = (exported_val.lower() == "true")
                        
                        exported_components.append({
                            "name": name,
                            "type": tag,
                            "exported": is_exported
                        })
        except Exception as e:
            print(f"Error parsing manifest XML: {e}")
            # En cas d'erreur XML, on continue avec ce qu'on a déjà

    # --- 3. Flags de sécurité ---
    flags = {
        "debuggable": a.is_debuggable(),
        "allowBackup": None,
        "usesCleartextTraffic": None
    }
    try:
        if manifest_xml:
            # Recherche simple de chaînes dans le XML brut pour ces flags
            # C'est une méthode "best effort" si le parsing strict échoue, 
            # ou on peut réutiliser 'root' si disponible.
            flags["allowBackup"] = 'android:allowBackup="true"' in manifest_xml
            flags["usesCleartextTraffic"] = 'android:usesCleartextTraffic="true"' in manifest_xml
    except Exception:
        pass

    return {
        "package": package,
        "permissions": permissions,
        "exported_components": exported_components,
        "flags": flags
    }

@app.route("/health")
def health():
    return jsonify({"status":"ok","service":"apkscanner"})

@app.route("/scan", methods=["POST"])
def scan():
    save_path = None
    try:
        if 'file' not in request.files:
            return jsonify({"error":"no file provided"}), 400
        
        f = request.files['file']
        # Sécurisation basique du nom de fichier ou génération d'UUID
        filename = f.filename or f"{uuid.uuid4().hex}.apk"
        save_path = os.path.join(STORAGE_DIR, filename)
        
        f.save(save_path)

        job_id = "job-" + uuid.uuid4().hex
        
        # 1. Enregistrement initial (statut: queued)
        save_scan_result(job_id, filename, None, "queued", {})
        
        # 2. Passage en 'running'
        update_status(job_id, "running")
        
        try:
            # 3. Analyse Synchrone
            result = analyze_apk(save_path)
            save_scan_result(job_id, filename, result.get("package"), "done", result)
            
            return jsonify({"job_id": job_id, "status":"done"}), 202

        except Exception as e:
            error_msg = str(e)
            trace = traceback.format_exc()
            print(f"Analysis failed for {job_id}: {error_msg}")
            save_scan_result(job_id, filename, None, "failed", {"error": error_msg, "trace": trace})
            return jsonify({"job_id": job_id, "status":"failed", "error": error_msg}), 500

    except Exception as e:
        # Erreur globale (ex: disque plein, erreur I/O avant analyse)
        return jsonify({"error": str(e)}), 500
    
    finally:
        # --- NETTOYAGE AUTOMATIQUE ---
        # Ce bloc s'exécute TOUJOURS, que l'analyse réussisse ou échoue.
        if save_path and os.path.exists(save_path):
            try:
                os.remove(save_path)
                print(f"Cleaned up file: {save_path}")
            except Exception as e:
                print(f"Error deleting file {save_path}: {e}")

@app.route("/scan/<job_id>", methods=["GET"])
def get_job(job_id):
    s = get_scan(job_id)
    if not s:
        return jsonify({"error":"not found"}), 404
    return jsonify(s)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)