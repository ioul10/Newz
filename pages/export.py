# =============================================================================
# NEWZ - Module Export de Rapport PDF
# Fichier : pages/export.py
# =============================================================================

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import sys
import base64
from io import BytesIO

# Import des configurations
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import COLORS, LOGO_CDG_PATH, ADMIN_STAMP_PATH, REPORTS_DIR, PDF_CONFIG

# -----------------------------------------------------------------------------
# 1. INITIALISATION DE L'ÉTAT DE SESSION
# -----------------------------------------------------------------------------
if 'export_selected_sections' not in st.session_state:
    st.session_state.export_selected_sections = [
        'summary', 'bdc_statut', 'bam_indicators', 'inflation'
    ]
if 'export_preview_generated' not in st.session_state:
    st.session_state.export_preview_generated = False
if 'export_pdf_path' not in st.session_state:
    st.session_state.export_pdf_path = None

# -----------------------------------------------------------------------------
# 2. FONCTIONS DE GÉNÉRATION DE DONNÉES SIMULÉES
# -----------------------------------------------------------------------------
def get_export_data():
    """Récupère les données à inclure dans le rapport"""
    return {
        'report_date': datetime.now().strftime('%d/%m/%Y'),
        'report_week': datetime.now().strftime('Semaine %V, %Y'),
        'masi': {
            'value': 12450.50,
            'change': 0.85,
            'volume': 45000000
        },
        'msi20': {
            'value': 1580.30,
            'change': 1.20,
            'volume': 38000000
        },
        'monia': {
            'value': 3.00,
            'change': 0.05
        },
        'bt10': {
            'value': 3.85,
            'change': -0.02
        },
        'usd_mad': {
            'value': 9.85,
            'change': -0.15
        },
        'eur_mad': {
            'value': 10.75,
            'change': 0.10
        },
        'inflation': {
            'value': -0.80,
            'target': 2.5,
            'status': 'low'
        },
        'market_status': 'Ouvert',
        'top_gainers': [
            {'name': 'Attijariwafa Bank', 'change': 3.5},
            {'name': 'Maroc Telecom', 'change': 2.8},
            {'name': 'LafargeHolcim', 'change': 2.1}
        ],
        'top_losers': [
            {'name': 'BCP', 'change': -1.5},
            {'name': 'Cosumar', 'change': -1.2},
            {'name': 'Sonasid', 'change': -0.9}
        ]
    }

# -----------------------------------------------------------------------------
# 3. AFFICHAGE DU HEADER EXPORT
# -----------------------------------------------------------------------------
def render_export_header():
    """Affiche le header de la page Export"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 10px;
        margin-bottom: 25px;
    ">
        <h2 style="margin: 0; font-size: 24px;">📤 Export de Rapport</h2>
        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 14px;">
            Génération de rapports PDF professionnels pour CDG Capital
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. ÉTAPE 1 : SÉLECTION DU CONTENU
# -----------------------------------------------------------------------------
def render_step1_selection():
    """Affiche l'étape 1 : Sélection du contenu du rapport"""
    st.markdown("### Étape 1 : Sélection du Contenu")
    
    st.info("📋 Cochez les sections que vous souhaitez inclure dans le rapport PDF.")
    
    # Sections disponibles
    sections = {
        'summary': {
            'label': '📊 Synthèse Executive',
            'description': 'KPIs principaux, statut marché, highlights de la semaine',
            'default': True
        },
        'bdc_statut': {
            'label': '📈 BDC Statut (MASI/MSI20)',
            'description': 'Graphiques des indices, top movers, volumes',
            'default': True
        },
        'bam_indicators': {
            'label': '🏦 Indicateurs BAM',
            'description': 'MONIA, Courbe BDT, Devises (MAD/USD, MAD/EUR)',
            'default': True
        },
        'inflation': {
            'label': '💹 Inflation & Macro',
            'description': 'Indice IPC, jauge vs cible BAM, tendance',
            'default': True
        },
        'statistics': {
            'label': '📊 Statistiques de Marché',
            'description': 'Corrélations MSI20, volatilité, contributions',
            'default': False
        },
        'news': {
            'label': '📰 Actualités Marquantes',
            'description': 'Top 3 news de la semaine avec impact',
            'default': False
        }
    }
    
    # Affichage des checkboxes
    for key, section in sections.items():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            is_selected = st.checkbox(
                f"**{section['label']}**",
                value=key in st.session_state.export_selected_sections,
                key=f"chk_{key}",
                help=section['description']
            )
        
        with col2:
            if is_selected:
                st.success("✅ Inclus")
            else:
                st.caption("⚪ Exclu")
        
        if is_selected:
            if key not in st.session_state.export_selected_sections:
                st.session_state.export_selected_sections.append(key)
        else:
            if key in st.session_state.export_selected_sections:
                st.session_state.export_selected_sections.remove(key)
        
        st.caption(f"  {section['description']}")
        st.markdown("---")
    
    # Options de format
    st.markdown("### ⚙️ Options de Format")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_format = st.selectbox(
            "Format du rapport :",
            options=['1 page (Executive)', '2 pages (Complet)'],
            index=0
        )
        st.session_state.export_format = report_format
    
    with col2:
        include_charts = st.checkbox(
            "Inclure les graphiques",
            value=True
        )
        st.session_state.export_include_charts = include_charts
    
    # Bouton pour passer à l'étape 2
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        if st.button(
            "▶️ Étape 2 : Prévisualisation",
            type="primary",
            use_container_width=True,
            disabled=len(st.session_state.export_selected_sections) == 0
        ):
            st.session_state.export_preview_generated = True
            st.rerun()

