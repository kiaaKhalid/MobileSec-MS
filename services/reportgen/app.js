const express = require('express');
const cors = require('cors');
const axios = require('axios');
const { jsPDF } = require('jspdf');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8005;

app.use(cors());  // Enable CORS for all routes
app.use(express.json());

// Configuration des services
const SERVICES = {
    apkscanner: process.env.APKSCANNER_URL || 'http://apkscanner:8001',
    secrethunter: process.env.SECRETHUNTER_URL || 'http://secrethunter:8002',
    cryptocheck: process.env.CRYPTOCHECK_URL || 'http://cryptocheck:8003',
    networkinspector: process.env.NETWORKINSPECTOR_URL || 'http://networkinspector:8004'
};

app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'reportgen' });
});

// Agrège les résultats de tous les services
app.post('/generate', async (req, res) => {
    try {
        const { job_ids } = req.body;
        
        if (!job_ids || !job_ids.apkscanner) {
            return res.status(400).json({ error: 'Missing apkscanner job_id' });
        }

        // Récupération des résultats de chaque service
        const results = {
            apk: null,
            secrets: null,
            crypto: null,
            network: null
        };

        try {
            const apkRes = await axios.get(`${SERVICES.apkscanner}/scan/${job_ids.apkscanner}`);
            results.apk = apkRes.data;
        } catch (e) {
            console.error('APKScanner error:', e.message);
        }

        if (job_ids.secrethunter) {
            try {
                const secretRes = await axios.get(`${SERVICES.secrethunter}/scan/${job_ids.secrethunter}`);
                results.secrets = secretRes.data;
            } catch (e) {
                console.error('SecretHunter error:', e.message);
            }
        }

        if (job_ids.cryptocheck) {
            try {
                const cryptoRes = await axios.get(`${SERVICES.cryptocheck}/scan/${job_ids.cryptocheck}`);
                results.crypto = cryptoRes.data;
            } catch (e) {
                console.error('CryptoCheck error:', e.message);
            }
        }

        if (job_ids.networkinspector) {
            try {
                const networkRes = await axios.get(`${SERVICES.networkinspector}/scan/${job_ids.networkinspector}`);
                results.network = networkRes.data;
            } catch (e) {
                console.error('NetworkInspector error:', e.message);
            }
        }

        // Génération du rapport JSON
        const report = generateReport(results);
        
        // Option de format
        const format = req.query.format || 'json';
        
        if (format === 'pdf') {
            const pdfBuffer = generatePDF(report);
            res.setHeader('Content-Type', 'application/pdf');
            res.setHeader('Content-Disposition', `attachment; filename="security-report-${Date.now()}.pdf"`);
            return res.send(pdfBuffer);
        } else if (format === 'sarif') {
            const sarifReport = generateSARIF(report);
            return res.json(sarifReport);
        } else {
            return res.json(report);
        }

    } catch (error) {
        console.error('Report generation error:', error);
        res.status(500).json({ error: error.message });
    }
});

function generateReport(results) {
    const report = {
        metadata: {
            generated_at: new Date().toISOString(),
            platform: 'MobileSec-MS',
            version: '1.0.0'
        },
        summary: {
            package_name: results.apk?.result?.package || 'unknown',
            filename: results.apk?.filename || 'unknown',
            total_issues: 0,
            critical: 0,
            high: 0,
            medium: 0,
            low: 0
        },
        findings: {
            apk_analysis: results.apk?.result || {},
            secrets: results.secrets?.findings || [],
            crypto_issues: results.crypto?.findings || [],
            network_issues: results.network?.findings || []
        },
        recommendations: []
    };

    // Calcul des statistiques
    const allFindings = [
        ...(results.secrets?.findings || []),
        ...(results.crypto?.findings || []),
        ...(results.network?.findings || [])
    ];

    allFindings.forEach(finding => {
        report.summary.total_issues++;
        const severity = finding.severity?.toUpperCase();
        if (severity === 'CRITICAL') report.summary.critical++;
        else if (severity === 'HIGH') report.summary.high++;
        else if (severity === 'MEDIUM') report.summary.medium++;
        else if (severity === 'LOW') report.summary.low++;
    });

    // Génération des recommandations prioritaires
    if (report.summary.critical > 0) {
        report.recommendations.push({
            priority: 'CRITICAL',
            message: `${report.summary.critical} vulnérabilités critiques détectées. Action immédiate requise.`
        });
    }

    // Recommandations OWASP MASVS
    if (results.apk?.result?.flags?.debuggable) {
        report.recommendations.push({
            priority: 'HIGH',
            masvs: 'MSTG-RESILIENCE-2',
            message: 'Désactiver le mode debug en production (android:debuggable="false")'
        });
    }

    if (results.apk?.result?.flags?.allowBackup) {
        report.recommendations.push({
            priority: 'MEDIUM',
            masvs: 'MSTG-STORAGE-8',
            message: 'Désactiver allowBackup ou implémenter des règles de backup sécurisées'
        });
    }

    return report;
}

function generatePDF(report) {
    const doc = new jsPDF();
    
    // Page de titre
    doc.setFontSize(20);
    doc.text('Security Analysis Report', 20, 20);
    doc.setFontSize(12);
    doc.text(`Package: ${report.summary.package_name}`, 20, 35);
    doc.text(`Generated: ${report.metadata.generated_at}`, 20, 42);
    
    // Résumé
    doc.setFontSize(16);
    doc.text('Summary', 20, 60);
    doc.setFontSize(11);
    doc.text(`Total Issues: ${report.summary.total_issues}`, 20, 70);
    doc.text(`Critical: ${report.summary.critical}`, 20, 77);
    doc.text(`High: ${report.summary.high}`, 20, 84);
    doc.text(`Medium: ${report.summary.medium}`, 20, 91);
    doc.text(`Low: ${report.summary.low}`, 20, 98);
    
    // Recommandations
    doc.setFontSize(16);
    doc.text('Top Recommendations', 20, 115);
    doc.setFontSize(10);
    let yPos = 125;
    report.recommendations.slice(0, 5).forEach((rec, idx) => {
        doc.text(`${idx + 1}. [${rec.priority}] ${rec.message}`, 20, yPos);
        yPos += 7;
    });
    
    return doc.output('arraybuffer');
}

function generateSARIF(report) {
    // Format SARIF 2.1.0 pour intégration CI/CD
    const sarif = {
        version: '2.1.0',
        $schema: 'https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json',
        runs: [
            {
                tool: {
                    driver: {
                        name: 'MobileSec-MS',
                        version: '1.0.0',
                        informationUri: 'https://github.com/yourusername/mobilesec-ms'
                    }
                },
                results: []
            }
        ]
    };

    const allFindings = [
        ...report.findings.secrets,
        ...report.findings.crypto_issues,
        ...report.findings.network_issues
    ];

    allFindings.forEach((finding, idx) => {
        sarif.runs[0].results.push({
            ruleId: finding.type || `ISSUE_${idx}`,
            level: mapSeverityToSARIF(finding.severity),
            message: {
                text: finding.description || finding.type
            },
            locations: finding.location ? [{
                physicalLocation: {
                    artifactLocation: {
                        uri: finding.location
                    }
                }
            }] : []
        });
    });

    return sarif;
}

function mapSeverityToSARIF(severity) {
    const map = {
        'CRITICAL': 'error',
        'HIGH': 'error',
        'MEDIUM': 'warning',
        'LOW': 'note'
    };
    return map[severity?.toUpperCase()] || 'warning';
}

app.listen(PORT, () => {
    console.log(`ReportGen service listening on port ${PORT}`);
});
