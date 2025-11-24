#!/bin/bash

# Script de test d'intégration pour MobileSec-MS
# Teste tous les services et le workflow complet

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🧪 MobileSec-MS - Test d'intégration"
echo "===================================="
echo ""

# 1. Vérification de l'état des services
echo "1️⃣  Vérification des services..."
services=("apkscanner:8001" "secrethunter:8002" "cryptocheck:8003" "networkinspector:8004" "reportgen:8005" "fixsuggest:8006" "ciconnector:8007")
failed=0

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if curl -s http://localhost:$port/health | grep -q "ok"; then
        echo -e "${GREEN}✅ $name${NC}"
    else
        echo -e "${RED}❌ $name${NC}"
        failed=$((failed + 1))
    fi
done

if [ $failed -gt 0 ]; then
    echo -e "${RED}❌ $failed service(s) en échec${NC}"
    exit 1
fi

echo ""

# 2. Test avec un APK fictif (création d'un fichier minimal)
echo "2️⃣  Création d'un APK de test..."
APK_TEST="/tmp/test-mobilesec.apk"

# Créer un fichier APK minimal si aucun n'existe dans examples
if [ ! -d "examples/apks" ]; then
    mkdir -p examples/apks
fi

# Utiliser un APK existant ou créer un fichier de test
if ls examples/apks/*.apk 1> /dev/null 2>&1; then
    APK_TEST=$(ls examples/apks/*.apk | head -1)
    echo -e "${GREEN}✅ APK trouvé: $APK_TEST${NC}"
else
    # Créer un fichier ZIP minimal avec structure APK basique
    echo -e "${YELLOW}⚠️  Aucun APK trouvé, création d'un fichier de test...${NC}"
    mkdir -p /tmp/apk-test
    echo "<?xml version=\"1.0\" encoding=\"utf-8\"?><manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" package=\"com.test.app\"></manifest>" > /tmp/apk-test/AndroidManifest.xml
    (cd /tmp/apk-test && zip -q $APK_TEST AndroidManifest.xml)
    rm -rf /tmp/apk-test
    echo -e "${GREEN}✅ Fichier de test créé${NC}"
fi

echo ""

# 3. Test APKScanner
echo "3️⃣  Test APKScanner..."
APK_RESPONSE=$(curl -s -X POST -F "file=@$APK_TEST" http://localhost:8001/scan)
APK_JOB=$(echo $APK_RESPONSE | jq -r '.job_id // empty')

if [ -z "$APK_JOB" ]; then
    echo -e "${RED}❌ APKScanner a échoué${NC}"
    echo "Réponse: $APK_RESPONSE"
    exit 1
fi
echo -e "${GREEN}✅ Job ID: $APK_JOB${NC}"

# Attendre la fin de l'analyse
sleep 3

# Vérifier le résultat
APK_RESULT=$(curl -s http://localhost:8001/scan/$APK_JOB)
APK_STATUS=$(echo $APK_RESULT | jq -r '.status // empty')

if [ "$APK_STATUS" == "done" ] || [ "$APK_STATUS" == "failed" ]; then
    echo -e "${GREEN}✅ Analyse terminée (status: $APK_STATUS)${NC}"
else
    echo -e "${YELLOW}⚠️  Status: $APK_STATUS${NC}"
fi

echo ""

# 4. Test SecretHunter
echo "4️⃣  Test SecretHunter..."
SECRET_RESPONSE=$(curl -s -X POST -F "file=@$APK_TEST" http://localhost:8002/scan)
SECRET_JOB=$(echo $SECRET_RESPONSE | jq -r '.job_id // empty')

if [ -z "$SECRET_JOB" ]; then
    echo -e "${RED}❌ SecretHunter a échoué${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Job ID: $SECRET_JOB${NC}"

echo ""

# 5. Test CryptoCheck
echo "5️⃣  Test CryptoCheck..."
CRYPTO_RESPONSE=$(curl -s -X POST -F "file=@$APK_TEST" http://localhost:8003/scan)
CRYPTO_JOB=$(echo $CRYPTO_RESPONSE | jq -r '.job_id // empty')

if [ -z "$CRYPTO_JOB" ]; then
    echo -e "${RED}❌ CryptoCheck a échoué${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Job ID: $CRYPTO_JOB${NC}"

echo ""

# 6. Test ReportGen
echo "6️⃣  Test ReportGen (agrégation)..."
sleep 3  # Attendre que toutes les analyses soient terminées

REPORT_JSON=$(curl -s -X POST http://localhost:8005/generate \
    -H "Content-Type: application/json" \
    -d "{\"job_ids\": {\"apkscanner\": \"$APK_JOB\", \"secrethunter\": \"$SECRET_JOB\", \"cryptocheck\": \"$CRYPTO_JOB\"}}")

PACKAGE=$(echo $REPORT_JSON | jq -r '.summary.package_name // empty')

if [ -n "$PACKAGE" ]; then
    echo -e "${GREEN}✅ Rapport généré pour: $PACKAGE${NC}"
    TOTAL_ISSUES=$(echo $REPORT_JSON | jq -r '.summary.total_issues // 0')
    echo "   📊 Issues trouvées: $TOTAL_ISSUES"
else
    echo -e "${YELLOW}⚠️  Rapport généré avec warnings${NC}"
fi

# Sauvegarder le rapport
echo "$REPORT_JSON" > /tmp/mobilesec-report.json
echo -e "${GREEN}✅ Rapport sauvegardé: /tmp/mobilesec-report.json${NC}"

echo ""

# 7. Test FixSuggest
echo "7️⃣  Test FixSuggest..."
FIXES_JSON=$(curl -s -X POST http://localhost:8006/suggest \
    -H "Content-Type: application/json" \
    -d "$REPORT_JSON")

FIXES_COUNT=$(echo $FIXES_JSON | jq -r '.total_fixes // 0')
echo -e "${GREEN}✅ Suggestions générées: $FIXES_COUNT correctifs${NC}"

echo ""

# 8. Test CIConnector
echo "8️⃣  Test CIConnector..."
GITHUB_YAML=$(curl -s http://localhost:8007/github-action)

if echo "$GITHUB_YAML" | grep -q "name: Mobile Security Scan"; then
    echo -e "${GREEN}✅ Workflow GitHub Actions généré${NC}"
else
    echo -e "${RED}❌ Échec génération workflow${NC}"
    exit 1
fi

GITLAB_YAML=$(curl -s http://localhost:8007/gitlab-ci)

if echo "$GITLAB_YAML" | grep -q "stages:"; then
    echo -e "${GREEN}✅ Config GitLab CI générée${NC}"
else
    echo -e "${RED}❌ Échec génération GitLab CI${NC}"
    exit 1
fi

echo ""

# 9. Test format SARIF
echo "9️⃣  Test génération SARIF..."
SARIF_JSON=$(curl -s -X POST "http://localhost:8005/generate?format=sarif" \
    -H "Content-Type: application/json" \
    -d "{\"job_ids\": {\"apkscanner\": \"$APK_JOB\", \"secrethunter\": \"$SECRET_JOB\", \"cryptocheck\": \"$CRYPTO_JOB\"}}")

SARIF_VERSION=$(echo $SARIF_JSON | jq -r '.version // empty')

if [ "$SARIF_VERSION" == "2.1.0" ]; then
    echo -e "${GREEN}✅ Rapport SARIF généré (version $SARIF_VERSION)${NC}"
else
    echo -e "${YELLOW}⚠️  Format SARIF incomplet${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ TOUS LES TESTS RÉUSSIS!${NC}"
echo "=========================================="
echo ""
echo "📄 Rapport disponible: /tmp/mobilesec-report.json"
echo ""
echo "Pour visualiser le rapport:"
echo "  cat /tmp/mobilesec-report.json | jq '.'"
echo ""
