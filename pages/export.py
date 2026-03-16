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
    """Génère un rapport HTML avec graphiques Plotly"""
    
    from utils.charts import (
        generate_masi_chart, generate_monia_chart, generate_fx_chart,
        generate_inflation_gauge, generate_bdt_chart, generate_reserves_chart,
        convert_fig_to_html
    )
    
    # Générer tous les graphiques
    masi_html = convert_fig_to_html(generate_masi_chart())
    monia_html = convert_fig_to_html(generate_monia_chart())
    eur_mad_html = convert_fig_to_html(generate_fx_chart('EUR/MAD'))
    usd_mad_html = convert_fig_to_html(generate_fx_chart('USD/MAD'))
    inflation_html = convert_fig_to_html(generate_inflation_gauge(data['inflation']['value'], data['inflation']['target']))
    bdt_html = convert_fig_to_html(generate_bdt_chart())
    reserves_html = convert_fig_to_html(generate_reserves_chart())
    
    sections = st.session_state.export_selected_sections
    
    # Construction des sections
    sections_html = ""
    
    if 'bdc_statut' in sections:
        sections_html += f"""
        <div class="section">
            <h2>📈 Indices Boursiers</h2>
            <div class="chart-grid">
                <div class="chart-container">{masi_html}</div>
            </div>
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
            <div class="chart-grid-2">
                <div class="chart-container">{monia_html}</div>
                <div class="chart-container">{bdt_html}</div>
            </div>
            <div class="chart-grid-2">
                <div class="chart-container">{eur_mad_html}</div>
                <div class="chart-container">{usd_mad_html}</div>
            </div>
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
            <div class="chart-grid">
                <div class="chart-container">{inflation_html}</div>
            </div>
            <p><b>Valeur actuelle :</b> {data['inflation']['value']:.2f}%</p>
            <p><b>Cible BAM :</b> {data['inflation']['target']}%</p>
            <p><b>Statut :</b> {'✅ Dans la cible' if abs(data['inflation']['value'] - data['inflation']['target']) <= 0.5 else '⚠️ Hors cible'}</p>
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
        <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #005696 0%, #003d6b 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; margin-bottom: 30px; }}
            .header h1 {{ margin: 0; font-size: 32px; }}
            .kpi-container {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: Parfait, Ilyas ! Je vois le modèle de rapport professionnel que vous voulez. Je vais créer un **générateur de graphiques avancés** pour intégrer des visualisations similaires dans votre rapport HTML.

---

## 📊 CRÉATION DU MODULE DE GRAPHIQUES

Créez le fichier `utils/report_charts.py` :

```python
# =============================================================================
# NEWZ - Générateur de Graphiques pour Rapports
# Fichier : utils/report_charts.py
# =============================================================================

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import base64
from io import BytesIO

# -----------------------------------------------------------------------------
# 1. FONCTIONS DE GÉNÉRATION DE DONNÉES
# -----------------------------------------------------------------------------
def generate_bdt_data():
    """Génère les données pour la courbe BDT"""
    return {
        '1Y': 2.43,
        '5Y': 2.87,
        '10Y': 3.25,
        '15Y': 3.55
    }

def generate_monia_history(days=90):
    """Génère l'historique MONIA"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    base_rate = 3.00
    changes = np.random.normal(0, 0.02, days)
    rates = base_rate + np.cumsum(changes)
    rates = np.clip(rates, 2.0, 4.5)
    return pd.DataFrame({'date': dates, 'rate': rates})

def generate_masi_history(days=90):
    """Génère l'historique MASI"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    base_value = 12000
    returns = np.random.normal(0.0005, 0.015, days)
    values = base_value * np.cumprod(1 + returns)
    return pd.DataFrame({'date': dates, 'value': values})

def generate_fx_history(days=90, base_rate=10.75):
    """Génère l'historique des taux de change"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    changes = np.random.normal(0, 0.02, days)
    rates = base_rate + np.cumsum(changes)
    return pd.DataFrame({'date': dates, 'rate': rates})

