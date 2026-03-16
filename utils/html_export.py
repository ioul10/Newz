# =============================================================================
# NEWZ - Export HTML (Alternative au PDF)
# Fichier : utils/html_export.py
# =============================================================================

from datetime import datetime
import base64

def generate_report_html(data):
    """Génère un rapport HTML professionnel"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Newz Report - {data['report_date']}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
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
            .header h1 {{ margin: 0; font-size: 32px; }}
            .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
            
            .kpi-container {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }}
            .kpi-box {{
                background: #f8f9fa;
                border-left: 5px solid #005696;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }}
            .kpi-box h3 {{
                margin: 0 0 10px 0;
                color: #005696;
                font-size: 14px;
                text-transform: uppercase;
            }}
            .kpi-box .value {{
                font-size: 28px;
                font-weight: bold;
                color: #333;
            }}
            .kpi-box .change {{
                font-size: 14px;
                margin-top: 5px;
            }}
            .positive {{ color: #28a745; }}
            .negative {{ color: #dc3545; }}
            
            .section {{
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 25px;
                margin-bottom: 25px;
            }}
            .section h2 {{
                color: #005696;
                border-bottom: 3px solid #005696;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background: #005696;
                color: white;
                font-weight: bold;
            }}
            tr:nth-child(even) {{ background: #f8f9fa; }}
            tr:hover {{ background: #e3f2fd; }}
            
            .footer {{
                margin-top: 50px;
                padding: 25px;
                background: #f8f9fa;
                border-radius: 8px;
                text-align: center;
                font-size: 12px;
                color: #666;
                border-top: 4px solid #005696;
            }}
            .stamp {{
                margin-top: 30px;
                display: inline-block;
                border: 4px solid #dc3545;
                color: #dc3545;
                padding: 15px 40px;
                font-weight: bold;
                font-size: 20px;
                transform: rotate(-3deg);
                opacity: 0.8;
            }}
            
            @media print {{
                body {{ margin: 0; }}
                .no-print {{ display: none; }}
            }}
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
            <p style="font-size: 12px; margin-top: 10px;">
                Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
            </p>
        </div>
        
        <div class="kpi-container">
            <div class="kpi-box">
                <h3>📊 MASI</h3>
                <div class="value">{data['masi']['value']:,.0f}</div>
                <div class="change {'positive' if data['masi']['change'] > 0 else 'negative'}">
                    {data['masi']['change']:+.2f}%
                </div>
            </div>
            <div class="kpi-box">
                <h3>💶 EUR/MAD</h3>
                <div class="value">{data['eur_mad']['value']:.4f}</div>
                <div class="change {'positive' if data['eur_mad']['change'] > 0 else 'negative'}">
                    {data['eur_mad']['change']:+.2f}%
                </div>
            </div>
            <div class="kpi-box">
                <h3>💹 Inflation</h3>
                <div class="value">{data['inflation']['value']:.2f}%</div>
                <div style="font-size: 12px; color: #666; margin-top: 5px;">
                    Cible: {data['inflation']['target']}%
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Indices Boursiers</h2>
            <table>
                <thead>
                    <tr>
                        <th>Indice</th>
                        <th>Valeur</th>
                        <th>Variation</th>
                        <th>Volume</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>MASI</b></td>
                        <td>{data['masi']['value']:,.0f}</td>
                        <td class="{'positive' if data['masi']['change'] > 0 else 'negative'}">
                            {data['masi']['change']:+.2f}%
                        </td>
                        <td>{data['masi']['volume']:,}</td>
                    </tr>
                    <tr>
                        <td><b>MSI20</b></td>
                        <td>{data['msi20']['value']:,.0f}</td>
                        <td class="{'positive' if data['msi20']['change'] > 0 else 'negative'}">
                            {data['msi20']['change']:+.2f}%
                        </td>
                        <td>{data['msi20']['volume']:,}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>🏦 Taux & Devises</h2>
            <table>
                <thead>
                    <tr>
                        <th>Indicateur</th>
                        <th>Valeur</th>
                        <th>Variation</th>
                    </tr>
                </thead>
                <tbody>
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
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>📊 Top Movers de la Semaine</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div>
                    <h3 style="color: #28a745; border-bottom: 2px solid #28a745; padding-bottom: 8px;">
                        🟢 Top Gainers
                    </h3>
                    <ul style="list-style: none; padding: 0;">
                        {''.join([f'<li style="padding: 8px 0; border-bottom: 1px solid #eee;">{g["name"]}: <b style="color: #28a745;">{g["change"]:+.1f}%</b></li>' for g in data['top_gainers']])}
                    </ul>
                </div>
                <div>
                    <h3 style="color: #dc3545; border-bottom: 2px solid #dc3545; padding-bottom: 8px;">
                        🔴 Top Losers
                    </h3>
                    <ul style="list-style: none; padding: 0;">
                        {''.join([f'<li style="padding: 8px 0; border-bottom: 1px solid #eee;">{l["name"]}: <b style="color: #dc3545;">{l["change"]:+.1f}%</b></li>' for l in data['top_losers']])}
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><b style="color: #005696; font-size: 14px;">CDG Capital — Market Data Team</b></p>
            <p>Newz v1.0 | Usage interne uniquement | Document confidentiel</p>
            <p style="margin-top: 15px; font-size: 11px;">
                Sources : Bourse de Casablanca | Bank Al-Maghrib | HCP
            </p>
            <div class="stamp">
                ADMIN<br/>CONFIDENTIEL
            </div>
        </div>
        
        <div class="no-print" style="margin-top: 30px; text-align: center; padding: 20px; background: #e8f5e9; border-radius: 8px;">
            <p style="margin: 0 0 15px 0; font-size: 16px; font-weight: bold; color: #2e7d32;">
                📄 Pour sauvegarder en PDF :
            </p>
            <p style="margin: 0; color: #666;">
                Appuyez sur <kbd style="background: white; padding: 5px 10px; border-radius: 4px; border: 1px solid #ccc;">Ctrl+P</kbd> 
                puis sélectionnez "Enregistrer au format PDF"
            </p>
        </div>
    </body>
    </html>
    """
    
    return html

def get_download_link(html_content, filename="newz_report.html"):
    """Génère un lien de téléchargement pour le fichier HTML"""
    b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    return f"""
    <a href="data:text/html;base64,{b64}" download="{filename}">
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
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 16px rgba(0, 86, 150, 0.4)'" 
          onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0, 86, 150, 0.3)'">
            📥 Télécharger le Rapport (HTML)
        </button>
    </a>
    <p style="color: #666; font-size: 13px; margin-top: 10px;">
        💡 <b>Astuce :</b> Ouvrez le fichier HTML téléchargé et appuyez sur Ctrl+P pour l'imprimer en PDF
    </p>
    """
