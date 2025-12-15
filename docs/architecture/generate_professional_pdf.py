#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime
import os

class PDFTemplate:
    def __init__(self, doc):
        self.doc = doc
    
    def header_footer(self, canvas, doc):
        canvas.saveState()
        # Header
        canvas.setFillColor(colors.HexColor('#1e3a8a'))
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawString(2*cm, A4[1] - 1.5*cm, "MobileSec-MS - Architecture Microservices")
        # Footer
        canvas.setFillColor(colors.grey)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2*cm, 1.5*cm, f"© 2025 MobileSec-MS Team")
        canvas.drawRightString(A4[0] - 2*cm, 1.5*cm, f"Page {doc.page}")
        canvas.restoreState()

def create_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='MainTitle', parent=styles['Heading1'], fontSize=32,
        textColor=colors.HexColor('#1e3a8a'), spaceAfter=20, alignment=TA_CENTER,
        fontName='Helvetica-Bold', leading=38))
    styles.add(ParagraphStyle(name='Subtitle', parent=styles['Normal'], fontSize=16,
        textColor=colors.HexColor('#475569'), spaceAfter=30, alignment=TA_CENTER,
        fontName='Helvetica', leading=20))
    styles.add(ParagraphStyle(name='SectionTitle', parent=styles['Heading1'], fontSize=20,
        textColor=colors.HexColor('#1e3a8a'), spaceAfter=15, spaceBefore=25,
        fontName='Helvetica-Bold', leading=24))
    styles.add(ParagraphStyle(name='SubsectionTitle', parent=styles['Heading2'], fontSize=15,
        textColor=colors.HexColor('#1e40af'), spaceAfter=12, spaceBefore=18,
        fontName='Helvetica-Bold', leftIndent=10, leading=18))
    styles.add(ParagraphStyle(name='BodyTextPro', parent=styles['BodyText'], fontSize=10,
        alignment=TA_JUSTIFY, spaceAfter=10, leading=14, textColor=colors.HexColor('#1f2937')))
    return styles

