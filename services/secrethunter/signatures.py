import re

# Liste de regex pour détecter les secrets communs
# Format: (Nom du secret, Regex pattern)
SIGNATURES = [
    ("Google API Key", r"AIza[0-9A-Za-z\\-_]{35}"),
    ("AWS Access Key ID", r"AKIA[0-9A-Z]{16}"),
    ("AWS Secret Access Key", r"(?i)aws.+[a-z0-9/+]{40}"),
    ("Generic API Key", r"(?i)(api_key|apikey|access_token|auth_token)[\s]*[:=]+[\s]*['\"]?[0-9a-zA-Z\-_]{16,64}['\"]?"),
    ("Firebase URL", r".*firebaseio\.com"),
    ("Slack Token", r"(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})"),
    ("Facebook Access Token", r"EAACEdEose0cBA[0-9A-Za-z]+"),
    ("Private Key (RSA/DSA)", r"-----BEGIN (RSA|DSA|EC|PGP) PRIVATE KEY-----"),
    ("Hardcoded Password", r"(?i)(password|passwd|pwd)[\s]*[:=]+[\s]*['\"]?[a-zA-Z0-9@#$%^&*]{4,32}['\"]?"),
    ("Email Address", r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
]

def scan_string(content):
    """Retourne une liste de secrets trouvés dans une chaîne."""
    findings = []
    if not content:
        return findings
        
    for name, pattern in SIGNATURES:
        matches = re.findall(pattern, content)
        for match in matches:
            # On évite les faux positifs trop courts ou vides
            if len(match) > 5:
                findings.append({
                    "type": name,
                    "value": match  # Attention: en prod, on obfusque souvent ça (ex: AKIA***)
                })
    return findings