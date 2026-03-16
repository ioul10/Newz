# =============================================================================
# NEWZ - Module BDC Statut (Bourse de Casa)
# Fichier : pages/bdc_statut.py
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
if 'bdc_selected_index' not in st.session_state:
    st.session_state.bdc_selected_index = 'MASI'
if 'bdc_show_details' not in st.session_state:
    st.session_state.bdc_show_details = False
if 'bdc_active_tab' not in st.session_state:
    st.session_state.bdc_active_tab = 'visualisation'

# -----------------------------------------------------------------------------
# 2. FONCTIONS DE GÉNÉRATION DE DONNÉES SIMULÉES
# -----------------------------------------------------------------------------
def generate_masi_history(days=90):
    """Génère un historique simulé du MASI"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    base_value = 12000
    returns = np.random.normal(0.0005, 0.015, days)
    values = base_value * np.cumprod(1 + returns)
    
    return pd.DataFrame({
        'date': dates,
        'value': values,
        'volume': np.random.randint(30000000, 60000000, days)
    })

def generate_msi20_history(days=90):
    """Génère un historique simulé du MSI20"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    base_value = 1500
    returns = np.random.normal(0.0008, 0.018, days)
    values = base_value * np.cumprod(1 + returns)
    
    return pd.DataFrame({
        'date': dates,
        'value': values,
        'volume': np.random.randint(25000000, 50000000, days)
    })

def generate_msi20_components():
    """Génère les 20 valeurs du MSI20 avec statistiques"""
    companies = [
        'Attijariwafa Bank', 'BCP', 'BMCE Bank', 'Crédit du Maroc', 'CIH Bank',
        'Maroc Telecom', 'Orange Maroc', 'Inwi', 'LafargeHolcim', 'Ciments du Maroc',
        'Sonasid', 'Managem', 'Cosumar', 'Lesieur', 'Centrale Danone',
        'Marocaine des Eaux', 'Lydec', 'Redal', 'Taqa Morocco', 'Nareva'
    ]
    
    data = []
    for company in companies:
        data.append({
            'Société': company,
            'Cours': round(random.uniform(50, 1500), 2),
            'Variation (%)': round(random.uniform(-5, 5), 2),
            'Volume': random.randint(10000, 500000),
            'Capitalisation (MDH)': round(random.uniform(500, 15000), 0),
            'Volatilité (30j)': round(random.uniform(10, 40), 2),
            'Bêta': round(random.uniform(0.5, 1.5), 2),
            'Secteur': random.choice(['Banque', 'Télécom', 'Immobilier', 'Industrie', 'Distribution'])
        })
    
    return pd.DataFrame(data)

def generate_correlation_matrix(df_components):
    """Génère une matrice de corrélation simulée"""
    n = len(df_components)
    np.random.seed(42)
    matrix = np.random.uniform(-0.5, 1.0, (n, n))
    matrix = (matrix + matrix.T) / 2  # Symétrique
    np.fill_diagonal(matrix, 1.0)
    
    return pd.DataFrame(matrix, index=df_components['Société'], columns=df_components['Société'])

# -----------------------------------------------------------------------------
# 3. FONCTION DE STATUT DU MARCHÉ
# -----------------------------------------------------------------------------
def get_market_status():
    """Détermine le statut actuel du marché boursier"""
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    
    # Week-end
    if weekday >= 5:
        return 'closed', '🔴 Fermé (Week-end)'
    
    # Heures d'ouverture (10h00 - 15h30)
    if 10 <= hour < 15:
        return 'open', '🟢 Ouvert'
    elif 9 <= hour < 10:
        return 'pre_open', '🟡 Pré-ouverture'
    elif 15 <= hour < 16:
        return 'post_close', '🟠 Clôture en cours'
    else:
        return 'closed', '🔴 Fermé'

# -----------------------------------------------------------------------------
# 4. AFFICHAGE DU HEADER DE STATUT
# -----------------------------------------------------------------------------
def render_market_status_header():
    """Affiche le header avec statut du marché"""
    status_code, status_text = get_market_status()
    now = datetime.now()
    
    # Calcul prochaine ouverture/fermeture
    if status_code == 'closed':
        next_open = now + timedelta(days=(4 - now.weekday()) % 7 + 1)
        next_open = next_open.replace(hour=10, minute=0, second=0)
        countdown = f"Prochaine ouverture: {next_open.strftime('%d/%m à %H:%M')}"
    else:
        countdown = f"Fermeture à 15:30"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 10px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <h2 style="margin: 0; font-size: 24px;">📊 BDC Statut</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 14px;">
                Bourse de Casablanca - Statut en temps réel
            </p>
        </div>
        <div style="text-align: right;">
            <p style="margin: 0; font-size: 28px; font-weight: bold;">{status_text}</p>
            <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 13px;">{countdown}</p>
            <p style="margin: 5px 0 0 0; opacity: 0.7; font-size: 12px;">
                {now.strftime('%d/%m/%Y - %H:%M:%S')}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. ONGLET 1 : VISUALISATION
