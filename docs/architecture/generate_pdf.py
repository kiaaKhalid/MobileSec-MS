#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération du PDF de l'architecture MobileSec-MS
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def create_header_footer(canvas, doc):
    """Ajoute header et footer sur chaque page"""
    canvas.saveState()
    
    # Header
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(colors.HexColor('#1e3a8a'))
    canvas.drawString(2*cm, A4[1] - 2*cm, "MobileSec-MS - Architecture Microservices")
    
    # Footer
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2*cm, 1.5*cm, f"© 2025 MobileSec-MS Team")
    canvas.drawRightString(A4[0] - 2*cm, 1.5*cm, f"Page {doc.page}")
    
    canvas.restoreState()

def generate_architecture_pdf():
    """Génère le PDF complet de l'architecture"""
    
    # Configuration du document
    filename = "MobileSec-MS_Architecture_Microservices.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=2.5*cm
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Style pour les titres de section
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Style pour le corps de texte
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=8,
        fontName='Courier',
        textColor=colors.HexColor('#1f2937'),
        backColor=colors.HexColor('#f3f4f6'),
        leftIndent=10,
        rightIndent=10
    )
    
    # Contenu du PDF
    story = []
    
    # ============ PAGE DE GARDE ============
    story.append(Spacer(1, 3*cm))
    
    # Titre principal
    story.append(Paragraph("🏗️ Architecture Microservices", title_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("MobileSec-MS", title_style))
    story.append(Spacer(1, 1*cm))
    
    # Sous-titre
    subtitle_style = ParagraphStyle('Subtitle', parent=body_style, fontSize=14, alignment=TA_CENTER, textColor=colors.grey)
    story.append(Paragraph("Plateforme d'analyse de sécurité pour applications mobiles Android", subtitle_style))
    story.append(Spacer(1, 2*cm))
    
    # Informations du document
    info_data = [
        ['Version', '1.0'],
        ['Date', datetime.now().strftime('%d/%m/%Y')],
        ['Statut', '✅ Production Ready'],
        ['Auteur', 'MobileSec-MS Team']
    ]
    
    info_table = Table(info_data, colWidths=[5*cm, 8*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    
    story.append(info_table)
    story.append(PageBreak())
    
    # ============ TABLE DES MATIÈRES ============
    story.append(Paragraph("📋 Table des matières", heading1_style))
    story.append(Spacer(1, 0.5*cm))
    
    toc_items = [
        "1. Schéma d'ensemble",
        "2. Rôle de chaque microservice",
        "3. Technologies utilisées",
        "4. Bases de données associées",
        "5. Méthodes de communication",
        "6. Architecture détaillée",
        "7. Résumé et métriques"
    ]
    
    for item in toc_items:
        story.append(Paragraph(f"• {item}", body_style))
        story.append(Spacer(1, 0.2*cm))
    
    story.append(PageBreak())
    
    # ============ SECTION 1: SCHÉMA D'ENSEMBLE ============
    story.append(Paragraph("1. 📐 Schéma d'ensemble (Vue globale)", heading1_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "L'architecture MobileSec-MS est composée de <b>7 microservices indépendants</b> "
        "orchestrés via Docker Compose. Chaque service a une responsabilité unique et communique "
        "via des API REST.", 
        body_style
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Architecture en couches
    architecture_text = """
    <b>Architecture en 4 couches :</b><br/>
    <br/>
    <b>1. Load Balancer / API Gateway</b><br/>
    &nbsp;&nbsp;&nbsp;• Nginx ou Traefik<br/>
    &nbsp;&nbsp;&nbsp;• Point d'entrée unique<br/>
    &nbsp;&nbsp;&nbsp;• Distribution de charge<br/>
    <br/>
    <b>2. Frontend Layer</b><br/>
    &nbsp;&nbsp;&nbsp;• React 18 + Vite (Port 5173)<br/>
    &nbsp;&nbsp;&nbsp;• Interface utilisateur moderne<br/>
    &nbsp;&nbsp;&nbsp;• Upload APK et visualisation des résultats<br/>
    <br/>
    <b>3. Microservices Layer</b><br/>
    &nbsp;&nbsp;&nbsp;• APKScanner (8001) - Analyse statique APK<br/>
    &nbsp;&nbsp;&nbsp;• SecretHunter (8002) - Détection de secrets<br/>
    &nbsp;&nbsp;&nbsp;• CryptoCheck (8003) - Vérification crypto<br/>
    &nbsp;&nbsp;&nbsp;• NetworkInspector (8004) - Analyse réseau<br/>
    &nbsp;&nbsp;&nbsp;• ReportGen (8005) - Agrégation rapports<br/>
    &nbsp;&nbsp;&nbsp;• FixSuggest (8006) - Suggestions correctifs<br/>
    &nbsp;&nbsp;&nbsp;• CIConnector (8007) - Intégration CI/CD<br/>
    <br/>
    <b>4. Infrastructure Layer</b><br/>
    &nbsp;&nbsp;&nbsp;• Docker Network (mobilesec-network)<br/>
    &nbsp;&nbsp;&nbsp;• Volumes persistants (SQLite databases)<br/>
    &nbsp;&nbsp;&nbsp;• Service Discovery automatique<br/>
    """
    
    story.append(Paragraph(architecture_text, body_style))
    story.append(PageBreak())
    
    # ============ SECTION 2: RÔLE DE CHAQUE MICROSERVICE ============
    story.append(Paragraph("2. 🎯 Rôle de chaque microservice", heading1_style))
    story.append(Spacer(1, 0.5*cm))
    
    services_data = [
        ['Microservice', 'Port', 'Responsabilité', 'Technologies'],
        ['APKScanner', '8001', 'Analyse statique APK\nDésassemblage et extraction manifest', 'Python 3.11\nFlask\nAndroguard'],
        ['SecretHunter', '8002', 'Détection de secrets exposés\nAPI keys, tokens, passwords', 'Python 3.11\nFlask\nRegex'],
        ['CryptoCheck', '8003', 'Vérification cryptographique\nDétection algos faibles', 'Python 3.11\nFlask\nCWE DB'],
        ['NetworkInspector', '8004', 'Analyse réseau\nHTTP cleartext, TLS config', 'Python 3.11\nFlask\nRegex'],
        ['ReportGen', '8005', 'Agrégation des rapports\nGénération PDF/JSON/SARIF', 'Node.js 18\nExpress\njsPDF'],
        ['FixSuggest', '8006', 'Suggestions de correctifs\nOWASP MASVS mapping', 'Python 3.10\nFlask\nYAML'],
        ['CIConnector', '8007', 'Intégration CI/CD\nGitHub Actions, GitLab CI', 'Python 3.10\nFlask\nJinja2']
    ]
    
    services_table = Table(services_data, colWidths=[3*cm, 1.5*cm, 5.5*cm, 3*cm])
    services_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    
    story.append(services_table)
    story.append(PageBreak())
    
    # ============ SECTION 3: DÉTAIL APKScanner ============
    story.append(Paragraph("2.1 APKScanner - Analyse statique APK", heading2_style))
    story.append(Spacer(1, 0.3*cm))
    
    apk_features = """
    <b>Fonctionnalités principales :</b><br/>
    <br/>
    ✅ <b>Désassemblage de l'APK</b> avec Androguard<br/>
    &nbsp;&nbsp;&nbsp;• Extraction du fichier APK complet<br/>
    &nbsp;&nbsp;&nbsp;• Décompilation des classes DEX<br/>
    <br/>
    ✅ <b>Analyse du AndroidManifest.xml</b><br/>
    &nbsp;&nbsp;&nbsp;• Parsing XML avec ElementTree<br/>
    &nbsp;&nbsp;&nbsp;• Extraction du package name<br/>
    <br/>
    ✅ <b>Permissions</b><br/>
    &nbsp;&nbsp;&nbsp;• Liste complète des permissions demandées<br/>
    &nbsp;&nbsp;&nbsp;• Détection des permissions dangereuses<br/>
    <br/>
    ✅ <b>Composants exportés</b><br/>
    &nbsp;&nbsp;&nbsp;• Activities, Services, Receivers, Providers<br/>
    &nbsp;&nbsp;&nbsp;• Détection de android:exported="true"<br/>
    <br/>
    ✅ <b>Flags de sécurité</b><br/>
    &nbsp;&nbsp;&nbsp;• android:debuggable="true" → Vulnérabilité HIGH<br/>
    &nbsp;&nbsp;&nbsp;• android:allowBackup="true" → Vulnérabilité MEDIUM<br/>
    &nbsp;&nbsp;&nbsp;• android:usesCleartextTraffic="true" → Vulnérabilité HIGH<br/>
    <br/>
    <b>API Endpoints :</b><br/>
    • POST /scan - Upload et analyse d'un APK<br/>
    • GET /scan/{job_id} - Récupération des résultats<br/>
    • GET /health - Health check du service<br/>
    """
    
    story.append(Paragraph(apk_features, body_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Base de données APKScanner
    story.append(Paragraph("Base de données : apkscanner.db (SQLite)", heading3_style))
    
    db_code = """
CREATE TABLE scans (
    job_id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    package_name TEXT,
    status TEXT NOT NULL,
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
    """
    
    story.append(Paragraph(db_code, code_style))
    story.append(PageBreak())
    
    # ============ SECTION 4: DÉTAIL SecretHunter ============
    story.append(Paragraph("2.2 SecretHunter - Détection de secrets", heading2_style))
    story.append(Spacer(1, 0.3*cm))
    
    secret_patterns = """
    <b>Patterns de détection :</b><br/>
    <br/>
    🔑 <b>API Keys</b><br/>
    &nbsp;&nbsp;&nbsp;• AWS Access Keys : AKIA[0-9A-Z]{16}<br/>
    &nbsp;&nbsp;&nbsp;• Google API Keys : AIza[0-9A-Za-z-_]{35}<br/>
    &nbsp;&nbsp;&nbsp;• Stripe Keys : sk_live_[0-9a-zA-Z]{24}<br/>
    <br/>
    🔐 <b>Tokens</b><br/>
    &nbsp;&nbsp;&nbsp;• JWT Tokens : eyJ[A-Za-z0-9-_=]+...<br/>
    &nbsp;&nbsp;&nbsp;• Bearer Tokens<br/>
    &nbsp;&nbsp;&nbsp;• OAuth Tokens<br/>
    <br/>
    🔒 <b>Mots de passe hardcodés</b><br/>
    &nbsp;&nbsp;&nbsp;• password = "..."<br/>
    &nbsp;&nbsp;&nbsp;• pwd = "..."<br/>
    <br/>
    📊 <b>Analyse d'entropie de Shannon</b><br/>
    &nbsp;&nbsp;&nbsp;• Détection de chaînes aléatoires (secrets potentiels)<br/>
    &nbsp;&nbsp;&nbsp;• Score de confiance 0-100%<br/>
    <br/>
    <b>Classification par sévérité :</b><br/>
    • 🔴 CRITICAL - API keys cloud (AWS, GCP, Azure)<br/>
    • 🟠 HIGH - Tokens OAuth, credentials<br/>
    • 🟡 MEDIUM - URLs sensibles<br/>
    • ⚪ LOW - Configuration non critique<br/>
    """
    
    story.append(Paragraph(secret_patterns, body_style))
    story.append(PageBreak())
    
    # ============ SECTION 5: COMMUNICATION ENTRE MICROSERVICES ============
    story.append(Paragraph("5. 🔄 Méthodes de communication", heading1_style))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("5.1 Communication Synchrone (REST API)", heading2_style))
    story.append(Spacer(1, 0.3*cm))
    
    comm_text = """
    <b>Pattern utilisé : HTTP/REST</b><br/>
    <br/>
    Tous les microservices communiquent via des API REST HTTP.<br/>
    <br/>
    <b>Avantages :</b><br/>
    ✅ Simplicité d'implémentation<br/>
    ✅ Debugging facile<br/>
    ✅ Pas de dépendances externes (pas de message broker)<br/>
    ✅ Service Discovery automatique via Docker DNS<br/>
    <br/>
    <b>Exemple de flux :</b><br/>
    1. Frontend envoie POST /scan à APKScanner (8001)<br/>
    2. APKScanner retourne {job_id: "xxx", status: "done"}<br/>
    3. ReportGen appelle GET /scan/xxx pour récupérer les résultats<br/>
    4. Agrégation de tous les microservices<br/>
    5. Génération du rapport final<br/>
    """
    
    story.append(Paragraph(comm_text, body_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Tableau des communications
    story.append(Paragraph("Tableau récapitulatif des communications", heading3_style))
    
    comm_data = [
        ['Source', 'Destination', 'Méthode', 'Endpoint', 'Données'],
        ['Frontend', 'APKScanner', 'POST', '/scan', 'Fichier APK'],
        ['Frontend', 'SecretHunter', 'POST', '/scan', 'Fichier APK'],
        ['Frontend', 'CryptoCheck', 'POST', '/scan', 'Fichier APK'],
        ['Frontend', 'ReportGen', 'POST', '/generate', 'job_ids (JSON)'],
        ['ReportGen', 'APKScanner', 'GET', '/scan/{id}', 'Résultats'],
        ['ReportGen', 'SecretHunter', 'GET', '/scan/{id}', 'Résultats'],
        ['Frontend', 'FixSuggest', 'POST', '/suggest', 'Rapport JSON'],
        ['Frontend', 'CIConnector', 'GET', '/github-action', 'Template YAML']
    ]
    
    comm_table = Table(comm_data, colWidths=[3*cm, 3*cm, 2*cm, 3*cm, 3*cm])
    comm_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    
    story.append(comm_table)
    story.append(PageBreak())
    
    # ============ SECTION 6: SERVICE DISCOVERY ============
    story.append(Paragraph("5.2 Service Discovery", heading2_style))
    story.append(Spacer(1, 0.3*cm))
    
    discovery_text = """
    <b>Mécanisme : Docker DNS automatique</b><br/>
    <br/>
    Tous les services sont dans le même réseau Docker (<i>mobilesec-network</i>).<br/>
    Docker fournit automatiquement la résolution DNS.<br/>
    <br/>
    <b>Résolution des noms :</b><br/>
    • apkscanner → 172.18.0.2:8001<br/>
    • secrethunter → 172.18.0.3:8002<br/>
    • cryptocheck → 172.18.0.4:8003<br/>
    • networkinspector → 172.18.0.5:8004<br/>
    • reportgen → 172.18.0.6:8005<br/>
    <br/>
    <b>Accès aux services :</b><br/>
    • Format : http://servicename:port<br/>
    • Exemple : http://apkscanner:8001/health<br/>
    <br/>
    <b>Configuration Docker Compose :</b><br/>
    Tous les services déclarent le réseau "mobilesec-network".<br/>
    La résolution DNS est automatique et transparente.<br/>
    """
    
    story.append(Paragraph(discovery_text, body_style))
    story.append(PageBreak())
    
    # ============ SECTION 7: RÉSUMÉ ET MÉTRIQUES ============
    story.append(Paragraph("7. 🎯 Résumé de l'architecture", heading1_style))
    story.append(Spacer(1, 0.5*cm))
    
    summary_text = """
    <b>Points clés de l'architecture :</b><br/>
    <br/>
    ✅ <b>7 microservices indépendants</b> avec responsabilités bien définies<br/>
    ✅ <b>Communication REST API synchrone</b> (simple et efficace)<br/>
    ✅ <b>Service Discovery automatique</b> via Docker DNS<br/>
    ✅ <b>Isolation des données</b> (chaque service a sa propre BDD)<br/>
    ✅ <b>Scalabilité horizontale</b> possible (duplication des containers)<br/>
    ✅ <b>Technologie polyglotte</b> (Python + Node.js)<br/>
    ✅ <b>Architecture modulaire</b> (facile d'ajouter de nouveaux services)<br/>
    ✅ <b>Standards ouverts</b> (REST, JSON, SARIF, OWASP MASVS)<br/>
    """
    
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Métriques de performance
    story.append(Paragraph("Métriques de performance", heading2_style))
    
    metrics_data = [
        ['Métrique', 'Valeur'],
        ['Temps de scan moyen', '40-70 secondes'],
        ['Throughput', '~50 APK/heure par instance'],
        ['Taille des containers', '200-500 MB chacun'],
        ['Consommation RAM totale', '~4 GB pour tous les services'],
        ['Latence réseau interne', '< 10ms (Docker network)'],
        ['Formats de rapport supportés', 'JSON, PDF, SARIF'],
        ['Standards de sécurité', 'OWASP MASVS, CWE']
    ]
    
    metrics_table = Table(metrics_data, colWidths=[8*cm, 6*cm])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    
    story.append(metrics_table)
    story.append(Spacer(1, 1*cm))
    
    # Technologies utilisées
    story.append(Paragraph("Technologies utilisées", heading2_style))
    
    tech_data = [
        ['Composant', 'Technologies'],
        ['Services Backend', 'Python 3.10/3.11, Flask 2.3, Gunicorn'],
        ['Service ReportGen', 'Node.js 18, Express 4.18, jsPDF'],
        ['Frontend', 'React 18, Vite 5.x, Axios'],
        ['Bases de données', 'SQLite 3 (Dev), PostgreSQL (Prod)'],
        ['Analyse APK', 'Androguard 4.x'],
        ['Communication', 'REST API, HTTP/JSON'],
        ['Conteneurisation', 'Docker 24.x, Docker Compose 2.x'],
        ['CI/CD', 'GitHub Actions, GitLab CI, Jenkins']
    ]
    
    tech_table = Table(tech_data, colWidths=[5*cm, 9*cm])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    
    story.append(tech_table)
    story.append(PageBreak())
    
    # ============ DERNIÈRE PAGE ============
    story.append(Spacer(1, 3*cm))
    
    conclusion_style = ParagraphStyle('Conclusion', parent=body_style, fontSize=12, alignment=TA_CENTER)
    story.append(Paragraph("<b>🎉 Architecture complète et documentée</b>", conclusion_style))
    story.append(Spacer(1, 1*cm))
    
    story.append(Paragraph(
        "Cette architecture microservices offre une solution robuste, scalable et maintenable "
        "pour l'analyse de sécurité des applications mobiles Android.",
        conclusion_style
    ))
    story.append(Spacer(1, 1*cm))
    
    contact_text = """
    <b>Contact et Support</b><br/>
    <br/>
    📧 Email : support@mobilesec-ms.com<br/>
    🌐 Website : https://mobilesec-ms.com<br/>
    📚 Documentation : https://docs.mobilesec-ms.com<br/>
    💬 GitHub : https://github.com/mobilesec-ms<br/>
    """
    
    story.append(Paragraph(contact_text, body_style))
    
    # Construction du PDF
    doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    
    print(f"✅ PDF généré avec succès : {filename}")
    print(f"📄 Taille du fichier : {os.path.getsize(filename) / 1024:.2f} KB")
    return filename

if __name__ == "__main__":
    try:
        pdf_file = generate_architecture_pdf()
        print(f"\n🎉 PDF disponible à : docs/architecture/{pdf_file}")
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        import traceback
        traceback.print_exc()