def create_pie_chart(data, labels, title):
    drawing = Drawing(400, 200)
    pie = Pie()
    pie.x, pie.y, pie.width, pie.height = 150, 50, 120, 120
    pie.data, pie.labels = data, labels
    pie.slices.strokeWidth = 0.5
    colors_list = [colors.HexColor(c) for c in ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4']]
    for i, color in enumerate(colors_list[:len(data)]):
        pie.slices[i].fillColor = color
    drawing.add(pie)
    title_string = String(200, 180, title, textAnchor='middle')
    title_string.fontName, title_string.fontSize = 'Helvetica-Bold', 12
    title_string.fillColor = colors.HexColor('#1e3a8a')
    drawing.add(title_string)
    return drawing

def create_bar_chart(data, categories, title):
    drawing = Drawing(400, 200)
    bc = VerticalBarChart()
    bc.x, bc.y, bc.height, bc.width = 50, 50, 125, 300
    bc.data = [data]
    bc.categoryAxis.categoryNames = categories
    bc.valueAxis.valueMin, bc.valueAxis.valueMax = 0, max(data) * 1.2
    bc.bars[0].fillColor = colors.HexColor('#3b82f6')
    drawing.add(bc)
    title_string = String(200, 180, title, textAnchor='middle')
    title_string.fontName, title_string.fontSize = 'Helvetica-Bold', 12
    title_string.fillColor = colors.HexColor('#1e3a8a')
    drawing.add(title_string)
    return drawing

def generate_professional_pdf():
    filename = "MobileSec-MS_Architecture_Microservices_Professional.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
        topMargin=3*cm, bottomMargin=3*cm, title="MobileSec-MS - Architecture Microservices",
        author="MobileSec-MS Team", subject="Documentation Architecture")
    template = PDFTemplate(doc)
    styles = create_styles()
    story = []
    
    # PAGE DE GARDE
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("🏗️", styles['MainTitle']))
    story.append(Paragraph("Architecture Microservices", styles['MainTitle']))
    story.append(Paragraph("MobileSec-MS", styles['MainTitle']))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Plateforme d'analyse de sécurité pour applications mobiles Android", styles['Subtitle']))
    story.append(Spacer(1, 2*cm))
    
    info_box = Table([
        ['📋 Version', '1.0'], ['📅 Date', datetime.now().strftime('%d %B %Y')],
        ['✅ Statut', 'Production Ready'], ['👥 Auteur', 'MobileSec-MS Team']
    ], colWidths=[6*cm, 7*cm])
    info_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dbeafe')),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1.5, colors.HexColor('#3b82f6')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))
    story.append(info_box)
    story.append(PageBreak())
    
    # TABLE DES MATIÈRES
    story.append(Paragraph("📑 Table des matières", styles['SectionTitle']))
    story.append(Spacer(1, 0.5*cm))
    toc_data = [
        ['Section', 'Description'],
        ['1', "Vue d'ensemble de l'architecture"],
        ['2', 'Microservices détaillés'],
        ['3', 'Stack technologique'],
        ['4', 'Métriques et performances'],
        ['5', 'Conclusion']
    ]
    toc_table = Table(toc_data, colWidths=[2*cm, 11*cm])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    story.append(toc_table)
    story.append(PageBreak())
    
    # SECTION 1
    story.append(Paragraph("1. 🌐 Vue d'ensemble de l'architecture", styles['SectionTitle']))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "MobileSec-MS est une plateforme DevSecOps complète composée de <b>7 microservices indépendants</b> "
        "qui collaborent pour fournir une analyse de sécurité approfondie des applications mobiles Android.",
        styles['BodyTextPro']))
    story.append(Spacer(1, 1*cm))
    pie_data = [1, 1, 1, 1, 1, 1, 1]
    pie_labels = ['APK', 'Secret', 'Crypto', 'Network', 'Report', 'Fix', 'CI']
    story.append(create_pie_chart(pie_data, pie_labels, 'Répartition des 7 microservices'))
    story.append(PageBreak())
    
    # SECTION 2
    story.append(Paragraph("2. 🎯 Microservices détaillés", styles['SectionTitle']))
    story.append(Spacer(1, 0.5*cm))
    services_data = [
        ['Service', 'Port', 'Technologie', 'Fonction'],
        ['🔍 APKScanner', '8001', 'Python 3.11', 'Analyse statique APK'],
        ['🔐 SecretHunter', '8002', 'Python 3.11', 'Détection secrets'],
        ['🔒 CryptoCheck', '8003', 'Python 3.11', 'Vérification crypto'],
        ['🌐 NetworkInspector', '8004', 'Python 3.11', 'Analyse réseau'],
        ['📊 ReportGen', '8005', 'Node.js 18', 'Agrégation rapports'],
        ['💡 FixSuggest', '8006', 'Python 3.10', 'Suggestions OWASP'],
        ['🔗 CIConnector', '8007', 'Python 3.10', 'Intégration CI/CD']
    ]
    services_table = Table(services_data, colWidths=[4*cm, 1.5*cm, 3*cm, 4.5*cm])
    services_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(services_table)
    story.append(PageBreak())
    
    # SECTION 3
    story.append(Paragraph("3. 💻 Stack technologique", styles['SectionTitle']))
    story.append(Spacer(1, 0.5*cm))
    tech_data = [
        ['Composant', 'Technologies', 'Version'],
        ['Backend', 'Python + Flask + Gunicorn', '3.10/3.11'],
        ['ReportGen', 'Node.js + Express', '18.x'],
        ['Frontend', 'React + Vite', '18.x'],
        ['Database', 'SQLite / PostgreSQL', '3.x / 15.x'],
        ['APK Analysis', 'Androguard', '4.x'],
        ['Container', 'Docker + Compose', '24.x']
    ]
    tech_table = Table(tech_data, colWidths=[4.5*cm, 6*cm, 2.5*cm])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f0fdf4'), colors.white])
    ]))
    story.append(tech_table)
    story.append(PageBreak())
    
    # SECTION 4
    story.append(Paragraph("4. 📈 Métriques et performances", styles['SectionTitle']))
    story.append(Spacer(1, 0.5*cm))
    metrics_data = [
        ['Métrique', 'Valeur', 'Unité'],
        ['⏱️ Temps scan moyen', '40-70', 'secondes'],
        ['🚀 Throughput', '~50', 'APK/heure'],
        ['💾 RAM totale', '~4', 'GB'],
        ['📦 Taille containers', '200-500', 'MB'],
        ['⚡ Latence réseau', '< 10', 'ms']
    ]
    metrics_table = Table(metrics_data, colWidths=[6*cm, 4*cm, 3*cm])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#fffbeb'), colors.white])
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 1*cm))
    perf_data = [45, 55, 70, 35, 50, 60, 40]
    perf_categories = ['APK', 'Secret', 'Crypto', 'Net', 'Report', 'Fix', 'CI']
    story.append(create_bar_chart(perf_data, perf_categories, "Temps d'exécution moyen (secondes)"))
    story.append(PageBreak())
    
    # CONCLUSION
    story.append(Paragraph("5. 🎯 Conclusion", styles['SectionTitle']))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "L'architecture microservices de <b>MobileSec-MS</b> offre une solution robuste, "
        "scalable et maintainable pour l'analyse de sécurité des applications mobiles Android.<br/><br/>"
        "<b>Points forts :</b><br/>✅ Indépendance des services<br/>✅ Scalabilité horizontale<br/>"
        "✅ Technologie polyglotte<br/>✅ Communication REST simple<br/>✅ Standards ouverts (SARIF, OWASP)",
        styles['BodyTextPro']))
    
    doc.build(story, onFirstPage=template.header_footer, onLaterPages=template.header_footer)
    
    file_size = os.path.getsize(filename) / 1024
    print(f"✅ PDF professionnel généré !")
    print(f"📄 Fichier : {filename}")
    print(f"💾 Taille : {file_size:.2f} KB")
    print(f"🎨 Design : Premium avec graphiques colorés")
    return filename

if __name__ == "__main__":
    try:
        generate_professional_pdf()
        print(f"\n🎉 PDF disponible dans docs/architecture/")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
