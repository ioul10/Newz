# =============================================================================
# NEWZ - Module Macronews (Actualités + Inflation)
# Fichier : pages/macronews.py
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import sys
import random

# Import des configurations
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import COLORS, DATA_DIR

# -----------------------------------------------------------------------------
# 1. INITIALISATION DE L'ÉTAT DE SESSION
# -----------------------------------------------------------------------------
if 'news_read' not in st.session_state:
    st.session_state.news_read = []
if 'news_popup_shown' not in st.session_state:
    st.session_state.news_popup_shown = False
if 'inflation_target' not in st.session_state:
    st.session_state.inflation_target = 2.5  # Cible BAM (2-3%)

# -----------------------------------------------------------------------------
# 2. FONCTIONS DE GÉNÉRATION DE DONNÉES SIMULÉES
# -----------------------------------------------------------------------------
def generate_news_feed():
    """Génère un flux d'actualités financières simulées"""
    
    news_categories = {
        'high': ['🔴 Haute Impact', COLORS['danger']],
        'medium': ['🟡 Moyenne Impact', COLORS['warning']],
        'low': ['🟢 Faible Impact', COLORS['success']]
    }
    
    news_sources = ['Ilboursa', 'Bourse de Casablanca', 'Leconomiste', 'Medias24', 'BAM']
    
    headlines = [
        "Bank Al-Maghrib maintient son taux directeur à 3%",
        "Le MASI franchit la barre des 12 500 points",
        "Attijariwafa Bank annonce des résultats record",
        "L'inflation au Maroc ralentit à 0,8% en glissement annuel",
        "Maroc Telecom investit 2 milliards dans la 5G",
        "La Bourse de Casablanca attire de nouveaux investisseurs étrangers",
        "Le Dirham se stabilise face à l'Euro",
        "Les réserves de change atteignent un niveau historique",
        "Cosumar lance un nouveau plan d'investissement",
        "Le secteur bancaire marocain affiche une croissance de 8%",
        "La BRVM et la Bourse de Casablanca signent un partenariat",
        "Les exportations de phosphates en hausse de 15%",
        "Inflation : Les prix alimentaires se stabilisent",
        "Le taux de chômage baisse au 4ème trimestre",
        "Nouvelle émission obligataire de l'État annoncée"
    ]
    
    news_items = []
    
    for i in range(15):
        impact = random.choice(['high', 'medium', 'low'])
        hours_ago = random.randint(1, 72)
        
        news_items.append({
            'id': i + 1,
            'title': headlines[i % len(headlines)],
            'summary': f"Analyse détaillée de l'actualité financière marocaine. Impact sur le marché boursier et les taux.",
            'source': random.choice(news_sources),
            'category': impact,
            'category_label': news_categories[impact][0],
            'category_color': news_categories[impact][1],
            'timestamp': datetime.now() - timedelta(hours=hours_ago),
            'url': f"https://www.ilboursa.com/news/{i}",
            'read': i in st.session_state.news_read
        })
    
    return news_items

def generate_inflation_history(months=24):
    """Génère l'historique de l'inflation (IPC)"""
    dates = pd.date_range(end=datetime.now(), periods=months, freq='M')
    
    # Simulation réaliste de l'inflation marocaine
    base_inflation = 2.5
    inflation_values = []
    
    for i in range(months):
        # Variation progressive avec pics occasionnels
        variation = np.random.normal(0, 0.3)
        if i in [6, 7, 8]:  # Pic simulé
            variation += 1.5
        inflation_values.append(base_inflation + variation)
    
    inflation_values = np.clip(inflation_values, -1, 8)
    
    return pd.DataFrame({
        'date': dates,
        'inflation': inflation_values,
        'target': [st.session_state.inflation_target] * months
    })

def get_inflation_status(current_inflation):
    """Détermine le statut de l'inflation par rapport à la cible BAM"""
    target = st.session_state.inflation_target
    tolerance = 0.5
    
    if abs(current_inflation - target) <= tolerance:
        return 'on_target', '🟢 Dans la cible', COLORS['success']
    elif current_inflation > target + tolerance:
        return 'high', '🔴 Au-dessus de la cible', COLORS['danger']
    else:
        return 'low', '🟡 En-dessous de la cible', COLORS['warning']

