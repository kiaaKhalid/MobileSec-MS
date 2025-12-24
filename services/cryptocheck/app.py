from flask import Flask, request, jsonify
from flask_cors import CORS
import os, uuid, re, traceback
from androguard.core.apk import APK
from androguard.core.dex import DEX
from androguard.core.analysis.analysis import Analysis
from utils import init_db, save_scan, get_scan_result, get_all_scans

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PORT = int(os.environ.get("PORT", 8003))
STORAGE_DIR = "/app/uploads"
os.makedirs(STORAGE_DIR, exist_ok=True)

init_db()

# Patterns de vulnérabilités cryptographiques
CRYPTO_PATTERNS = {
    "ECB_MODE": {
        "pattern": r"AES/ECB",
        "severity": "HIGH",
        "cwe": "CWE-327",
        "description": "Mode ECB détecté - non sécurisé, utiliser CBC/GCM",
        "recommendation": "Utiliser AES/CBC/PKCS5Padding ou AES/GCM/NoPadding"
    },
    "WEAK_HASH_MD5": {
        "pattern": r"MessageDigest\.getInstance\(['\"]MD5['\"]\)",
        "severity": "HIGH",
        "cwe": "CWE-328",
        "description": "Algorithme MD5 détecté - cryptographiquement cassé",
        "recommendation": "Utiliser SHA-256 ou SHA-3"
    },
    "WEAK_HASH_SHA1": {
        "pattern": r"MessageDigest\.getInstance\(['\"]SHA-1['\"]\)",
        "severity": "MEDIUM",
        "cwe": "CWE-328",
        "description": "Algorithme SHA-1 détecté - faible",
        "recommendation": "Utiliser SHA-256 ou supérieur"
    },
    "WEAK_RANDOM": {
        "pattern": r"java\.util\.Random",
        "severity": "MEDIUM",
        "cwe": "CWE-338",
        "description": "java.util.Random utilisé - non cryptographiquement sécurisé",
        "recommendation": "Utiliser java.security.SecureRandom"
    },
    "DES_ALGORITHM": {
        "pattern": r"DES/",
        "severity": "HIGH",
        "cwe": "CWE-327",
        "description": "Algorithme DES détecté - obsolète et faible",
        "recommendation": "Utiliser AES-256"
    },
    "NO_PADDING": {
        "pattern": r"AES/.*/NoPadding",
        "severity": "LOW",
        "cwe": "CWE-326",
        "description": "NoPadding détecté - peut exposer des informations",
        "recommendation": "Vérifier que le padding est géré manuellement correctement"
    },
    "HARDCODED_KEY": {
        "pattern": r"(SecretKeySpec|IvParameterSpec)\s*\(\s*[\"'][\w+/=]{16,}[\"']",
        "severity": "CRITICAL",
        "cwe": "CWE-321",
        "description": "Clé cryptographique codée en dur détectée",
        "recommendation": "Utiliser Android Keystore pour stocker les clés"
    },
    "SSL_VALIDATION_DISABLED": {
        "pattern": r"TrustAllCerts|X509TrustManager.*checkServerTrusted.*\{\s*\}",
        "severity": "CRITICAL",
        "cwe": "CWE-295",
        "description": "Validation SSL/TLS désactivée",
        "recommendation": "Toujours valider les certificats SSL"
    }
}

def analyze_crypto_issues(filepath):
    """Analyse les problèmes cryptographiques dans l'APK"""
    findings = []
    
    try:
        apk = APK(filepath)
        
        # Analyser tous les fichiers DEX
        for dex_bytes in apk.get_all_dex():
            try:
                d = DEX(dex_bytes)
                dx = Analysis()
                dx.add(d)
                dx.create_xref()
                
                # Analyser toutes les méthodes
                for method in d.get_methods():
                    if method.get_code():
                        try:
                            # Récupérer le code source
                            method_name = f"{method.get_class_name()}.{method.get_name()}"
                            
                            # Convertir en texte pour l'analyse
                            code_text = method.get_source() if hasattr(method, 'get_source') else ""
                            
                            # Vérifier chaque pattern
                            for vuln_name, vuln_data in CRYPTO_PATTERNS.items():
                                if re.search(vuln_data["pattern"], code_text, re.IGNORECASE):
                                    findings.append({
                                        "type": vuln_name,
                                        "severity": vuln_data["severity"],
                                        "cwe": vuln_data["cwe"],
                                        "description": vuln_data["description"],
                                        "recommendation": vuln_data["recommendation"],
                                        "location": method_name,
                                        "class": method.get_class_name()
                                    })
                        except Exception as e:
                            continue
                
                # Analyser aussi les strings pour détecter les patterns
                for string_value in d.get_strings():
                    for vuln_name, vuln_data in CRYPTO_PATTERNS.items():
                        if re.search(vuln_data["pattern"], string_value, re.IGNORECASE):
                            findings.append({
                                "type": vuln_name,
                                "severity": vuln_data["severity"],
                                "cwe": vuln_data["cwe"],
                                "description": vuln_data["description"],
                                "recommendation": vuln_data["recommendation"],
                                "location": "string_constant",
                                "value": string_value[:100]  # Limiter la taille
                            })
            except Exception as e:
                print(f"Error processing DEX: {e}")
                continue
        
        # Dédupliquer les résultats
        unique_findings = []
        seen = set()
        for f in findings:
            key = f"{f['type']}:{f.get('location', '')}"
            if key not in seen:
                unique_findings.append(f)
                seen.add(key)
        
        # Trier par sévérité
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        unique_findings.sort(key=lambda x: severity_order.get(x["severity"], 4))
        
        return unique_findings
        
    except Exception as e:
        print(f"Error analyzing crypto: {e}")
        traceback.print_exc()
        return []

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "cryptocheck"})

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

        job_id = "crypto-" + uuid.uuid4().hex
        save_scan(job_id, filename, "running", [])

        # Analyse
        issues = analyze_crypto_issues(save_path)
        save_scan(job_id, filename, "done", issues)

        return jsonify({
            "job_id": job_id, 
            "status": "done", 
            "issues_count": len(issues),
            "critical_count": sum(1 for x in issues if x["severity"] == "CRITICAL"),
            "high_count": sum(1 for x in issues if x["severity"] == "HIGH")
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
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

@app.route("/scans", methods=["GET"])
def list_scans():
    try:
        scans = get_all_scans()
        return jsonify(scans)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