def generate_reserves_history(days=90):
    """Génère l'historique des réserves obligatoires"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    base_reserves = 11500
    changes = np.random.normal(0, 150, days)
    reserves = base_reserves + np.cumsum(changes)
    return pd.DataFrame({'date': dates, 'reserves': reserves})

# -----------------------------------------------------------------------------
# 2. GRAPHIQUES INDIVIDUELS
# -----------------------------------------------------------------------------
def create_bdt_chart():
    """Crée le graphique BDT (1Y/5Y)"""
    data = generate_bdt_data()
    
    fig = go.Figure(data=[
        go.Bar(
            x=['1Y', '5Y', '10Y', '15Y'],
            y=[data['1Y'], data['5Y'], data['10Y'], data['15Y']],
            marker_color=['#005696', '#003d6b', '#00a8e8', '#0077b6'],
            text=[f"{v:.2f}%" for v in data.values()],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title='Maturité',
        yaxis_title='Taux (%)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def create_monia_chart():
    """Crée le graphique MONIA"""
    data = generate_monia_history(90)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['rate'],
        mode='lines',
        line=dict(color='#005696', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 86, 150, 0.1)'
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title='Date',
        yaxis_title='Taux (%)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def create_masi_chart():
    """Crée le graphique MASI"""
    data = generate_masi_history(90)
    current = data['value'].iloc[-1]
    change = ((current - data['value'].iloc[-2]) / data['value'].iloc[-2]) * 100
    color = '#28a745' if change >= 0 else '#dc3545'
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['value'],
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba(40, 167, 69, 0.1)' if change >= 0 else f'rgba(220, 53, 69, 0.1)'
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title='Date',
        yaxis_title='Indice MASI',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def create_eur_mad_chart():
    """Crée le graphique EUR/MAD"""
    data = generate_fx_history(90, 10.75)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['rate'],
        mode='lines',
        line=dict(color='#00a8e8', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 168, 232, 0.1)'
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title='Date',
        yaxis_title='EUR/MAD',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def create_inflation_gauge(value=-0.8, target_min=2, target_max=3):
    """Crée la jauge d'inflation"""
    # Déterminer la couleur selon la position
    if target_min - 0.5 <= value <= target_max + 0.5:
        color = '#28a745'  # Vert - dans la cible
        status = "Dans la cible"
    elif value < target_min:
        color = '#ffc107'  # Jaune - en dessous
        status = "En-dessous"
    else:
        color = '#dc3545'  # Rouge - au-dessus
        status = "Au-dessus"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Inflation (%)<br><span style='font-size: 12px'>{status}</span>", 
               'font': {'size': 14}},
        number={'font': {'size': 24}},
        gauge={
            'axis': {'range': [-2, 8], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [-2, 2], 'color': '#e8f5e9'},
                {'range': [2, 3], 'color': '#c8e6c9'},
                {'range': [3, 8], 'color': '#ffebee'}
            ],
            'threshold': {
                'line': {'color': '#dc3545', 'width': 4},
                'thickness': 0.75,
                'value': target_max + 0.5
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_reserves_chart():
    """Crée le graphique des réserves obligatoires"""
    data = generate_reserves_history(90)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['reserves'],
        mode='lines',
        line=dict(color='#005696', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 86, 150, 0.1)'
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title='Date',
        yaxis_title='Réserves (MDH)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def create_usd_mad_chart():
    """Crée le graphique USD/MAD"""
    data = generate_fx_history(90, 9.85)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['rate'],
        mode='lines',
        line=dict(color='#003d6b', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 61, 107, 0.1)'
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title='Date',
        yaxis_title='USD/MAD',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def create_qualitative_gauge(score=2, max_score=4):
    """Crée la jauge qualitative (sentiment/stress)"""
    # Déterminer la couleur
    if score <= 1:
        color = '#28a745'
        label = "Faible"
    elif score <= 2:
        color = '#ffc107'
        label = "Modéré"
    else:
        color = '#dc3545'
        label = "Élevé"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Sentiment & Stress<br><span style='font-size: 12px'>{label}</span>", 
               'font': {'size': 14}},
        number={'font': {'size': 32}},
        gauge={
            'axis': {'range': [0, max_score], 'tickwidth': 2},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [0, 1], 'color': '#e8f5e9'},
                {'range': [1, 2], 'color': '#fff9c4'},
                {'range': [2, 4], 'color': '#ffebee'}
            ]
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# -----------------------------------------------------------------------------
# 3. CONVERSION GRAPHIQUES → IMAGES BASE64
# -----------------------------------------------------------------------------
def fig_to_base64(fig, format='png', scale=2):
    """Convertit un graphique Plotly en image Base64"""
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format=format, scale=scale)
    img_bytes.seek(0)
    return base64.b64encode(img_bytes.read()).decode()

# -----------------------------------------------------------------------------
# 4. FONCTION PRINCIPALE - TOUS LES GRAPHIQUES
# -----------------------------------------------------------------------------
def generate_all_charts():
    """Génère tous les graphiques et les retourne en Base64"""
    
    charts = {
        'bdt': fig_to_base64(create_bdt_chart()),
        'monia': fig_to_base64(create_monias_chart()),
        'masi': fig_to_base64(create_masi_chart()),
        'eur_mad': fig_to_base64(create_eur_mad_chart()),
        'inflation': fig_to_base64(create_inflation_gauge()),
        'reserves': fig_to_base64(create_reserves_chart()),
        'usd_mad': fig_to_base64(create_usd_mad_chart()),
        'qualitative': fig_to_base64(create_qualitative_gauge())
    }
    
    return charts

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
