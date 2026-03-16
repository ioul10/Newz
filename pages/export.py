# =============================================================================
# NEWZ - Module Export de Rapport (HTML)
# Fichier : pages/export.py
# =============================================================================

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import sys
import base64

# Import des configurations
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import COLORS

# -----------------------------------------------------------------------------
# 1. INITIALISATION DE L'ÉTAT DE SESSION
# -----------------------------------------------------------------------------
if 'export_selected_sections' not in st.session_state:
    st.session_state.export_selected_sections = [
        'summary', 'bdc_statut', 'bam_indicators', 'inflation'
    ]
if 'export_preview_generated' not in st.session_state:
    st.session_state.export_preview_generated = False
if 'export_html_generated' not in st.session_state:
    st.session_state.export_html_generated = False

# -----------------------------------------------------------------------------
# 2. DONNÉES SIMULÉES POUR LE RAPPORT
# -----------------------------------------------------------------------------
def get_export_data():
    """Récupère les données à inclure dans le rapport"""
    return {
        'report_date': datetime.now().strftime('%d/%m/%Y'),
        'report_week': datetime.now().strftime('Semaine %V, %Y'),
        'masi': {'value': 12450.50, 'change': 0.85, 'volume': 45000000},
        'msi20': {'value': 1580.30, 'change': 1.20, 'volume': 38000000},
        'monia': {'value': 3.00, 'change': 0.05},
        'bt10': {'value': 3.85, 'change': -0.02},
        'usd_mad': {'value': 9.85, 'change': -0.15},
        'eur_mad': {'value': 10.75, 'change': 0.10},
        'inflation': {'value': -0.80, 'target': 2.5, 'status': 'low'},
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
# 3. HEADER DE LA PAGE
# -----------------------------------------------------------------------------
def render_export_header():
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
            Génération de rapports professionnels pour CDG Capital
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. ÉTAPE 1 : SÉLECTION DU CONTENU
# -----------------------------------------------------------------------------
def render_step1_selection():
    st.markdown("### Étape 1 : Sélection du Contenu")
    st.info("📋 Cochez les sections à inclure dans le rapport.")
    
    sections = {
        'summary': {'label': '📊 Synthèse Executive', 'desc': 'KPIs principaux, statut marché', 'default': True},
        'bdc_statut': {'label': '📈 BDC Statut (MASI/MSI20)', 'desc': 'Graphiques indices, top movers', 'default': True},
        'bam_indicators': {'label': '🏦 Indicateurs BAM', 'desc': 'MONIA, BDT, Devises', 'default': True},
        'inflation': {'label': '💹 Inflation & Macro', 'desc': 'IPC, jauge vs cible BAM', 'default': True},
        'statistics': {'label': '📊 Statistiques', 'desc': 'Corrélations, volatilité', 'default': False},
        'news': {'label': '📰 Actualités', 'desc': 'Top news de la semaine', 'default': False}
    }
    
    for key, section in sections.items():
        col1, col2 = st.columns([4, 1])
        with col1:
            is_selected = st.checkbox(
                f"**{section['label']}**",
                value=key in st.session_state.export_selected_sections,
                key=f"chk_{key}",
                help=section['desc']
            )
        with col2:
            st.success("✅ Inclus") if is_selected else st.caption("⚪ Exclu")
        
        if is_selected and key not in st.session_state.export_selected_sections:
            st.session_state.export_selected_sections.append(key)
        elif not is_selected and key in st.session_state.export_selected_sections:
            st.session_state.export_selected_sections.remove(key)
        
        st.caption(f"  {section['desc']}")
        st.markdown("---")
    
    # Options de format
    st.markdown("### ⚙️ Options")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.export_format = st.selectbox(
            "Format :", ['1 page (Executive)', '2 pages (Complet)'], index=0
        )
    with col2:
        st.session_state.export_include_charts = st.checkbox("Inclure graphiques", value=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("▶️ Étape 2 : Prévisualisation", type="primary", use_container_width=True,
                     disabled=len(st.session_state.export_selected_sections) == 0):
            st.session_state.export_preview_generated = True
            st.rerun()

# -----------------------------------------------------------------------------
# 5. ÉTAPE 2 : PRÉVISUALISATION
# -----------------------------------------------------------------------------
def render_step2_preview():
    st.markdown("### Étape 2 : Prévisualisation")
    st.info("👀 Aperçu du contenu du rapport.")
    
    data = get_export_data()
    
    st.markdown("#### 📄 Page 1 : Synthèse & Marchés")
    
    st.markdown(f"""
    <div style="
        border: 2px solid {COLORS['primary']};
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        background: white;
    ">
        <div style="text-align: center; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 18px; font-weight: bold; color: {COLORS['primary']};">CDG CAPITAL</p>
            <p style="margin: 5px 0; font-size: 14px; color: #666;">Newz — Market Data Weekly</p>
            <p style="margin: 5px 0; font-size: 12px; color: #999;">{data['report_week']}</p>
        </div>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <p style="margin: 0; font-size: 14px; font-weight: bold;">📊 KPIs Principaux</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;">
                <div style="text-align: center;">
                    <p style="margin: 0; font-size: 11px; color: #666;">MASI</p>
                    <p style="margin: 5px 0; font-size: 16px; font-weight: bold; color: {COLORS['primary']};">{data['masi']['value']:,.0f}</p>
                    <p style="margin: 0; font-size: 12px; color: {'green' if data['masi']['change'] > 0 else 'red'};">{data['masi']['change']:+.2f}%</p>
                </div>
                <div style="text-align: center;">
                    <p style="margin: 0; font-size: 11px; color: #666;">EUR/MAD</p>
                    <p style="margin: 5px 0; font-size: 16px; font-weight: bold;">{data['eur_mad']['value']:.4f}</p>
                    <p style="margin: 0; font-size: 12px; color: {'green' if data['eur_mad']['change'] > 0 else 'red'};">{data['eur_mad']['change']:+.2f}%</p>
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
    
    st.markdown("**Sections incluses :**")
    for section in st.session_state.export_selected_sections:
        st.write(f"✅ {section}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("◀ Retour", use_container_width=True):
            st.session_state.export_preview_generated = False
            st.rerun()
    with col2:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.rerun()
    with col3:
        if st.button("▶️ Étape 3 : Générer", type="primary", use_container_width=True):
            st.session_state.export_html_generated = True
            st.rerun()

# -----------------------------------------------------------------------------
# 6. GÉNÉRATEUR HTML PROFESSIONNEL
# -----------------------------------------------------------------------------
def generate_report_html(data):
    """Génère un rapport HTML professionnel"""
    
    sections = st.session_state.export_selected_sections
    
    # Construction dynamique des sections HTML
    sections_html = ""
    
    if 'bdc_statut' in sections:
        sections_html += f"""
        <div class="section">
            <h2>📈 Indices Boursiers</h2>
            <table>
                <thead><tr><th>Indice</th><th>Valeur</th><th>Variation</th><th>Volume</th></tr></thead>
                <tbody>
                    <tr><td><b>MASI</b></td><td>{data['masi']['value']:,.0f}</td>
                        <td class="{'positive' if data['masi']['change'] > 0 else 'negative'}">{data['masi']['change']:+.2f}%</td>
                        <td>{data['masi']['volume']:,}</td></tr>
                    <tr><td><b>MSI20</b></td><td>{data['msi20']['value']:,.0f}</td>
                        <td class="{'positive' if data['msi20']['change'] > 0 else 'negative'}">{data['msi20']['change']:+.2f}%</td>
                        <td>{data['msi20']['volume']:,}</td></tr>
                </tbody>
            </table>
        </div>
        """
    
    if 'bam_indicators' in sections:
        sections_html += f"""
        <div class="section">
            <h2>🏦 Taux & Devises</h2>
            <table>
                <thead><tr><th>Indicateur</th><th>Valeur</th><th>Variation</th></tr></thead>
                <tbody>
                    <tr><td>MONIA</td><td>{data['monia']['value']:.2f}%</td><td>{data['monia']['change']:+.2f}%</td></tr>
                    <tr><td>USD/MAD</td><td>{data['usd_mad']['value']:.4f}</td><td>{data['usd_mad']['change']:+.2f}%</td></tr>
                    <tr><td>EUR/MAD</td><td>{data['eur_mad']['value']:.4f}</td><td>{data['eur_mad']['change']:+.2f}%</td></tr>
                </tbody>
            </table>
        </div>
        """
    
    if 'inflation' in sections:
        sections_html += f"""
        <div class="section">
            <h2>💹 Inflation</h2>
            <p><b>Valeur actuelle :</b> {data['inflation']['value']:.2f}%</p>
            <p><b>Cible BAM :</b> {data['inflation']['target']}%</p>
            <p><b>Statut :</b> {'✅ Dans la cible' if abs(data['inflation']['value'] - data['inflation']['target']) <= 0.5 else '⚠️ Hors cible'}</p>
        </div>
        """
    
    if 'statistics' in sections:
        sections_html += """
        <div class="section">
            <h2>📊 Statistiques Clés</h2>
            <p>• Corrélation moyenne MSI20 : 0.65</p>
            <p>• Volatilité MASI (30j) : 1.2%</p>
            <p>• Beta moyen des valeurs : 1.05</p>
        </div>
        """
    
    if 'news' in sections:
        sections_html += """
        <div class="section">
            <h2>📰 Actualités Marquantes</h2>
            <ul>
                <li>Bank Al-Maghrib maintient son taux directeur à 3%</li>
                <li>Le MASI franchit la barre des 12 500 points</li>
                <li>L'inflation au Maroc ralentit à 0,8% en glissement annuel</li>
            </ul>
        </div>
        """
    
    # Top movers
    gainers_html = ''.join([f'<li>{g["name"]}: <b style="color:#28a745">{g["change"]:+.1f}%</b></li>' for g in data['top_gainers']])
    losers_html = ''.join([f'<li>{l["name"]}: <b style="color:#dc3545">{l["change"]:+.1f}%</b></li>' for l in data['top_losers']])
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Newz Report - {data['report_date']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #005696 0%, #003d6b 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; margin-bottom: 30px; }}
            .header h1 {{ margin: 0; font-size: 32px; }}
            .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
            .kpi-container {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }}
            .kpi-box {{ background: #f8f9fa; border-left: 5px solid #005696; padding: 20px; border-radius: 8px; text-align: center; }}
            .kpi-box h3 {{ margin: 0 0 10px 0; color: #005696; font-size: 14px; text-transform: uppercase; }}
            .kpi-box .value {{ font-size: 28px; font-weight: bold; color: #333; }}
            .positive {{ color: #28a745; }} .negative {{ color: #dc3545; }}
            .section {{ background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 25px; margin-bottom: 25px; }}
            .section h2 {{ color: #005696; border-bottom: 3px solid #005696; padding-bottom: 10px; margin-top: 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #005696; color: white; font-weight: bold; }}
            tr:nth-child(even) {{ background: #f8f9fa; }}
            .footer {{ margin-top: 50px; padding: 25px; background: #f8f9fa; border-radius: 8px; text-align: center; font-size: 12px; color: #666; border-top: 4px solid #005696; }}
            .stamp {{ margin-top: 30px; display: inline-block; border: 4px solid #dc3545; color: #dc3545; padding: 15px 40px; font-weight: bold; font-size: 20px; transform: rotate(-3deg); opacity: 0.8; }}
            .movers-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
            .movers-grid h3 {{ color: #005696; border-bottom: 2px solid #005696; padding-bottom: 8px; }}
            .movers-grid ul {{ list-style: none; padding: 0; }}
            .movers-grid li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
            @media print {{ body {{ margin: 0; }} .no-print {{ display: none; }} }}
        </style>
    </head>
    <body>
        <div class="no-print" style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center;">
            <strong>💡 Astuce :</strong> Appuyez sur <kbd>Ctrl+P</kbd> (ou Cmd+P) pour imprimer cette page en PDF
        </div>
        
        <div class="header">
            <h1>🏦 CDG CAPITAL</h1>
            <p><b>Newz — Market Data Weekly</b></p>
            <p>{data['report_week']}</p>
            <p style="font-size: 12px; margin-top: 10px;">Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
        </div>
        
        <div class="kpi-container">
            <div class="kpi-box"><h3>📊 MASI</h3><div class="value">{data['masi']['value']:,.0f}</div><div class="change {'positive' if data['masi']['change'] > 0 else 'negative'}">{data['masi']['change']:+.2f}%</div></div>
            <div class="kpi-box"><h3>💶 EUR/MAD</h3><div class="value">{data['eur_mad']['value']:.4f}</div><div class="change {'positive' if data['eur_mad']['change'] > 0 else 'negative'}">{data['eur_mad']['change']:+.2f}%</div></div>
            <div class="kpi-box"><h3>💹 Inflation</h3><div class="value">{data['inflation']['value']:.2f}%</div><div style="font-size: 12px; color: #666; margin-top: 5px;">Cible: {data['inflation']['target']}%</div></div>
        </div>
        
        {sections_html}
        
        <div class="section">
            <h2>📊 Top Movers</h2>
            <div class="movers-grid">
                <div><h3 style="color:#28a745">🟢 Top Gainers</h3><ul>{gainers_html}</ul></div>
                <div><h3 style="color:#dc3545">🔴 Top Losers</h3><ul>{losers_html}</ul></div>
            </div>
        </div>
        
        <div class="footer">
            <p><b style="color: #005696; font-size: 14px;">CDG Capital — Market Data Team</b></p>
            <p>Newz v1.0 | Usage interne uniquement | Document confidentiel</p>
            <p style="margin-top: 15px; font-size: 11px;">Sources : Bourse de Casablanca | Bank Al-Maghrib | HCP</p>
            <div class="stamp">ADMIN<br/>CONFIDENTIEL</div>
        </div>
        
        <div class="no-print" style="margin-top: 30px; text-align: center; padding: 20px; background: #e8f5e9; border-radius: 8px;">
            <p style="margin: 0 0 15px 0; font-size: 16px; font-weight: bold; color: #2e7d32;">📄 Pour sauvegarder en PDF :</p>
            <p style="margin: 0; color: #666;">Appuyez sur <kbd style="background: white; padding: 5px 10px; border-radius: 4px; border: 1px solid #ccc;">Ctrl+P</kbd> puis sélectionnez "Enregistrer au format PDF"</p>
        </div>
    </body>
    </html>
    """
    return html

def get_download_link(html_content, filename="newz_report.html"):
    """Génère un lien de téléchargement pour le fichier HTML"""
    b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    return f"""
    <a href="data:text/html;base64,{b64}" download="{filename}" style="text-decoration: none;">
        <button style="
            background: linear-gradient(135deg, #005696 0%, #003d6b 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0, 86, 150, 0.3);
            transition: all 0.3s ease;
        ">📥 Télécharger le Rapport (HTML)</button>
    </a>
    <p style="color: #666; font-size: 13px; margin-top: 10px;">
        💡 <b>Astuce :</b> Ouvrez le fichier HTML et appuyez sur Ctrl+P pour l'imprimer en PDF
    </p>
    """

# -----------------------------------------------------------------------------
# 7. ÉTAPE 3 : GÉNÉRATION HTML
# -----------------------------------------------------------------------------
def render_step3_generation():
    st.markdown("### Étape 3 : Rapport Généré")
    
    data = get_export_data()
    html_content = generate_report_html(data)
    
    st.success("✅ Rapport généré avec succès !")
    
    # Lien de téléchargement
    st.markdown(get_download_link(html_content), unsafe_allow_html=True)
    
    # Aperçu optionnel
    if st.checkbox("👁️ Voir l'aperçu HTML"):
        st.components.v1.html(html_content, height=800, scrolling=True)
    
    # Infos fichier
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Format", value="HTML")
    with col2:
        st.metric(label="Taille estimée", value="~15 KB")
    with col3:
        st.metric(label="Date", value=datetime.now().strftime('%H:%M'))
    
    # Options supplémentaires
    st.markdown("---")
    st.markdown("### 📧 Options de Diffusion")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**📧 Envoyer par email**\n\nFonctionnalité à implémenter :\n- Configuration SMTP\n- Liste de diffusion")
    with col2:
        st.info("**🗄️ Archiver sur réseau**\n\nFonctionnalité à implémenter :\n- Chemin réseau configurable\n- Historique des exports")
    
    # Bouton nouveau rapport
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Générer un nouveau rapport", use_container_width=True):
        st.session_state.export_preview_generated = False
        st.session_state.export_html_generated = False
        st.rerun()

# -----------------------------------------------------------------------------
# 8. FONCTION PRINCIPALE
# -----------------------------------------------------------------------------
def render():
    render_export_header()
    
    # Barre de progression
    st.markdown("### 📋 Progression")
    
    if not st.session_state.export_preview_generated:
        current_step = 1
    elif not st.session_state.export_html_generated:
        current_step = 2
    else:
        current_step = 3
    
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
    
    # Affichage selon l'état
    if not st.session_state.export_preview_generated:
        render_step1_selection()
    elif not st.session_state.export_html_generated:
        render_step2_preview()
    else:
        render_step3_generation()
    
    # Footer
    st.markdown("---")
    st.caption(f"📤 Export HTML | Charte CDG Capital | Sources : Bourse de Casablanca, Bank Al-Maghrib")

# -----------------------------------------------------------------------------
# 9. POINT D'ENTRÉE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    render()
