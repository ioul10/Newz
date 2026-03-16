# =============================================================================
# NEWZ - Générateur PDF Simplifié
# Fichier : utils/pdf_generator.py
# =============================================================================

import streamlit as st
from datetime import datetime
from pathlib import Path
import base64

def generate_simple_pdf(data):
    """
    Génère un PDF simple en utilisant l'export HTML de Streamlit
    """
    
    # Création du contenu HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Newz Report - {data['report_date']}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                color: #333;
            }}
            .header {{
                background: linear-gradient(135deg, #005696 0%, #003d6b 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
            }}
            .kpi-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }}
            .kpi-card {{
                background: #f8f9fa;
                border-left: 5px solid #005696;
                padding: 20px;
                border-radius: 8px;
            }}
            .kpi-card h3 {{
                margin: 0 0 10px 0;
                color: #005696;
                font-size: 14px;
            }}
            .kpi-value {{
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 20px;
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }}
            .section h2 {{
                color: #005696;
                border-bottom: 2px solid #005696;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background: #005696;
                color: white;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background: #f8f9fa;
            }}
            .footer {{
                margin-top: 50px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }}
            .stamp {{
                margin-top: 30px;
                text-align: right;
            }}
            .stamp-box {{
                display: inline-block;
                border: 3px solid #dc3545;
                color: #dc3545;
                padding: 15px 30px;
                font-weight: bold;
                font-size: 18px;
                transform: rotate(-5deg);
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏦 CDG CAPITAL</h1>
            <p><b>Newz — Market Data Weekly</b></p>
            <p>{data['report_week']}</p>
            <p style="font-size: 12px; margin-top: 10px;">
                Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
            </p>
        </div>
        
        <div class="kpi-grid">
            <div class="kpi-card">
                <h3>📊 MASI</h3>
                <div class="kpi-value">{data['masi']['value']:,.0f}</div>
                <div style="color: {'green' if data['masi']['change'] > 0 else 'red'}; font-size: 14px;">
                    {data['masi']['change']:+.2f}%
                </div>
            </div>
            <div class="kpi-card">
                <h3>💶 EUR/MAD</h3>
                <div class="kpi-value">{data['eur_mad']['value']:.4f}</div>
                <div style="color: {'green' if data['eur_mad']['change'] > 0 else 'red'}; font-size: 14px;">
                    {data['eur_mad']['change']:+.2f}%
                </div>
            </div>
            <div class="kpi-card">
                <h3>💹 Inflation</h3>
                <div class="kpi-value">{data['inflation']['value']:.2f}%</div>
                <div style="font-size: 12px; color: #666;">
                    Cible: {data['inflation']['target']}%
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Indices Boursiers</h2>
            <table>
                <tr>
                    <th>Indice</th>
                    <th>Valeur</th>
                    <th>Variation</th>
                    <th>Volume</th>
                </tr>
                <tr>
                    <td><b>MASI</b></td>
                    <td>{data['masi']['value']:,.0f}</td>
                    <td style="color: {'green' if data['masi']['change'] > 0 else 'red'};">
                        {data['masi']['change']:+.2f}%
                    </td>
                    <td>{data['masi']['volume']:,}</td>
                </tr>
                <tr>
                    <td><b>MSI20</b></td>
                    <td>{data['msi20']['value']:,.0f}</td>
                    <td style="color: {'green' if data['msi20']['change'] > 0 else 'red'};">
                        {data['msi20']['change']:+.2f}%
                    </td>
                    <td>{data['msi20']['volume']:,}</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>🏦 Taux & Devises</h2>
            <table>
                <tr>
                    <th>Indicateur</th>
                    <th>Valeur</th>
                    <th>Variation</th>
                </tr>
                <tr>
                    <td>MONIA</td>
                    <td>{data['monia']['value']:.2f}%</td>
                    <td>{data['monia']['change']:+.2f}%</td>
                </tr>
                <tr>
                    <td>USD/MAD</td>
                    <td>{data['usd_mad']['value']:.4f}</td>
                    <td>{data['usd_mad']['change']:+.2f}%</td>
                </tr>
                <tr>
                    <td>EUR/MAD</td>
                    <td>{data['eur_mad']['value']:.4f}</td>
                    <td>{data['eur_mad']['change']:+.2f}%</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📊 Top Movers</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h3 style="color: green;">🟢 Top Gainers</h3>
                    <ul>
                        {''.join([f"<li>{g['name']}: {g['change']:+.1f}%</li>" for g in data['top_gainers']])}
                    </ul>
                </div>
                <div>
                    <h3 style="color: red;">🔴 Top Losers</h3>
                    <ul>
                        {''.join([f"<li>{l['name']}: {l['change']:+.1f}%</li>" for l in data['top_losers']])}
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><b>CDG Capital — Market Data Team</b></p>
            <p>Newz v1.0 | Usage interne uniquement | Confidentiel</p>
            <p>Sources : Bourse de Casablanca, Bank Al-Maghrib</p>
            <div class="stamp">
                <div class="stamp-box">ADMIN<br/>CONFIDENTIEL</div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def download_html_as_pdf(html_content, filename):
    """
    Permet de télécharger le HTML (l'utilisateur peut l'imprimer en PDF)
    """
    b64 = base64.b64encode(html_content.encode()).decode()
    return f"""
    <a href="data:text/html;base64,{b64}" download="{filename}">
        <button style="
            background: #005696;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin: 20px 0;
        ">
            📥 Télécharger le Rapport (HTML)
        </button>
    </a>
    <p style="color: #666; font-size: 12px;">
        💡 Astuce : Ouvrez le fichier HTML et utilisez Ctrl+P pour l'imprimer en PDF
    </p>
    """