# -----------------------------------------------------------------------------
# 5. ÉTAPE 2 : PRÉVISUALISATION
# -----------------------------------------------------------------------------
def render_step2_preview():
    """Affiche l'étape 2 : Prévisualisation du rapport"""
    st.markdown("### Étape 2 : Prévisualisation")
    
    st.info("👀 Aperçu du contenu qui sera inclus dans le PDF.")
    
    data = get_export_data()
    
    # ---------------------------------------------------------------------
    # APERÇU PAGE 1
    # ---------------------------------------------------------------------
    st.markdown("#### 📄 Page 1 : Synthèse & Marchés")
    
    preview_container = st.container()
    
    with preview_container:
        # En-tête simulé
        st.markdown(f"""
        <div style="
            border: 2px solid {COLORS['primary']};
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background: white;
        ">
            <div style="text-align: center; margin-bottom: 20px;">
                <p style="margin: 0; font-size: 18px; font-weight: bold; color: {COLORS['primary']};">
                    CDG CAPITAL
                </p>
                <p style="margin: 5px 0; font-size: 14px; color: #666;">
                    Newz — Market Data Weekly
                </p>
                <p style="margin: 5px 0; font-size: 12px; color: #999;">
                    {data['report_week']}
                </p>
            </div>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p style="margin: 0; font-size: 14px; font-weight: bold;">📊 KPIs Principaux</p>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;">
                    <div style="text-align: center;">
                        <p style="margin: 0; font-size: 11px; color: #666;">MASI</p>
                        <p style="margin: 5px 0; font-size: 16px; font-weight: bold; color: {COLORS['primary']};">
                            {data['masi']['value']:,.0f}
                        </p>
                        <p style="margin: 0; font-size: 12px; color: {'green' if data['masi']['change'] > 0 else 'red'};">
                            {data['masi']['change']:+.2f}%
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <p style="margin: 0; font-size: 11px; color: #666;">EUR/MAD</p>
                        <p style="margin: 5px 0; font-size: 16px; font-weight: bold;">{data['eur_mad']['value']:.4f}</p>
                        <p style="margin: 0; font-size: 12px; color: {'green' if data['eur_mad']['change'] > 0 else 'red'};">
                            {data['eur_mad']['change']:+.2f}%
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <p style="margin: 0; font-size: 11px; color: #666;">Inflation</p>
                        <p style="margin: 5px 0; font-size: 16px; font-weight: bold;">{data['inflation']['value']:.2f}%</p>
                        <p style="margin: 0; font-size: 12px; color: #666;">Cible: {data['inflation']['target']}%</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sections sélectionnées
        st.markdown("**Sections incluses :**")
        for section in st.session_state.export_selected_sections:
            st.write(f"✅ {section}")
    
    # ---------------------------------------------------------------------
    # BOUTONS DE NAVIGATION
    # ---------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button(
            "◀ Retour à la sélection",
            use_container_width=True
        ):
            st.session_state.export_preview_generated = False
            st.rerun()
    
    with col2:
        if st.button(
            "🔄 Actualiser l'aperçu",
            use_container_width=True
        ):
            st.rerun()
    
    with col3:
        if st.button(
            "▶️ Étape 3 : Générer PDF",
            type="primary",
            use_container_width=True
        ):
            # Génération du PDF
            pdf_path = generate_pdf_report(data)
            st.session_state.export_pdf_path = pdf_path
            st.rerun()

# -----------------------------------------------------------------------------
# 6. ÉTAPE 3 : GÉNÉRATION PDF
# -----------------------------------------------------------------------------
def render_step3_generation():
    """Affiche l'étape 3 : Génération et téléchargement du PDF"""
    st.markdown("### Étape 3 : Rapport Généré")
    
    if not st.session_state.export_pdf_path:
        st.warning("⚠️ Aucun PDF généré. Veuillez retourner à l'étape 2.")
        return
    
    pdf_path = Path(st.session_state.export_pdf_path)
    
    if pdf_path.exists():
        st.success("✅ Rapport PDF généré avec succès !")
        
        # ---------------------------------------------------------------------
        # INFORMATIONS DU FICHIER
        # ---------------------------------------------------------------------
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Fichier",
                value=pdf_path.name
            )
        
        with col2:
            file_size = pdf_path.stat().st_size / 1024  # KB
            st.metric(
                label="Taille",
                value=f"{file_size:.1f} KB"
            )
        
        with col3:
            st.metric(
                label="Date",
                value=datetime.now().strftime('%H:%M')
            )
        
        # ---------------------------------------------------------------------
        # BOUTON DE TÉLÉCHARGEMENT
        # ---------------------------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Lecture du fichier PDF
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        st.download_button(
            label="📥 Télécharger le PDF",
            data=pdf_bytes,
            file_name=pdf_path.name,
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
        
        # ---------------------------------------------------------------------
        # OPTIONS SUPPLÉMENTAIRES
        # ---------------------------------------------------------------------
        st.markdown("### 📧 Options de Diffusion")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **📧 Envoyer par email**
            
            Fonctionnalité à implémenter :
            - Configuration SMTP
            - Liste de diffusion
            - Personnalisation du message
            """)
        
        with col2:
            st.info("""
            **🗄️ Archiver sur réseau**
            
            Fonctionnalité à implémenter :
            - Chemin réseau configurable
            - Nommage automatique
            - Historique des exports
            """)
        
        # ---------------------------------------------------------------------
        # BOUTON NOUVEAU RAPPORT
        # ---------------------------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button(
            "🔄 Générer un nouveau rapport",
            use_container_width=True
        ):
            # Reset de l'état
            st.session_state.export_preview_generated = False
            st.session_state.export_pdf_path = None
            st.rerun()
    
    else:
        st.error(f"❌ Le fichier PDF n'a pas été trouvé : {pdf_path}")

# -----------------------------------------------------------------------------
# 7. GÉNÉRATION DU PDF (SIMULÉE)
# -----------------------------------------------------------------------------
def generate_pdf_report(data):
    """
    Génère le rapport PDF
    TODO: Implémenter la vraie génération avec WeasyPrint
    """
    
    # Nom du fichier
    filename = f"newz_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = REPORTS_DIR / filename
    
    # Pour cette version, on crée un PDF placeholder
    # Dans la version finale, utiliser WeasyPrint avec template HTML
    
    try:
        # Création d'un PDF simple avec reportlab (ou fichier placeholder)
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        
        # Création du document
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=PDF_CONFIG['margin_right'],
            leftMargin=PDF_CONFIG['margin_left'],
            topMargin=PDF_CONFIG['margin_top'],
            bottomMargin=PDF_CONFIG['margin_bottom']
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # -----------------------------------------------------------------
        # EN-TÊTE (Logo CDG Capital)
        # -----------------------------------------------------------------
        if LOGO_CDG_PATH.exists():
            try:
                logo = Image(str(LOGO_CDG_PATH), width=150, height=50)
                logo.hAlign = 'CENTER'
                elements.append(logo)
                elements.append(Spacer(1, 20))
            except Exception as e:
                elements.append(Paragraph(f"<b>CDG CAPITAL</b>", styles['Title']))
                elements.append(Spacer(1, 10))
        else:
            elements.append(Paragraph(f"<b>CDG CAPITAL</b>", styles['Title']))
            elements.append(Spacer(1, 10))
        
        # Titre du rapport
        elements.append(Paragraph(
            f"<b>Newz — Market Data Weekly</b>",
            ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor(COLORS['primary']))
        ))
        elements.append(Spacer(1, 5))
        
        elements.append(Paragraph(
            f"{data['report_week']} | Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
            ParagraphStyle('CustomSubtitle', parent=styles['Normal'], fontSize=10, textColor=colors.grey)
        ))
        elements.append(Spacer(1, 30))
        
        # -----------------------------------------------------------------
        # CORPS DU RAPPORT (KPIs et sections)
        # -----------------------------------------------------------------
        # Tableau des KPIs
        kpi_data = [
            ['Indicateur', 'Valeur', 'Variation'],
            ['MASI', f"{data['masi']['value']:,.0f}", f"{data['masi']['change']:+.2f}%"],
            ['MSI20', f"{data['msi20']['value']:,.0f}", f"{data['msi20']['change']:+.2f}%"],
            ['EUR/MAD', f"{data['eur_mad']['value']:.4f}", f"{data['eur_mad']['change']:+.2f}%"],
            ['USD/MAD', f"{data['usd_mad']['value']:.4f}", f"{data['usd_mad']['change']:+.2f}%"],
            ['MONIA', f"{data['monia']['value']:.2f}%", f"{data['monia']['change']:+.2f}%"],
            ['Inflation', f"{data['inflation']['value']:.2f}%", f"Cible: {data['inflation']['target']}%"]
        ]
        
        kpi_table = Table(kpi_data, colWidths=[200, 150, 150])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['primary'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(kpi_table)
        elements.append(Spacer(1, 30))
        
        # -----------------------------------------------------------------
        # SECTIONS SÉLECTIONNÉES
        # -----------------------------------------------------------------
        elements.append(Paragraph(f"<b>Sections incluses :</b>", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        for section in st.session_state.export_selected_sections:
            elements.append(Paragraph(f"• {section}", styles['Normal']))
        
        elements.append(Spacer(1, 30))
        
        # -----------------------------------------------------------------
        # PIED DE PAGE (Cachet Admin)
        # -----------------------------------------------------------------
        elements.append(Spacer(1, 50))
        
        elements.append(Paragraph(
            f"<b>Statut :</b> {data['market_status']} | <b>Version :</b> Newz v1.0",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey)
        ))
        
        elements.append(Spacer(1, 10))
        
        elements.append(Paragraph(
            "Généré par Newz — Usage interne CDG Capital — Confidentiel",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=1)
        ))
        
        # Si le cachet admin existe, on pourrait l'ajouter ici
        if ADMIN_STAMP_PATH.exists():
            elements.append(Spacer(1, 20))
            # elements.append(Image(str(ADMIN_STAMP_PATH), width=100, height=100))
        
        # -----------------------------------------------------------------
        # GÉNÉRATION
        # -----------------------------------------------------------------
        doc.build(elements)
        
        return str(pdf_path)
        
    except Exception as e:
        st.error(f"Erreur de génération PDF : {str(e)}")
        
        # Fallback : créer un fichier placeholder
        pdf_path.write_text(f"Rapport Newz généré le {datetime.now()}\nSections: {st.session_state.export_selected_sections}")
        return str(pdf_path)

# -----------------------------------------------------------------------------
# 8. FONCTION DE RENDU PRINCIPAL
# -----------------------------------------------------------------------------
def render():
    """Affiche la page Export"""
    
    # ---------------------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------------------
    render_export_header()
    
    # ---------------------------------------------------------------------
    # BARRE DE PROGRESSION
    # ---------------------------------------------------------------------
    st.markdown("### 📋 Progression")
    
    if not st.session_state.export_preview_generated:
        current_step = 1
    elif st.session_state.export_pdf_path:
        current_step = 3
    else:
        current_step = 2
    
    progress_steps = ['1. Sélection', '2. Prévisualisation', '3. Génération']
    
    cols = st.columns(3)
    for i, step in enumerate(progress_steps):
        with cols[i]:
            if i + 1 == current_step:
                st.success(f"**{step}** ✅")
            elif i + 1 < current_step:
                st.success(f"{step} ✓")
            else:
                st.caption(f"{step}")
    
    st.markdown("---")
    
    # ---------------------------------------------------------------------
    # AFFICHAGE SELON L'ÉTAT
    # ---------------------------------------------------------------------
    if not st.session_state.export_preview_generated:
        render_step1_selection()
    elif not st.session_state.export_pdf_path:
        render_step2_preview()
    else:
        render_step3_generation()
    
    # ---------------------------------------------------------------------
    # FOOTER DE PAGE
    # ---------------------------------------------------------------------
    st.markdown("---")
    st.caption(f"📤 Export PDF | Charte graphique CDG Capital | {PDF_CONFIG['format']} | Sources : Bourse de Casablanca, Bank Al-Maghrib")

# -----------------------------------------------------------------------------
# 9. POINT D'ENTRÉE POUR TEST UNITAIRE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    render()
