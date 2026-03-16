# =============================================================================
# NEWZ - Composant Sidebar (Navigation Latérale)
# Fichier : components/sidebar.py
# =============================================================================

import streamlit as st
from pathlib import Path
from datetime import datetime
import sys

# Import des configurations
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import COLORS, NAVIGATION, APP_VERSION

# -----------------------------------------------------------------------------
# 1. INITIALISATION DE L'ÉTAT DE SESSION
# -----------------------------------------------------------------------------
def init_sidebar_state():
    """Initialise l'état de session pour la sidebar"""
    if 'sidebar_collapsed' not in st.session_state:
        st.session_state.sidebar_collapsed = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'sidebar_notifications' not in st.session_state:
        st.session_state.sidebar_notifications = {}

# -----------------------------------------------------------------------------
# 2. BOUTON TOGGLE (RÉTRACTION)
# -----------------------------------------------------------------------------
def render_toggle_button():
    """Affiche le bouton pour rétracter/déployer la sidebar"""
    
    # Positionné en bas de sidebar
    st.sidebar.markdown("---")
    
    col1, col2 = st.sidebar.columns([3, 1])
    
    with col1:
        st.caption(f"Newz v{APP_VERSION}")
    
    with col2:
        # Icône toggle
        toggle_icon = "◀" if not st.session_state.sidebar_collapsed else "▶"
        if st.button(
            toggle_icon,
            key="sidebar_toggle",
            help="Rétracter/Déployer la sidebar"
        ):
            st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
            st.rerun()