# -----------------------------------------------------------------------------
def render_visualisation_tab():
    """Affiche l'onglet de visualisation des indices"""
    
    # ---------------------------------------------------------------------
    # SECTION 1: SÉLECTEUR D'INDICE (TOGGLE)
    # ---------------------------------------------------------------------
    st.markdown("### 📈 Sélection de l'Indice")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        selected_index = st.radio(
            "Choisir l'indice à afficher :",
            options=['MASI', 'MSI20'],
            horizontal=True,
            index=0 if st.session_state.bdc_selected_index == 'MASI' else 1,
            key='index_selector'
        )
        
        if selected_index != st.session_state.bdc_selected_index:
            st.session_state.bdc_selected_index = selected_index
            st.rerun()
    
    # ---------------------------------------------------------------------
    # SECTION 2: GRAPHIQUE PRINCIPAL
    # ---------------------------------------------------------------------
    st.markdown("### 📊 Évolution de l'Indice")
    
    # Génération des données
    if selected_index == 'MASI':
        data = generate_masi_history(90)
        current_value = data['value'].iloc[-1]
        previous_value = data['value'].iloc[-2]
        change_pct = ((current_value - previous_value) / previous_value) * 100
        y_min = data['value'].min() * 0.95
        y_max = data['value'].max() * 1.05
    else:
        data = generate_msi20_history(90)
        current_value = data['value'].iloc[-1]
        previous_value = data['value'].iloc[-2]
        change_pct = ((current_value - previous_value) / previous_value) * 100
        y_min = data['value'].min() * 0.95
        y_max = data['value'].max() * 1.05
    
    # Affichage des KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=f"{selected_index} Actuel",
            value=f"{current_value:,.2f}",
            delta=f"{change_pct:+.2f}%"
        )
    
    with col2:
        st.metric(
            label="Plus Haut (90j)",
            value=f"{data['value'].max():,.2f}"
        )
    
    with col3:
        st.metric(
            label="Plus Bas (90j)",
            value=f"{data['value'].min():,.2f}"
        )
    
    with col4:
        st.metric(
            label="Volume Moyen",
            value=f"{data['volume'].mean()/1e6:.1f}M"
        )
    
    # Graphique Plotly
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['value'],
        mode='lines',
        name=selected_index,
        line=dict(color=COLORS['primary'], width=2),
        fill='tozeroy',
        fillcolor=f'rgba(0, 86, 150, 0.1)'
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis_title='Date',
        yaxis_title=f'Valeur {selected_index}',
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(range=[y_min, y_max])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ---------------------------------------------------------------------
    # SECTION 3: TABLEAU DE DÉTAILS (MASQUÉ PAR DÉFAUT)
    # ---------------------------------------------------------------------
    st.markdown("### 📋 Données Détaillées")
    
    if not st.session_state.bdc_show_details:
        if st.button("▼ Afficher les données brutes"):
            st.session_state.bdc_show_details = True
            st.rerun()
    else:
        # Affichage du tableau
        display_data = data.copy()
        display_data['Variation (%)'] = display_data['value'].pct_change() * 100
        display_data = display_data.tail(20)  # 20 derniers jours
        
        st.dataframe(
            display_data[['date', 'value', 'volume', 'Variation (%)']],
            use_container_width=True,
            hide_index=True
        )
        
        # Bouton pour masquer
        if st.button("▲ Masquer les données"):
            st.session_state.bdc_show_details = False
            st.rerun()
        
        # Export CSV
        csv = display_data.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger en CSV",
            data=csv,
            file_name=f"{selected_index.lower()}_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# -----------------------------------------------------------------------------
