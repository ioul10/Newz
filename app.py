# =============================================================================
# NEWZ - Point d'Entrée Principal
# Fichier : app.py
# =============================================================================

import streamlit as st
from pathlib import Path
import sys

# -----------------------------------------------------------------------------
# 1. CONFIGURATION DE LA PAGE (DOIT ÊTRE LA PREMIÈRE COMMANDE STREAMLIT)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Newz | Market Data Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:support@cdgcapital.ma',
        'Report a bug': 'https://github.com/votre-username/newz/issues',
        'About': "# Newz v1.0\nDéveloppé pour CDG Capital"
    }
)

# -----------------------------------------------------------------------------
# 2. IMPORTS ET CONFIGURATION
# -----------------------------------------------------------------------------
# Ajout du chemin racine pour les imports
sys.path.append(str(Path(__file__).resolve().parent))

from config.settings import (
    APP_TITLE, APP_VERSION, COLORS, NAVIGATION,
    LOGO_CDG_PATH, ADMIN_STAMP_PATH
)

# -----------------------------------------------------------------------------
# 3. INITIALISATION DE L'ÉTAT DE SESSION
# -----------------------------------------------------------------------------
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# -----------------------------------------------------------------------------
# 4. STYLE PERSONNALISÉ (CSS)
# -----------------------------------------------------------------------------
def load_custom_css():
    """Charge le CSS personnalisé pour éviter le look Streamlit classique"""
    st.markdown(f"""
    <style>
        /* Cache le menu hamburger par défaut */
        #MainMenu {{visibility: hidden;}}
        
        /* Header personnalisé */
        .header {{
            background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 0;
            margin: -10px -10px 20px -10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        /* Sidebar styling */
        .stSidebar {{
            background-color: #f8f9fa;
            border-right: 1px solid #e0e0e0;
        }}
        
        /* Navigation items */
        .nav-item {{
            padding: 12px 15px;
            margin: 5px 10px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .nav-item:hover {{
            background-color: #e3f2fd;
            color: {COLORS['primary']};
        }}
        
        .nav-item.active {{
            background-color: {COLORS['primary']};
            color: white;
            border-left: 4px solid {COLORS['secondary']};
        }}
        
        /* Bouton toggle sidebar */
        .sidebar-toggle {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            z-index: 1000;
            background: {COLORS['primary']};
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }}
        
        /* Footer */
        .footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #f5f5f5;
            padding: 10px 25px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. HEADER PERSONNALISÉ
# -----------------------------------------------------------------------------
def render_header():
    """Affiche le header avec logo, titre et infos utilisateur"""
    col1, col2, col3 = st.columns([3, 1, 2])
    
    with col1:
        # Logo + Titre
        if LOGO_CDG_PATH.exists():
            st.image(str(LOGO_CDG_PATH), width=80)
        st.markdown(f"""
        <div style="margin-left: 20px;">
            <h2 style="margin: 0; color: {COLORS['primary']};">Newz</h2>
            <p style="margin: 0; font-size: 12px; color: #666;">Market Data Platform v{APP_VERSION}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Horloge
        from datetime import datetime
        now = datetime.now()
        st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <p style="margin: 0; font-size: 14px; font-weight: bold;">{now.strftime('%H:%M:%S')}</p>
            <p style="margin: 0; font-size: 11px; color: #666;">{now.strftime('%d/%m/%Y')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Utilisateur + Notifications
        st.markdown(f"""
        <div style="text-align: right; padding: 10px;">
            <p style="margin: 0; font-size: 14px;">👤 Ilyas</p>
            <p style="margin: 0; font-size: 11px; color: #666;">CDG Capital</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. SIDEBAR DE NAVIGATION
# -----------------------------------------------------------------------------
def render_sidebar():
    """Affiche la sidebar avec navigation"""
    
    # Bouton toggle sidebar
    if st.sidebar.button("◀" if st.session_state.sidebar_state == 'expanded' else "▶", 
                         key="toggle_sidebar"):
        st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
        st.rerun()
    
    # Navigation
    for page_key, page_info in NAVIGATION.items():
        # Skip settings for now (will be implemented later)
        if page_key == 'settings':
            continue
            
        is_active = st.session_state.current_page == page_key
        
        # Style conditionnel
        if is_active:
            st.sidebar.markdown(f"""
            <div class="nav-item active">
                <span>{page_info['icon']}</span>
                <span>{page_info['label']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.sidebar.button(f"{page_info['icon']} {page_info['label']}", 
                                 key=f"nav_{page_key}",
                                 use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
    
    # Footer sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="text-align: center; font-size: 11px; color: #666;">
        <p>© CDG Capital</p>
        <p>Réalisé par OULMADANI</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. CHARGEMENT DES PAGES
# -----------------------------------------------------------------------------
def load_page(page_name):
    """Charge dynamiquement la page demandée"""
    try:
        if page_name == 'home':
            from pages.home import render
            render()
        elif page_name == 'data_ingestion':
            from pages.data_ingestion import render
            render()
        elif page_name == 'bdc_statut':
            from pages.bdc_statut import render
            render()
        elif page_name == 'bam':
            from pages.bam import render
            render()
        elif page_name == 'macronews':
            from pages.macronews import render
            render()
        elif page_name == 'export':
            from pages.export import render
            render()
        else:
            st.error(f"Page '{page_name}' non trouvée")
    except ImportError as e:
        st.error(f"Erreur d'import de la page {page_name}: {str(e)}")
        st.info("Cette page sera implémentée dans les prochains fichiers.")

# -----------------------------------------------------------------------------
# 8. FOOTER
# -----------------------------------------------------------------------------
def render_footer():
    """Affiche le footer de l'application"""
    st.markdown(f"""
    <div class="footer">
        <p>Newz v{APP_VERSION} | Développé pour CDG Capital | Données en temps différé</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. FONCTION PRINCIPALE

def main():
    """Fonction principale de l'application"""
    
    # CSS Personnalisé pour améliorer le design
    st.markdown("""
    <style>
        /* Import du CSS externe */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Appliquer la police */
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Cacher le menu hamburger */
        #MainMenu {visibility: hidden;}
        
        /* Header personnalisé */
        .header-cdg {
            background: linear-gradient(135deg, #005696 0%, #003d6b 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: -10px -10px 30px -10px;
            box-shadow: 0 4px 20px rgba(0, 86, 150, 0.3);
        }
        
        /* Cartes KPI */
        .kpi-card {
            background: white;
            border-left: 5px solid #005696;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        
        /* Boutons */
        .stButton > button {
            background: #005696;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: #003d6b;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 86, 150, 0.4);
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* Métriques */
        [data-testid="stMetricValue"] {
            color: #005696;
            font-size: 28px;
            font-weight: 700;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .main > div {
            animation: fadeIn 0.5s ease-out;
        }
    </style>
    """, unsafe_allow_html=True) 
    
    """Fonction principale de l'application"""
    
    # Chargement du CSS personnalisé
    load_custom_css()
    
    # Affichage du header
    render_header()
    
    # Affichage de la sidebar
    render_sidebar()
    
    # Zone de contenu principal
    st.markdown(f"""
    <div style="margin-top: 20px;">
        <p style="color: #666; font-size: 14px;">
            Accueil > {NAVIGATION.get(st.session_state.current_page, {}).get('label', 'Accueil')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement de la page active
    load_page(st.session_state.current_page)
    
    # Footer
    render_footer()

# -----------------------------------------------------------------------------
# 10. POINT D'ENTRÉE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