# -----------------------------------------------------------------------------
# 3. POPUP D'ALERTE NEWS IMPORTANTE
# -----------------------------------------------------------------------------
def render_news_popup():
    """Affiche une popup pour les news importantes (non-intrusive)"""
    
    if st.session_state.news_popup_shown:
        return
    
    news_items = generate_news_feed()
    high_impact_news = [n for n in news_items if n['category'] == 'high']
    
    if high_impact_news:
        # Afficher seulement une fois par session
        st.session_state.news_popup_shown = True
        
        news = high_impact_news[0]
        
        st.markdown(f"""
        <div style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            background: white;
            border-left: 5px solid {COLORS['danger']};
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            padding: 20px;
            z-index: 1000;
            animation: slideIn 0.5s ease-out;
        ">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <p style="margin: 0; font-size: 12px; color: {COLORS['danger']}; font-weight: bold;">
                        ⚠️ NEWS IMPORTANTE
                    </p>
                    <h4 style="margin: 10px 0 5px 0; font-size: 14px; color: #333;">
                        {news['title']}
                    </h4>
                    <p style="margin: 0; font-size: 11px; color: #666;">
                        {news['source']} | {news['timestamp'].strftime('%H:%M')}
                    </p>
                </div>
                <button style="
                    background: none;
                    border: none;
                    font-size: 18px;
                    cursor: pointer;
                    color: #999;
                " onclick="this.parentElement.parentElement.style.display='none'">×</button>
            </div>
            <div style="margin-top: 15px; text-align: right;">
                <a href="{news['url']}" target="_blank" style="
                    color: {COLORS['primary']};
                    text-decoration: none;
                    font-size: 12px;
                    font-weight: bold;
                ">Voir le détail →</a>
            </div>
        </div>
        
        <style>
        @keyframes slideIn {{
            from {{ transform: translateX(400px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Bouton pour fermer manuellement
        col1, col2, col3 = st.columns([3, 1, 1])
        with col3:
            if st.button("✖ Fermer l'alerte", key="close_popup"):
                st.session_state.news_popup_shown = True
                st.rerun()

# -----------------------------------------------------------------------------
# 4. AFFICHAGE DU HEADER MACRONEWS
# -----------------------------------------------------------------------------
def render_macronews_header():
    """Affiche le header de la page Macronews"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 10px;
        margin-bottom: 25px;
    ">
        <h2 style="margin: 0; font-size: 24px;">📰 Macronews</h2>
        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 14px;">
            Actualités financières marocaines et indicateurs macroéconomiques
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. FLUX D'ACTUALITÉS
# -----------------------------------------------------------------------------
def render_news_feed():
    """Affiche le flux d'actualités financières"""
    st.markdown("### 📰 Fil d'Actualités")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_impact = st.selectbox(
            "Impact :",
            options=['Tous', 'Haute', 'Moyenne', 'Faible'],
            index=0
        )
    
    with col2:
        filter_source = st.selectbox(
            "Source :",
            options=['Toutes', 'Ilboursa', 'Bourse de Casablanca', 'Leconomiste', 'Medias24', 'BAM'],
            index=0
        )
    
    with col3:
        sort_by = st.selectbox(
            "Trier par :",
            options=['Plus récent', 'Plus ancien', 'Impact'],
            index=0
        )
    
    # Génération et filtrage des news
    news_items = generate_news_feed()
    
    # Application des filtres
    if filter_impact != 'Tous':
        impact_map = {'Haute': 'high', 'Moyenne': 'medium', 'Faible': 'low'}
        news_items = [n for n in news_items if n['category'] == impact_map[filter_impact]]
    
    if filter_source != 'Toutes':
        news_items = [n for n in news_items if n['source'] == filter_source]
    
    # Tri
    if sort_by == 'Plus récent':
        news_items.sort(key=lambda x: x['timestamp'], reverse=True)
    elif sort_by == 'Plus ancien':
        news_items.sort(key=lambda x: x['timestamp'])
    elif sort_by == 'Impact':
        impact_order = {'high': 0, 'medium': 1, 'low': 2}
        news_items.sort(key=lambda x: impact_order[x['category']])
    
    # Affichage des news (cartes)
    for news in news_items[:10]:  # Limiter à 10 news
        is_read = news['read']
        
        # Couleur selon l'impact
        border_color = news['category_color']
        
        st.markdown(f"""
        <div style="
            background: white;
            border-left: 4px solid {border_color};
            border-radius: 8px;
            padding: 15px 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            opacity: {0.6 if is_read else 1};
        ">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <p style="margin: 0; font-size: 11px; color: #666;">
                        {news['category_label']} | {news['source']} | {news['timestamp'].strftime('%d/%m à %H:%M')}
                    </p>
                    <h4 style="margin: 8px 0 5px 0; font-size: 15px; color: #333;">
                        {'✅ ' if is_read else '🔵 '}{news['title']}
                    </h4>
                    <p style="margin: 0; font-size: 13px; color: #666; line-height: 1.5;">
                        {news['summary']}
                    </p>
                </div>
                <div style="margin-left: 20px;">
                    <a href="{news['url']}" target="_blank" style="
                        background: {COLORS['primary']};
                        color: white;
                        padding: 8px 15px;
                        border-radius: 5px;
                        text-decoration: none;
                        font-size: 12px;
                        font-weight: bold;
                    ">Lire →</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bouton pour marquer comme lu
        col1, col2 = st.columns([5, 1])
        with col2:
            if not is_read:
                if st.button("Marquer comme lu", key=f"read_{news['id']}"):
                    st.session_state.news_read.append(news['id'])
                    st.rerun()
        
        st.markdown("---")

# -----------------------------------------------------------------------------
# 6. MODULE INFLATION
# -----------------------------------------------------------------------------
def render_inflation_module():
    """Affiche le module d'inflation avec jauge et historique"""
    st.markdown("### 📊 Indice d'Inflation (IPC)")
    
    # Données
    inflation_data = generate_inflation_history(24)
    current_inflation = inflation_data['inflation'].iloc[-1]
    previous_inflation = inflation_data['inflation'].iloc[-2]
    change = current_inflation - previous_inflation
    
    # Statut
    status_code, status_text, status_color = get_inflation_status(current_inflation)
    
    # ---------------------------------------------------------------------
    # SECTION 1 : KPIs ET JAUGE
    # ---------------------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Inflation Actuelle",
            value=f"{current_inflation:.2f}%",
            delta=f"{change:+.2f}%"
        )
    
    with col2:
        st.metric(
            label="Moyenne 12 mois",
            value=f"{inflation_data['inflation'].tail(12).mean():.2f}%"
        )
    
    with col3:
        st.metric(
            label="Cible BAM",
            value=f"{st.session_state.inflation_target:.1f}%"
        )
    
    with col4:
        st.metric(
            label="Statut",
            value=status_text.split(' ')[-1]  # Juste "Dans la cible", etc.
        )
    
    # ---------------------------------------------------------------------
    # SECTION 2 : JAUGE SEMI-CIRCULAIRE
    # ---------------------------------------------------------------------
    st.markdown("#### 🎯 Position par rapport à la cible")
    
    import plotly.graph_objects as go
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_inflation,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Inflation vs Cible BAM (2-3%)", 'font': {'size': 16}},
        number={'font': {'size': 40}},
        gauge={
            'axis': {'range': [-2, 8], 'tickwidth': 1, 'tickcolor': "#333"},
            'bar': {'color': status_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [-2, 2], 'color': '#e8f5e9'},  # Vert clair (bas)
                {'range': [2, 3], 'color': '#c8e6c9'},  # Vert (cible)
                {'range': [3, 8], 'color': '#ffebee'}   # Rouge (haut)
            ],
            'threshold': {
                'line': {'color': COLORS['danger'], 'width': 4},
                'thickness': 0.75,
                'value': st.session_state.inflation_target + 0.5
            }
        }
    ))
    
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Interprétation
        st.markdown("#### 📋 Interprétation")
        
        if status_code == 'on_target':
            st.success("""
            **Situation stable**
            
            L'inflation est dans la fourchette cible de Bank Al-Maghrib (2-3%). 
            La politique monétaire peut rester accommodante.
            """)
        elif status_code == 'high':
            st.warning("""
            **Pression inflationniste**
            
            L'inflation dépasse la cible. BAM pourrait envisager 
            un resserrement de la politique monétaire.
            """)
        else:
            st.info("""
            **Risque déflationniste**
            
            L'inflation est sous la cible. Risque de faible 
            croissance de la demande intérieure.
            """)
        
        # Stats rapides
        st.markdown(f"""
        <div style="padding: 15px; background: #f8f9fa; border-radius: 8px; margin-top: 15px;">
            <p style="margin: 0; font-size: 12px; color: #666;">Écart à la cible</p>
            <p style="margin: 5px 0; font-size: 18px; font-weight: bold; color: {status_color};">
                {current_inflation - st.session_state.inflation_target:+.2f}%
            </p>
            
            <p style="margin: 15px 0 5px 0; font-size: 12px; color: #666;">Tendance (3 mois)</p>
            <p style="margin: 0; font-size: 14px; font-weight: bold;">
                {'📈 Haussière' if change > 0.2 else '📉 Baissière' if change < -0.2 else '➡️ Stable'}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------
    # SECTION 3 : HISTORIQUE
    # ---------------------------------------------------------------------
    st.markdown("#### 📈 Historique (24 mois)")
    
    fig_history = go.Figure()
    
    fig_history.add_trace(go.Scatter(
        x=inflation_data['date'],
        y=inflation_data['inflation'],
        mode='lines+markers',
        name='Inflation IPC',
        line=dict(color=COLORS['primary'], width=2),
        marker=dict(size=6)
    ))
    
    # Ligne cible
    fig_history.add_hline(
        y=st.session_state.inflation_target,
        line_dash="dash",
        line_color=COLORS['success'],
        annotation_text="Cible BAM",
        annotation_position="right"
    )
    
    # Zone cible (2-3%)
    fig_history.add_hrect(
        y0=2, y1=3,
        fillcolor="rgba(40, 167, 69, 0.1)",
        line_width=0,
        annotation_text="Zone cible (2-3%)",
        annotation_position="right"
    )
    
    fig_history.update_layout(
        height=350,
        xaxis_title='Date',
        yaxis_title='Inflation (%)',
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(x=0, y=1)
    )
    
    st.plotly_chart(fig_history, use_container_width=True)
    
    # Tableau des derniers mois
    st.markdown("#### 📋 Derniers Mois")
    
    display_data = inflation_data.tail(6).copy()
    display_data['date'] = display_data['date'].dt.strftime('%m/%Y')
    display_data = display_data.rename(columns={'date': 'Mois', 'inflation': 'Inflation (%)'})
    
    st.dataframe(
        display_data[['Mois', 'Inflation (%)']],
        use_container_width=True,
        hide_index=True
    )

# -----------------------------------------------------------------------------
# 7. FONCTION DE RENDU PRINCIPAL
# -----------------------------------------------------------------------------
def render():
    """Affiche la page Macronews"""
    
    # ---------------------------------------------------------------------
    # POPUP D'ALERTE (à appeler en premier)
    # ---------------------------------------------------------------------
    render_news_popup()
    
    # ---------------------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------------------
    render_macronews_header()
    
    # ---------------------------------------------------------------------
    # SECTION 1 : FLUX D'ACTUALITÉS
    # ---------------------------------------------------------------------
    render_news_feed()
    
    # ---------------------------------------------------------------------
    # SECTION 2 : MODULE INFLATION
    # ---------------------------------------------------------------------
    st.markdown("---")
    render_inflation_module()
    
    # ---------------------------------------------------------------------
    # FOOTER DE PAGE
    # ---------------------------------------------------------------------
    st.markdown("---")
    st.caption(f"📰 Sources : Ilboursa, Bourse de Casablanca, Leconomiste, Medias24, Bank Al-Maghrib | Dernière MAJ: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# -----------------------------------------------------------------------------
# 8. POINT D'ENTRÉE POUR TEST UNITAIRE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    render()