# 6. ONGLET 2 : STATISTIQUES
# -----------------------------------------------------------------------------
def render_statistiques_tab():
    """Affiche l'onglet de statistiques avancées"""
    
    # ---------------------------------------------------------------------
    # SECTION 1: COMPOSANTES MSI20
    # ---------------------------------------------------------------------
    st.markdown("### 🏢 Composantes du MSI20")
    
    df_components = generate_msi20_components()
    
    # Affichage résumé
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Nombre de valeurs",
            value=len(df_components)
        )
    
    with col2:
        avg_volatility = df_components['Volatilité (30j)'].mean()
        st.metric(
            label="Volatilité Moyenne",
            value=f"{avg_volatility:.2f}%"
        )
    
    with col3:
        total_cap = df_components['Capitalisation (MDH)'].sum()
        st.metric(
            label="Capitalisation Totale",
            value=f"{total_cap:,.0f} MDH"
        )
    
    # ---------------------------------------------------------------------
    # SECTION 2: MATRICE DE CORRÉLATION
    # ---------------------------------------------------------------------
    st.markdown("### 🔗 Matrice de Corrélation (MSI20)")
    
    corr_matrix = generate_correlation_matrix(df_components)
    
    # Heatmap avec Plotly
    import plotly.express as px
    
    fig_corr = px.imshow(
        corr_matrix,
        color_continuous_scale='RdBu_r',
        zmin=-1,
        zmax=1,
        aspect='auto',
        height=500
    )
    
    fig_corr.update_layout(
        xaxis_title='Société',
        yaxis_title='Société',
        coloraxis_colorbar=dict(title='Corrélation')
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.caption("💡 Lecture : 1 = Corrélation parfaite positive, -1 = Corrélation parfaite négative, 0 = Aucune corrélation")
    
    # ---------------------------------------------------------------------
    # SECTION 3: CLASSEMENT PAR VOLATILITÉ
    # ---------------------------------------------------------------------
    st.markdown("### 📊 Classement par Volatilité")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔴 Les Plus Volatiles")
        top_volatile = df_components.nlargest(5, 'Volatilité (30j)')[['Société', 'Volatilité (30j)', 'Variation (%)']]
        st.dataframe(top_volatile, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 🟢 Les Moins Volatiles")
        low_volatile = df_components.nsmallest(5, 'Volatilité (30j)')[['Société', 'Volatilité (30j)', 'Variation (%)']]
        st.dataframe(low_volatile, use_container_width=True, hide_index=True)
    
    # ---------------------------------------------------------------------
    # SECTION 4: CONTRIBUTION AU MASI
    # ---------------------------------------------------------------------
    st.markdown("### 💰 Top Contributions au MASI")
    
    # Calcul de la contribution (Capitalisation x Performance)
    df_components['Contribution'] = df_components['Capitalisation (MDH)'] * df_components['Variation (%)']
    top_contributors = df_components.nlargest(5, 'Contribution')[['Société', 'Capitalisation (MDH)', 'Variation (%)', 'Contribution']]
    
    st.dataframe(top_contributors, use_container_width=True, hide_index=True)
    
    # ---------------------------------------------------------------------
    # SECTION 5: GRAPHIQUE SECTORIEL
    # ---------------------------------------------------------------------
    st.markdown("### 🏭 Performance par Secteur")
    
    sector_perf = df_components.groupby('Secteur')['Variation (%)'].mean().reset_index()
    
    import plotly.express as px
    fig_sector = px.bar(
        sector_perf,
        x='Secteur',
        y='Variation (%)',
        color='Variation (%)',
        color_continuous_scale='RdYlGn',
        height=350
    )
    
    fig_sector.update_layout(
        xaxis_title='Secteur',
        yaxis_title='Performance Moyenne (%)',
        showlegend=False
    )
    
    st.plotly_chart(fig_sector, use_container_width=True)

# -----------------------------------------------------------------------------
# 7. FONCTION DE RENDU PRINCIPAL
# -----------------------------------------------------------------------------
def render():
    """Affiche la page BDC Statut"""
    
    # ---------------------------------------------------------------------
    # HEADER DE STATUT DU MARCHÉ
    # ---------------------------------------------------------------------
    render_market_status_header()
    
    # ---------------------------------------------------------------------
    # NAVIGATION PAR ONGLETS (SOUS-ONGLETS)
    # ---------------------------------------------------------------------
    tab1, tab2 = st.tabs(["📈 Visualisation", "📊 Statistiques"])
    
    with tab1:
        render_visualisation_tab()
    
    with tab2:
        render_statistiques_tab()
    
    # ---------------------------------------------------------------------
    # FOOTER DE PAGE
    # ---------------------------------------------------------------------
    st.markdown("---")
    st.caption(f"📊 Données Bourse de Casablanca | Dernière MAJ: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Source: casablanca-bourse.com")

# -----------------------------------------------------------------------------
# 8. POINT D'ENTRÉE POUR TEST UNITAIRE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    render()
