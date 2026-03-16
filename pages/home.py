# =============================================================================
# NEWZ - Page d'Accueil
# Fichier : pages/home.py
# =============================================================================

import streamlit as st
from pathlib import Path
from datetime import datetime
import sys

# Import des configurations
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import APP_VERSION, COLORS, LOGO_CDG_PATH

# -----------------------------------------------------------------------------
# 1. FONCTION DE RENDU PRINCIPAL
# -----------------------------------------------------------------------------
def render():
    """Affiche la page d'accueil de Newz"""
    
    # ---------------------------------------------------------------------
    # SECTION 1 : BANNIÈRE DE BIENVENUE
    # ---------------------------------------------------------------------
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    ">
        <h1 style="margin: 0; font-size: 36px;">👋 Bienvenue sur Newz</h1>
        <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">
            Market Data Platform pour CDG Capital
        </p>
        <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.7;">
            Version {APP_VERSION} | Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------
    # SECTION 2 : LOGO ET PRÉSENTATION
    # ---------------------------------------------------------------------
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if LOGO_CDG_PATH.exists():
            st.image(str(LOGO_CDG_PATH), width=200, use_container_width=False)
        else:
            st.info("📁 Logo non trouvé. Ajoutez 'logo_cdg.png' dans le dossier assets/")
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            <h3 style="color: {COLORS['primary']};">Plateforme Market Data & Reporting</h3>
            <p style="color: #666; line-height: 1.6;">
                Newz centralise les données financières marocaines : indices boursiers, 
                taux Bank Al-Maghrib, devises, actualités et génération de rapports PDF professionnels.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------
    # SECTION 3 : MODULES PRINCIPAUX (Cartes interactives)
    # ---------------------------------------------------------------------
    st.markdown("### 📊 Modules Principaux")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: white;
            border-left: 5px solid {COLORS['primary']};
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        ">
            <h4 style="margin: 0; color: {COLORS['primary']};">📥 Data Ingestion</h4>
            <p style="font-size: 13px; color: #666; margin: 10px 0;">
                Collecte automatique des données depuis la Bourse de Casablanca et Bank Al-Maghrib
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: white;
            border-left: 5px solid {COLORS['accent']};
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        ">
            <h4 style="margin: 0; color: {COLORS['accent']};">📊 BDC Statut</h4>
            <p style="font-size: 13px; color: #666; margin: 10px 0;">
                Visualisation MASI/MSI20, statistiques et corrélations des valeurs
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: white;
            border-left: 5px solid {COLORS['success']};
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        ">
            <h4 style="margin: 0; color: {COLORS['success']};">📤 Export PDF</h4>
            <p style="font-size: 13px; color: #666; margin: 10px 0;">
                Génération de rapports professionnels 1-2 pages avec charte CDG
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------
    # SECTION 4 : GUIDE DE L'APPLICATION
    # ---------------------------------------------------------------------
    st.markdown("### 📖 Guide de l'Application")
    
    with st.expander("🚀 Comment utiliser Newz ?", expanded=False):
        st.markdown("""
        #### Étape 1 : Data Ingestion
        - Accédez à l'onglet **Data Ingestion** dans la sidebar
        - Cliquez sur "Lancer la collecte" pour récupérer les dernières données
        - Vérifiez le statut (🟢 Succès / 🔴 Échec)
        
        #### Étape 2 : Consulter les Données
        - **BDC Statut** : Visualisez MASI/MSI20 et statistiques
        - **BAM** : Consultez les taux MONIA, BDT et devises
        - **Macronews** : Lisez les actualités et l'inflation
        
        #### Étape 3 : Générer un Rapport
        - Allez dans **Export Rapport**
        - Sélectionnez les éléments à inclure
        - Prévisualisez puis téléchargez le PDF
        """)
        
        st.info("💡 **Astuce** : Utilisez les raccourcis clavier (Ctrl+H, Ctrl+D, Ctrl+B, etc.) pour naviguer rapidement !")
    
    # ---------------------------------------------------------------------
    # SECTION 5 : STATUT DES DONNÉES
    # ---------------------------------------------------------------------
    st.markdown("### 📈 Statut des Données")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Bourse de Casablanca",
            value="⏳ En attente",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Bank Al-Maghrib",
            value="⏳ En attente",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Dernière MAJ",
            value="Jamais",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Rapports générés",
            value="0",
            delta=None
        )
    
    st.caption("ℹ️ Ces indicateurs se mettront à jour après la première collecte de données.")
    
    # ---------------------------------------------------------------------
    # SECTION 6 : ABOUT ME
    # ---------------------------------------------------------------------
    st.markdown("---")
    
    st.markdown("### 👤 About Me")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Placeholder pour photo de profil (optionnel)
        st.markdown(f"""
        <div style="
            width: 100px;
            height: 100px;
            background: {COLORS['primary']};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 40px;
            margin: 0 auto;
        ">
            👤
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        **Développé par :** Ilyas  
        **Pour :** CDG Capital - Market Data Team  
        **Version :** {APP_VERSION}  
        **Contact :** marketdata@cdgcapital.ma
        
        ---
        
        #### 🎯 Objectif du Projet
        Newz a été conçu pour centraliser et automatiser la production de rapports market data 
        hebdomadaires, en respectant la charte graphique et les standards de CDG Capital.
        
        #### 🛠️ Technologies Utilisées
        - **Python** & **Streamlit** pour l'interface
        - **Pandas** pour le traitement des données
        - **Plotly** pour les graphiques interactifs
        - **WeasyPrint** pour la génération PDF
        """)
    
    # ---------------------------------------------------------------------
    # SECTION 7 : LIENS RAPIDES
    # ---------------------------------------------------------------------
    st.markdown("---")
    
    st.markdown("### 🔗 Liens Utiles")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.link_button(
            "🏦 Bourse de Casablanca",
            "https://www.casablanca-bourse.com"
        )
    
    with col2:
        st.link_button(
            "🏛️ Bank Al-Maghrib",
            "https://www.bkam.ma"
        )
    
    with col3:
        st.link_button(
            "📰 Ilboursa",
            "https://www.ilboursa.com"
        )
    
    with col4:
        st.link_button(
            "📧 Support",
            "mailto:support@cdgcapital.ma"
        )
    
    # ---------------------------------------------------------------------
    # SECTION 8 : BOUTON D'ACTION RAPIDE
    # ---------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        if st.button(
            "🚀 Commencer à utiliser Newz",
            type="primary",
            use_container_width=True
        ):
            st.session_state.current_page = 'data_ingestion'
            st.rerun()

# -----------------------------------------------------------------------------
# 2. POINT D'ENTRÉE POUR TEST UNITAIRE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    render()