# -----------------------------------------------------------------------------
# 3. ÉLÉMENTS DE NAVIGATION
# -----------------------------------------------------------------------------
def render_navigation_items():
    """Affiche les éléments de navigation principaux"""
    
    for page_key, page_info in NAVIGATION.items():
        # Skip settings pour l'instant
        if page_key == 'settings':
            continue
        
        is_active = st.session_state.current_page == page_key
        
        # Notification badge (si des nouvelles données sont disponibles)
        notification = ""
        if page_key in st.session_state.sidebar_notifications:
            if st.session_state.sidebar_notifications[page_key]:
                notification = " 🔴"
        
        # Affichage selon état collapsed
        if st.session_state.sidebar_collapsed:
            # Mode rétracté : icône seulement
            if st.sidebar.button(
                f"{page_info['icon']}",
                key=f"nav_{page_key}",
                help=page_info['label'],
                use_container_width=True
            ):
                st.session_state.current_page = page_key
                st.rerun()
        else:
            # Mode déployé : icône + texte
            if is_active:
                # Style actif
                st.sidebar.markdown(f"""
                <div style="
                    background: {COLORS['primary']};
                    color: white;
                    padding: 12px 15px;
                    margin: 5px 10px;
                    border-radius: 8px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    border-left: 4px solid {COLORS['secondary']};
                ">
                    <span>{page_info['icon']}</span>
                    <span style="font-weight: bold;">{page_info['label']}</span>
                    {f'<span style="margin-left: auto; background: red; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px;">NEW</span>' if notification else ''}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Style inactif
                if st.sidebar.button(
                    f"{page_info['icon']} {page_info['label']}{notification}",
                    key=f"nav_{page_key}",
                    use_container_width=True,
                    help=page_info.get('description', '')
                ):
                    st.session_state.current_page = page_key
                    st.rerun()

# -----------------------------------------------------------------------------
# 4. SECTION UTILISATEUR
# -----------------------------------------------------------------------------
def render_user_section():
    """Affiche la section utilisateur en bas de sidebar"""
    
    st.sidebar.markdown("---")
    
    if not st.session_state.sidebar_collapsed:
        # Informations utilisateur
        st.sidebar.markdown(f"""
        <div style="
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            margin: 10px;
        ">
            <p style="margin: 0; font-size: 13px; font-weight: bold; color: {COLORS['primary']};">
                👤 Ilyas
            </p>
            <p style="margin: 5px 0 0 0; font-size: 11px; color: #666;">
                CDG Capital
            </p>
            <p style="margin: 5px 0 0 0; font-size: 10px; color: #999;">
                {datetime.now().strftime('%d/%m/%Y')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Bouton déconnexion (placeholder)
    if st.sidebar.button(
        "🚪 Déconnexion",
        key="btn_logout",
        help="Se déconnecter de l'application"
    ):
        st.warning("Fonctionnalité de déconnexion à implémenter")

# -----------------------------------------------------------------------------
# 5. SECTION STATUT DES DONNÉES
# -----------------------------------------------------------------------------
def render_data_status():
    """Affiche le statut des données en bas de sidebar"""
    
    if st.session_state.sidebar_collapsed:
        return
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Statut des Données")
    
    # Statut simulé (à connecter avec data_loader plus tard)
    status_data = {
        'bourse_casa': {'status': '✅', 'age': '2h'},
        'bam': {'status': '✅', 'age': '2h'},
        'news': {'status': '🟡', 'age': '30min'},
        'inflation': {'status': '⚪', 'age': '7j'}
    }
    
    for source, info in status_data.items():
        st.sidebar.caption(f"{info['status']} {source}: {info['age']}")

# -----------------------------------------------------------------------------
# 6. RACCOURCIS CLAVIER (INFO)
# -----------------------------------------------------------------------------
def render_keyboard_shortcuts():
    """Affiche les raccourcis clavier disponibles"""
    
    if st.session_state.sidebar_collapsed:
        return
    
    with st.sidebar.expander("⌨️ Raccourcis Clavier", expanded=False):
        st.markdown("""
        | Raccourci | Action |
        |-----------|--------|
        | `Ctrl + H` | Accueil |
        | `Ctrl + D` | Data Ingestion |
        | `Ctrl + B` | BDC Statut |
        | `Ctrl + M` | BAM |
        | `Ctrl + N` | Macronews |
        | `Ctrl + E` | Export PDF |
        | `Ctrl + R` | Rafraîchir |
        """)

# -----------------------------------------------------------------------------
# 7. PIED DE SIDEBAR
# -----------------------------------------------------------------------------
def render_sidebar_footer():
    """Affiche le pied de la sidebar"""
    
    if st.session_state.sidebar_collapsed:
        return
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="text-align: center; font-size: 10px; color: #999;">
        <p>© 2025 CDG Capital</p>
        <p>Usage interne uniquement</p>
        <p>Confidentiel</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 8. FONCTION PRINCIPALE DU COMPOSANT
# -----------------------------------------------------------------------------
def render_sidebar():
    """
    Fonction principale pour afficher la sidebar complète
    
    À appeler dans app.py après st.set_page_config()
    """
    
    # Initialisation de l'état
    init_sidebar_state()
    
    # Application du style CSS personnalisé pour la sidebar
    st.markdown(f"""
    <style>
        /* Cacher le menu hamburger Streamlit */
        #MainMenu {{visibility: hidden;}}
        
        /* Style de la sidebar */
        .stSidebar {{
            background-color: #f8f9fa;
            border-right: 1px solid #e0e0e0;
        }}
        
        /* Boutons de navigation */
        .stButton > button {{
            border: none;
            background: transparent;
            text-align: left;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background-color: #e3f2fd;
            color: {COLORS['primary']};
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Rendu des différents éléments
    render_navigation_items()
    render_data_status()
    render_keyboard_shortcuts()
    render_user_section()
    render_toggle_button()
    render_sidebar_footer()

# -----------------------------------------------------------------------------
# 9. FONCTIONS UTILITAIRES
# -----------------------------------------------------------------------------
def set_current_page(page_key):
    """Définit la page active"""
    st.session_state.current_page = page_key

def get_current_page():
    """Retourne la page active"""
    return st.session_state.current_page

def set_notification(page_key, has_notification):
    """Définit une notification pour une page"""
    st.session_state.sidebar_notifications[page_key] = has_notification

def clear_all_notifications():
    """Efface toutes les notifications"""
    st.session_state.sidebar_notifications = {}

def collapse_sidebar():
    """Rétracte la sidebar"""
    st.session_state.sidebar_collapsed = True

def expand_sidebar():
    """Déploie la sidebar"""
    st.session_state.sidebar_collapsed = False

# -----------------------------------------------------------------------------
# 10. TEST DU COMPOSANT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    """Test du composant sidebar (nécessite Streamlit)"""
    st.set_page_config(page_title="Test Sidebar", layout="wide")
    render_sidebar()
    
    st.markdown("### Test du Composant Sidebar")
    st.write(f"Page actuelle : {get_current_page()}")
    
    if st.button("Tester Notification"):
        set_notification('bdc_statut', True)
        st.rerun()
    
    if st.button("Effacer Notifications"):
        clear_all_notifications()
        st.rerun()
