from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PORT = int(os.environ.get("PORT", 8006))

# Base de connaissances MASVS -> Correctifs
MASVS_RULES = {
    "MSTG-STORAGE-8": {
        "title": "Backup désactivé",
        "issue": "allowBackup=true détecté",
        "fix": {
            "file": "AndroidManifest.xml",
            "change": 'android:allowBackup="false"',
            "or": "Créer backup_rules.xml avec exclusions"
        },
        "severity": "MEDIUM"
    },
    "MSTG-RESILIENCE-2": {
        "title": "Mode debug actif",
        "issue": "android:debuggable=true",
        "fix": {
            "file": "AndroidManifest.xml",
            "change": 'Retirer android:debuggable ou mettre "false"',
            "gradle": "Vérifier buildTypes { release { debuggable false } }"
        },
        "severity": "HIGH"
    },
    "MSTG-CODE-2": {
        "title": "Obfuscation désactivée",
        "issue": "ProGuard/R8 non configuré",
        "fix": {
            "file": "build.gradle",
            "change": "minifyEnabled true\nproguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'"
        },
        "severity": "MEDIUM"
    },
    "MSTG-NETWORK-1": {
        "title": "Trafic cleartext autorisé",
        "issue": "usesCleartextTraffic=true",
        "fix": {
            "file": "AndroidManifest.xml",
            "change": 'android:usesCleartextTraffic="false"',
            "additional": "Créer res/xml/network_security_config.xml avec cleartextTrafficPermitted=false"
        },
        "severity": "HIGH"
    },
    "MSTG-STORAGE-1": {
        "title": "Composant exporté non protégé",
        "issue": "exported=true sans permission",
        "fix": {
            "file": "AndroidManifest.xml",
            "change": 'android:exported="false" OU ajouter android:permission="com.example.CUSTOM_PERMISSION"'
        },
        "severity": "HIGH"
    },
    "MSTG-CRYPTO-1": {
        "title": "Algorithme cryptographique faible",
        "issue": "Utilisation de MD5/SHA1/DES/ECB",
        "fix": {
            "code_change": "Remplacer par SHA-256 ou supérieur",
            "example": "MessageDigest.getInstance(\"SHA-256\")\nCipher.getInstance(\"AES/GCM/NoPadding\")"
        },
        "severity": "CRITICAL"
    },
    "MSTG-CRYPTO-2": {
        "title": "Clé codée en dur",
        "issue": "SecretKeySpec avec valeur hardcodée",
        "fix": {
            "code_change": "Utiliser Android Keystore",
            "example": "KeyStore keyStore = KeyStore.getInstance(\"AndroidKeyStore\");"
        },
        "severity": "CRITICAL"
    }
}

def generate_fixes(findings):
    """Génère des suggestions de correctifs basées sur les vulnérabilités détectées"""
    fixes = []
    
    # Analyse des flags APK
    if findings.get("apk"):
        apk_data = findings["apk"].get("result", {})
        flags = apk_data.get("flags", {})
        
        if flags.get("debuggable"):
            fixes.append({
                "masvs": "MSTG-RESILIENCE-2",
                "priority": "HIGH",
                **MASVS_RULES["MSTG-RESILIENCE-2"]
            })
        
        if flags.get("allowBackup"):
            fixes.append({
                "masvs": "MSTG-STORAGE-8",
                "priority": "MEDIUM",
                **MASVS_RULES["MSTG-STORAGE-8"]
            })
        
        if flags.get("usesCleartextTraffic"):
            fixes.append({
                "masvs": "MSTG-NETWORK-1",
                "priority": "HIGH",
                **MASVS_RULES["MSTG-NETWORK-1"]
            })
        
        # Composants exportés
        exported = apk_data.get("exported_components", [])
        exported_unprotected = [c for c in exported if c.get("exported") == True]
        if exported_unprotected:
            fixes.append({
                "masvs": "MSTG-STORAGE-1",
                "priority": "HIGH",
                "components": [c["name"] for c in exported_unprotected[:5]],
                **MASVS_RULES["MSTG-STORAGE-1"]
            })
    
    # Analyse crypto
    if findings.get("crypto"):
        crypto_findings = findings["crypto"].get("findings", [])
        crypto_critical = [f for f in crypto_findings if f.get("severity") == "CRITICAL"]
        
        if any("WEAK_HASH" in f.get("type", "") or "DES" in f.get("type", "") or "ECB" in f.get("type", "") for f in crypto_findings):
            fixes.append({
                "masvs": "MSTG-CRYPTO-1",
                "priority": "CRITICAL",
                **MASVS_RULES["MSTG-CRYPTO-1"]
            })
        
        if any("HARDCODED_KEY" in f.get("type", "") for f in crypto_findings):
            fixes.append({
                "masvs": "MSTG-CRYPTO-2",
                "priority": "CRITICAL",
                **MASVS_RULES["MSTG-CRYPTO-2"]
            })
    
    # Analyse secrets
    if findings.get("secrets"):
        secret_findings = findings["secrets"].get("findings", [])
        if len(secret_findings) > 0:
            fixes.append({
                "masvs": "MSTG-STORAGE-14",
                "priority": "CRITICAL",
                "title": "Secrets exposés",
                "issue": f"{len(secret_findings)} secrets détectés dans le code",
                "fix": {
                    "action": "Retirer tous les secrets du code source",
                    "alternatives": [
                        "Utiliser des variables d'environnement",
                        "Implémenter un service backend pour gérer les clés",
                        "Utiliser Android NDK pour obfusquer les secrets critiques"
                    ]
                },
                "severity": "CRITICAL"
            })
    
    return fixes

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "fixsuggest"})

@app.route("/suggest", methods=["POST"])
def suggest():
    """
    Reçoit les résultats agrégés et génère des suggestions de correctifs
    """
    try:
        findings = request.get_json()
        
        if not findings:
            return jsonify({"error": "no findings provided"}), 400
        
        fixes = generate_fixes(findings)
        
        # Trier par priorité
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        fixes.sort(key=lambda x: priority_order.get(x.get("priority", "LOW"), 4))
        
        response = {
            "total_fixes": len(fixes),
            "critical": sum(1 for f in fixes if f.get("priority") == "CRITICAL"),
            "high": sum(1 for f in fixes if f.get("priority") == "HIGH"),
            "fixes": fixes,
            "compliance": {
                "owasp_masvs": "https://mobile-security.gitbook.io/masvs/",
                "cwe": "https://cwe.mitre.org/",
                "nist": "https://www.nist.gov/itl/applied-cybersecurity/mobile-security"
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/patch/<masvs_id>", methods=["GET"])
def get_patch_details(masvs_id):
    """Retourne les détails d'un correctif spécifique"""
    rule = MASVS_RULES.get(masvs_id)
    if not rule:
        return jsonify({"error": "rule not found"}), 404
    
    return jsonify({
        "masvs_id": masvs_id,
        **rule
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
