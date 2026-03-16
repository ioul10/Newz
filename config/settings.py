# =============================================================================
# NEWZ - Configuration Globale
# Fichier : config/settings.py
# =============================================================================

import os
from pathlib import Path

# -----------------------------------------------------------------------------
# 1. CHEMINS ET DIRECTOIRES
# -----------------------------------------------------------------------------
# Racine du projet (parent du dossier config)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Dossiers principaux
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"
TEMPLATES_DIR = ROOT_DIR / "templates"
REPORTS_DIR = ROOT_DIR / "reports"

# Création automatique des dossiers s'ils n'existent pas
for directory in [ASSETS_DIR, DATA_DIR, TEMPLATES_DIR, REPORTS_DIR]:
    directory.mkdir(exist_ok=True)

# Chemins des assets graphiques
LOGO_CDG_PATH = ASSETS_DIR / "logo_cdg.png"
ADMIN_STAMP_PATH = ASSETS_DIR / "admin_stamp.png"
FAVICON_PATH = ASSETS_DIR / "favicon.ico"

# -----------------------------------------------------------------------------
# 2. MÉTADONNÉES DE L'APPLICATION
# -----------------------------------------------------------------------------
APP_TITLE = "Newz | Market Data Platform"
APP_VERSION = "1.0.0"
APP_AUTHOR = "CDG Capital - Market Data Team"
PAGE_LAYOUT = "wide"  # "centered" ou "wide"
SIDEBAR_STATE = "expanded"  # "expanded" ou "collapsed" par défaut

# -----------------------------------------------------------------------------
# 3. CHARTE GRAPHIQUE (CDG Capital)
# -----------------------------------------------------------------------------
COLORS = {
    "primary": "#005696",       # Bleu CDG
    "secondary": "#003d6b",     # Bleu foncé
    "accent": "#00a8e8",        # Bleu clair
    "success": "#28a745",       # Vert
    "warning": "#ffc107",       # Jaune
    "danger": "#dc3545",        # Rouge
    "background": "#f5f5f5",    # Gris très clair
    "text": "#333333",          # Gris foncé
    "white": "#ffffff"
}

# -----------------------------------------------------------------------------
# 4. SOURCES DE DONNÉES (URLs pour scraping)
# -----------------------------------------------------------------------------
# Note : Ces URLs sont des exemples. À adapter selon la structure réelle des sites.
SOURCES = {
    "bourse_casa": {
        "base_url": "https://www.casablanca-bourse.com",
        "masi_endpoint": "/fr/live-market/overview",  # Exemple
        "timeout": 10
    },
    "bam": {
        "base_url": "https://www.bkam.ma",
        "taux_endpoint": "/Taux-de-change",  # Exemple
        "timeout": 10
    },
    "news": {
        "ilboursa": "https://www.ilboursa.com",
        "leconomiste": "https://www.leconomiste.com"
    }
}

# -----------------------------------------------------------------------------
# 5. CONFIGURATION PDF
# -----------------------------------------------------------------------------
PDF_CONFIG = {
    "format": "A4",
    "orientation": "portrait",
    "margin_top": "2cm",
    "margin_bottom": "2cm",
    "margin_left": "2cm",
    "margin_right": "2cm",
    "font_family": "Arial, sans-serif",
    "footer_text": "Généré par Newz — Usage interne CDG Capital"
}

# -----------------------------------------------------------------------------
# 6. NAVIGATION (Labels et Icônes)
# -----------------------------------------------------------------------------
NAVIGATION = {
    "home": {"label": "Accueil", "icon": "🏠"},
    "data_ingestion": {"label": "Data Ingestion", "icon": "📥"},
    "bdc_statut": {"label": "BDC Statut", "icon": "📊"},
    "bam": {"label": "BAM", "icon": "🏦"},
    "macronews": {"label": "Macronews", "icon": "📰"},
    "export": {"label": "Export Rapport", "icon": "📤"},
    "settings": {"label": "Paramètres", "icon": "⚙️"}
}

# -----------------------------------------------------------------------------
# 7. TEST DE CONFIGURATION (Pour validation du fichier)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("✅ Configuration Newz chargée avec succès !")
    print(f"📂 Racine du projet : {ROOT_DIR}")
    print(f"🎨 Couleur primaire : {COLORS['primary']}")
    print(f"📄 Dossier rapports : {REPORTS_DIR}")
    print(f" Source Bourse : {SOURCES['bourse_casa']['base_url']}")
    
    # Vérification des dossiers
    for directory in [ASSETS_DIR, DATA_DIR, TEMPLATES_DIR, REPORTS_DIR]:
        if directory.exists():
            print(f"✅ Dossier existant : {directory.name}")
        else:
            print(f"❌ Dossier manquant : {directory.name}")
