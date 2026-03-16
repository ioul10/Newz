# =============================================================================
# NEWZ - Module de Graphiques pour Export
# Fichier : utils/charts.py
# =============================================================================

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_masi_chart():
    """Génère le graphique MASI"""
    dates = pd.date_range(end=datetime.now(), periods=90, freq='B')
    values = 12000 + np.cumsum(np.random.normal(0, 50, 90))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values,
        mode='lines',
        line=dict(color='#005696', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 86, 150, 0.1)'
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=40, r=20, t=30, b=20),
        xaxis_title='',
        yaxis_title='MASI',
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def generate_monia_chart():
    """Génère le graphique MONIA"""
    dates = pd.date_range(end=datetime.now(), periods=90, freq='B')
    values = 3.0 + np.cumsum(np.random.normal(0, 0.02, 90))
    values = np.clip(values, 2.5, 3.5)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values,
        mode='lines',
        line=dict(color='#00a8e8', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 168, 232, 0.1)'
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=40, r=20, t=30, b=20),
        xaxis_title='',
        yaxis_title='MONIA (%)',
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def generate_fx_chart(pair='EUR/MAD'):
    """Génère le graphique de change"""
    dates = pd.date_range(end=datetime.now(), periods=90, freq='B')
    base = 10.75 if 'EUR' in pair else 9.85
    values = base + np.cumsum(np.random.normal(0, 0.02, 90))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values,
        mode='lines',
        line=dict(color='#28a745', width=2),
        fill='tozeroy',
        fillcolor='rgba(40, 167, 69, 0.1)'
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=40, r=20, t=30, b=20),
        xaxis_title='',
        yaxis_title=pair,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def generate_inflation_gauge(value=-0.8, target=2.5):
    """Génère la jauge d'inflation"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Inflation (%)", 'font': {'size': 14}},
        number={'font': {'size': 24}},
        gauge={
            'axis': {'range': [-2, 8], 'tickwidth': 1},
            'bar': {'color': '#dc3545' if abs(value - target) > 1 else '#28a745'},
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
                'value': target + 0.5
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def generate_bdt_chart():
    """Génère le graphique BDT (courbe des taux)"""
    maturities = ['1Y', '2Y', '3Y', '5Y', '7Y', '10Y']
    today = [2.43, 2.55, 2.68, 2.87, 3.05, 3.25]
    last_week = [t + np.random.uniform(-0.05, 0.05) for t in today]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=maturities, y=today,
        name='Aujourd\'hui',
        marker_color='#005696'
    ))
    fig.add_trace(go.Bar(
        x=maturities, y=last_week,
        name='Semaine dernière',
        marker_color='#999999'
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=40, r=20, t=30, b=20),
        xaxis_title='Maturité',
        yaxis_title='Taux (%)',
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True
    )
    
    return fig

def generate_reserves_chart():
    """Génère le graphique des réserves obligatoires"""
    dates = pd.date_range(end=datetime.now(), periods=90, freq='B')
    values = 11000 + np.cumsum(np.random.normal(0, 100, 90))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values,
        mode='lines',
        line=dict(color='#ffc107', width=2),
        fill='tozeroy',
        fillcolor='rgba(255, 193, 7, 0.1)'
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=40, r=20, t=30, b=20),
        xaxis_title='',
        yaxis_title='Réserves (MDH)',
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def convert_fig_to_html(fig):
    """Convertit une figure Plotly en HTML embeddable"""
    import plotly.io as pio
    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
