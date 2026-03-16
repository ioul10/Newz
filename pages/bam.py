# =============================================================================
# NEWZ - Module BAM (Bank Al-Maghrib)
# Fichier : pages/bam.py
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Import des configurations
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import COLORS, DATA_DIR

# -----------------------------------------------------------------------------
# 1. INITIALISATION DE L'ÉTAT DE SESSION
# -----------------------------------------------------------------------------
if 'bam_selected_charts' not in st.session_state:
    st.session_state.bam_selected_charts = ['mad_usd', 'mad_eur']
if 'bam_chart_layout' not in st.session_state:
    st.session_state.bam_chart_layout = 'side_by_side'  # 'side_by_side', 'overlay', 'separate'

# -----------------------------------------------------------------------------
# 2. FONCTIONS DE GÉNÉRATION DE DONNÉES SIMULÉES
# -----------------------------------------------------------------------------
def generate_monia_history(days=90):
    """Génère un historique simulé du taux MONIA"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    base_rate = 3.00
    # Simulation de variations réalistes de taux
    changes = np.random.normal(0, 0.02, days)
    rates = base_rate + np.cumsum(changes)
    rates = np.clip(rates, 2.0, 4.5)  # Plafonnement réaliste
    
    return pd.DataFrame({
        'date': dates,
        'rate': rates,
        'ma7': pd.Series(rates).rolling(7).mean(),
        'ma30': pd.Series(rates).rolling(30).mean()
    })

def generate_bdt_curve():
    """Génère la courbe des taux BDT (Bon du Trésor)"""
    maturities = ['1 an', '2 ans', '3 ans', '5 ans', '7 ans', '10 ans', '15 ans', '20 ans']
    
    # Courbe normale (pentue)
    today_curve = [2.43, 2.55, 2.68, 2.87, 3.05, 3.25, 3.40, 3.55]
    
    # Courbe semaine dernière (légèrement différente)
    last_week_curve = [r + np.random.uniform(-0.05, 0.05) for r in today_curve]
    
    return pd.DataFrame({
        'Maturité': maturities,
        'Aujourd\'hui': today_curve,
        'Semaine dernière': last_week_curve
    })

def generate_fx_history(days=90, pair='USD/MAD'):
    """Génère un historique de taux de change"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    
    if 'USD' in pair:
        base_rate = 9.85
        volatility = 0.02
    else:  # EUR
        base_rate = 10.75
        volatility = 0.025
    
    changes = np.random.normal(0, volatility, days)
    rates = base_rate + np.cumsum(changes)
    
    return pd.DataFrame({
        'date': dates,
        'rate': rates
    })

def generate_mad_index(days=90):
    """Génère l'indice de change effectif du MAD"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    base_index = 100
    changes = np.random.normal(0, 0.005, days)
    index_values = base_index * np.cumprod(1 + changes)
    
    return pd.DataFrame({
        'date': dates,
        'index': index_values
    })

# -----------------------------------------------------------------------------
# 3. AFFICHAGE DU HEADER BAM
# -----------------------------------------------------------------------------
def render_bam_header():
    """Affiche le header de la page BAM"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 10px;
        margin-bottom: 25px;
    ">
        <h2 style="margin: 0; font-size: 24px;">🏦 Bank Al-Maghrib</h2>
        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 14px;">
            Taux monétaires, courbe des taux et devises
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. SÉLECTEUR DE GRAPHIQUES
# -----------------------------------------------------------------------------
def render_chart_selector():
    """Affiche le sélecteur de graphiques à afficher"""
    st.markdown("### 📊 Sélection des Graphiques")
    
    chart_options = {
        'mad_index': '📈 Indice de change effectif MAD',
        'eur_usd': '🌍 EUR/USD (Référence internationale)',
        'mad_usd': '💵 MAD/USD',
        'mad_eur': '💶 MAD/EUR'
    }
    
    selected = st.multiselect(
        "Choisissez les graphiques à afficher :",
        options=list(chart_options.keys()),
        default=st.session_state.bam_selected_charts,
        format_func=lambda x: chart_options[x]
    )
    
    st.session_state.bam_selected_charts = selected
    
    # Option de disposition
    st.markdown("**Disposition des graphiques :**")
    layout = st.radio(
        "Mode d'affichage :",
        options=['side_by_side', 'overlay', 'separate'],
        format_func=lambda x: {
            'side_by_side': '📊 Côte à côte',
            'overlay': '🔀 Superposé',
            'separate': '📄 Séparé'
        }.get(x, x),
        horizontal=True,
        index=0 if st.session_state.bam_chart_layout == 'side_by_side' else 
               1 if st.session_state.bam_chart_layout == 'overlay' else 2
    )
    
    st.session_state.bam_chart_layout = layout
    
    return selected

# -----------------------------------------------------------------------------
# 5. AFFICHAGE DES GRAPHIQUES DE DEVISES
# -----------------------------------------------------------------------------
def render_fx_charts(selected_charts, layout):
    """Affiche les graphiques de devises sélectionnés"""
    
    if not selected_charts:
        st.info("ℹ️ Sélectionnez au moins un graphique à afficher.")
        return
    
    import plotly.graph_objects as go
    
    # ---------------------------------------------------------------------
    # GRAPHIQUE 1 : INDICE MAD
    # ---------------------------------------------------------------------
    if 'mad_index' in selected_charts:
        st.markdown("### Indice de Change Effectif du MAD")
        
        data = generate_mad_index(90)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['index'],
            mode='lines',
            name='Indice MAD',
            line=dict(color=COLORS['primary'], width=2)
        ))
        
        fig.update_layout(
            height=350,
            xaxis_title='Date',
            yaxis_title='Indice (Base 100)',
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ---------------------------------------------------------------------
    # GRAPHIQUE 2 : EUR/USD
    # ---------------------------------------------------------------------
    if 'eur_usd' in selected_charts:
        st.markdown("### EUR/USD (Référence Internationale)")
        
        data = generate_fx_history(90, 'EUR/USD')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['rate'],
            mode='lines',
            name='EUR/USD',
            line=dict(color='#0066cc', width=2)
        ))
        
        fig.update_layout(
            height=350,
            xaxis_title='Date',
            yaxis_title='EUR/USD',
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ---------------------------------------------------------------------
    # GRAPHIQUES 3 & 4 : MAD/USD et MAD/EUR
    # ---------------------------------------------------------------------
    mad_pairs = [p for p in selected_charts if p in ['mad_usd', 'mad_eur']]
    
    if mad_pairs:
        if layout == 'overlay' and len(mad_pairs) == 2:
            # Superposition des deux paires
            st.markdown("### MAD/USD et MAD/EUR (Superposé)")
            
            fig = go.Figure()
            
            data_usd = generate_fx_history(90, 'USD/MAD')
            data_eur = generate_fx_history(90, 'EUR/MAD')
            
            fig.add_trace(go.Scatter(
                x=data_usd['date'],
                y=data_usd['rate'],
                mode='lines',
                name='MAD/USD',
                line=dict(color=COLORS['primary'], width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=data_eur['date'],
                y=data_eur['rate'],
                mode='lines',
                name='MAD/EUR',
                line=dict(color='#00a8e8', width=2)
            ))
            
            fig.update_layout(
                height=400,
                xaxis_title='Date',
                yaxis_title='Taux de Change',
                hovermode='x unified',
                plot_bgcolor='white',
                paper_bgcolor='white',
                legend=dict(x=0, y=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif layout == 'side_by_side':
            # Côte à côte
            cols = st.columns(len(mad_pairs))
            
            for idx, pair in enumerate(mad_pairs):
                with cols[idx]:
                    if pair == 'mad_usd':
                        st.markdown("#### MAD/USD")
                        data = generate_fx_history(90, 'USD/MAD')
                        color = COLORS['primary']
                        current = data['rate'].iloc[-1]
                        prev = data['rate'].iloc[-2]
                        change = ((current - prev) / prev) * 100
                        
                        st.metric(
                            label="Taux Actuel",
                            value=f"{current:.4f}",
                            delta=f"{change:+.2f}%"
                        )
                    else:
                        st.markdown("#### MAD/EUR")
                        data = generate_fx_history(90, 'EUR/MAD')
                        color = '#00a8e8'
                        current = data['rate'].iloc[-1]
                        prev = data['rate'].iloc[-2]
                        change = ((current - prev) / prev) * 100
                        
                        st.metric(
                            label="Taux Actuel",
                            value=f"{current:.4f}",
                            delta=f"{change:+.2f}%"
                        )
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=data['date'],
                        y=data['rate'],
                        mode='lines',
                        name=pair.upper(),
                        line=dict(color=color, width=2)
                    ))
                    
                    fig.update_layout(
                        height=300,
                        xaxis_title='Date',
                        yaxis_title='Taux',
                        hovermode='x unified',
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        margin=dict(l=40, r=20, t=40, b=40)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        else:
            # Séparé (un par un)
            for pair in mad_pairs:
                if pair == 'mad_usd':
                    st.markdown("### MAD/USD")
                    data = generate_fx_history(90, 'USD/MAD')
                    color = COLORS['primary']
                else:
                    st.markdown("### MAD/EUR")
                    data = generate_fx_history(90, 'EUR/MAD')
                    color = '#00a8e8'
                
                current = data['rate'].iloc[-1]
                prev = data['rate'].iloc[-2]
                change = ((current - prev) / prev) * 100
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=data['date'],
                        y=data['rate'],
                        mode='lines',
                        name=pair.upper(),
                        line=dict(color=color, width=2)
                    ))
                    
                    fig.update_layout(
                        height=350,
                        xaxis_title='Date',
                        yaxis_title='Taux',
                        hovermode='x unified',
                        plot_bgcolor='white',
                        paper_bgcolor='white'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.metric(
                        label="Taux Actuel",
                        value=f"{current:.4f}",
                        delta=f"{change:+.2f}%"
                    )
                    
                    st.markdown(f"""
                    <div style="padding: 15px; background: #f8f9fa; border-radius: 8px;">
                        <p style="margin: 0; font-size: 12px; color: #666;">Plus Haut (90j)</p>
                        <p style="margin: 5px 0; font-size: 16px; font-weight: bold;">{data['rate'].max():.4f}</p>
                        <p style="margin: 0; font-size: 12px; color: #666;">Plus Bas (90j)</p>
                        <p style="margin: 5px 0; font-size: 16px; font-weight: bold;">{data['rate'].min():.4f}</p>
                        <p style="margin: 0; font-size: 12px; color: #666;">Moyenne (90j)</p>
                        <p style="margin: 5px 0; font-size: 16px; font-weight: bold;">{data['rate'].mean():.4f}</p>
                    </div>
                    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. AFFICHAGE DU MONIA
# ---------------------------------------------------------------------
def render_monia_section():
    """Affiche la section MONIA"""
    st.markdown("---")
    st.markdown("### 📈 Indice MONIA")
    
    data = generate_monia_history(90)
    current_rate = data['rate'].iloc[-1]
    previous_rate = data['rate'].iloc[-2]
    change = ((current_rate - previous_rate) / previous_rate) * 100
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="MONIA Actuel",
            value=f"{current_rate:.2f}%",
            delta=f"{change:+.2f}%"
        )
    
    with col2:
        st.metric(
            label="Moyenne 7j",
            value=f"{data['ma7'].iloc[-1]:.2f}%"
        )
    
    with col3:
        st.metric(
            label="Moyenne 30j",
            value=f"{data['ma30'].iloc[-1]:.2f}%"
        )
    
    with col4:
        st.metric(
            label="Volatilité (30j)",
            value=f"{data['rate'].std():.2f}%"
        )
    
    # Graphique
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['rate'],
        mode='lines',
        name='MONIA',
        line=dict(color=COLORS['primary'], width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['ma7'],
        mode='lines',
        name='MM 7j',
        line=dict(color=COLORS['accent'], width=1, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['ma30'],
        mode='lines',
        name='MM 30j',
        line=dict(color='#ffc107', width=1, dash='dot')
    ))
    
    # Zones de tension
    fig.add_hrect(
        y0=3.5, y1=4.5,
        fillcolor="rgba(220, 53, 69, 0.1)",
        line_width=0,
        annotation_text="Zone de tension",
        annotation_position="top right"
    )
    
    fig.update_layout(
        height=400,
        xaxis_title='Date',
        yaxis_title='Taux (%)',
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(x=0, y=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("💡 MONIA = Moroccan OverNight Index Average. Taux moyen pondéré des transactions interbancaires au jour le jour.")

# -----------------------------------------------------------------------------
# 7. AFFICHAGE DE LA COURBE BDT
# -----------------------------------------------------------------------------
def render_bdt_section():
    """Affiche la section Courbe des Taux BDT"""
    st.markdown("---")
    st.markdown("### 📊 Courbe des Taux BDT (Bon du Trésor)")
    
    data = generate_bdt_curve()
    
    # Calcul de la pente
    spread_10y2y = data['Aujourd\'hui'].iloc[5] - data['Aujourd\'hui'].iloc[1]
    spread_status = "🟢 Courbe pentue (croissance attendue)" if spread_10y2y > 0.5 else "🟡 Courbe plate" if spread_10y2y > 0 else "🔴 Courbe inversée (risque récession)"
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Graphique
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['Maturité'],
            y=data['Aujourd\'hui'],
            mode='lines+markers',
            name='Aujourd\'hui',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=data['Maturité'],
            y=data['Semaine dernière'],
            mode='lines+markers',
            name='Semaine dernière',
            line=dict(color='#999999', width=2, dash='dash'),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            height=400,
            xaxis_title='Maturité',
            yaxis_title='Taux (%)',
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(x=0, y=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Stats rapides
        st.markdown("#### 📋 Indicateurs")
        
        st.markdown(f"""
        <div style="padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <p style="margin: 0; font-size: 12px; color: #666;">Pente 10Y-2Y</p>
            <p style="margin: 5px 0; font-size: 18px; font-weight: bold; color: {COLORS['primary']};">{spread_10y2y:.2f}%</p>
            
            <p style="margin: 15px 0 5px 0; font-size: 12px; color: #666;">Taux 1 an</p>
            <p style="margin: 0; font-size: 16px; font-weight: bold;">{data['Aujourd\'hui'].iloc[0]:.2f}%</p>
            
            <p style="margin: 15px 0 5px 0; font-size: 12px; color: #666;">Taux 10 ans</p>
            <p style="margin: 0; font-size: 16px; font-weight: bold;">{data['Aujourd\'hui'].iloc[5]:.2f}%</p>
            
            <p style="margin: 15px 0 5px 0; font-size: 12px; color: #666;">Statut</p>
            <p style="margin: 0; font-size: 13px;">{spread_status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tableau des taux
    st.markdown("#### 📋 Tableau des Taux")
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

# -----------------------------------------------------------------------------
# 8. FONCTION DE RENDU PRINCIPAL
# -----------------------------------------------------------------------------
def render():
    """Affiche la page BAM"""
    
    # ---------------------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------------------
    render_bam_header()
    
    # ---------------------------------------------------------------------
    # SÉLECTEUR DE GRAPHIQUES
    # ---------------------------------------------------------------------
    selected_charts = render_chart_selector()
    
    # ---------------------------------------------------------------------
    # GRAPHIQUES DE DEVISES
    # ---------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 💱 Devises")
    render_fx_charts(selected_charts, st.session_state.bam_chart_layout)
    
    # ---------------------------------------------------------------------
    # SECTION MONIA
    # ---------------------------------------------------------------------
    render_monia_section()
    
    # ---------------------------------------------------------------------
    # SECTION BDT
    # ---------------------------------------------------------------------
    render_bdt_section()
    
    # ---------------------------------------------------------------------
    # FOOTER DE PAGE
    # ---------------------------------------------------------------------
    st.markdown("---")
    st.caption(f"🏦 Données Bank Al-Maghrib | Dernière MAJ: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Source: bkam.ma")

# -----------------------------------------------------------------------------
# 9. POINT D'ENTRÉE POUR TEST UNITAIRE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    render()
