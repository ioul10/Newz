# =============================================================================
# NEWZ - Module Data Ingestion
# Fichier : pages/data_ingestion.py
# =============================================================================

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import sys
import time
import random

# Import des configurations
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import COLORS, DATA_DIR, SOURCES

# -----------------------------------------------------------------------------
# 1. INITIALISATION DE L'ÉTAT DE SESSION
# -----------------------------------------------------------------------------
if 'last_ingestion' not in st.session_state:
    st.session_state.last_ingestion = None
if 'ingestion_status' not in st.session_state:
    st.session_state.ingestion_status = {}
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = {}

# -----------------------------------------------------------------------------
# 2. FONCTIONS SIMULÉES DE COLLECTE (À REMPLACER PAR VRAI SCRAPING)
# -----------------------------------------------------------------------------
def fetch_bourse_casa_data():
    """
    Simule la collecte des données depuis la Bourse de Casablanca
    TODO: Implémenter le vrai scraping avec BeautifulSoup/requests
    """
    # Données simulées pour le développement
    return {
        'masi': {
            'value': 12450.50,
            'change': 0.85,
            'volume': 45000000,
            'timestamp': datetime.now()
        },
        'msi20': {
            'value': 1580.30,
            'change': 1.20,
            'volume': 38000000,
            'timestamp': datetime.now()
        },
        'status': 'success',
        'source': 'casablanca-bourse.com'
    }

def fetch_bam_data():
    """
    Simule la collecte des données depuis Bank Al-Maghrib
    TODO: Implémenter le vrai scraping avec BeautifulSoup/requests
    """
    # Données simulées pour le développement
    return {
        'monia': {
            'value': 3.00,
            'change': 0.05,
            'timestamp': datetime.now()
        },
        'bt10': {
            'value': 3.85,
            'change': -0.02,
            'timestamp': datetime.now()
        },
        'usd_mad': {
            'value': 9.85,
            'change': -0.15,
            'timestamp': datetime.now()
        },
        'eur_mad': {
            'value': 10.75,
            'change': 0.10,
            'timestamp': datetime.now()
        },
        'status': 'success',
        'source': 'bkam.ma'
    }

def validate_data_quality(data_dict):
    """
    Vérifie la qualité des données collectées
    Retourne un rapport de validation
    """
    report = {
        'total_checks': 0,
        'passed': 0,
        'failed': 0,
        'warnings': []
    }
    
    # Check 1: Données manquantes
    report['total_checks'] += 1
    if data_dict and len(data_dict) > 0:
        report['passed'] += 1
    else:
        report['failed'] += 1
        report['warnings'].append("⚠️ Aucune donnée collectée")
    
    # Check 2: Valeurs aberrantes (exemple simple)
    report['total_checks'] += 1
    if 'masi' in data_dict:
        masi_value = data_dict.get('masi', {}).get('value', 0)
        if 5000 < masi_value < 20000:  # Seuil raisonnable pour MASI
            report['passed'] += 1
        else:
            report['failed'] += 1
            report['warnings'].append(f"⚠️ Valeur MASI suspecte: {masi_value}")
    else:
        report['passed'] += 1
    
    # Check 3: Fraîcheur des données
    report['total_checks'] += 1
    if 'masi' in data_dict:
        timestamp = data_dict.get('masi', {}).get('timestamp')
        if timestamp and (datetime.now() - timestamp).total_seconds() < 86400:
            report['passed'] += 1
        else:
            report['failed'] += 1
            report['warnings'].append("⚠️ Données trop anciennes (> 24h)")
    else:
        report['passed'] += 1
    
    return report

# -----------------------------------------------------------------------------
# 3. FONCTION DE COLLECTE PRINCIPALE
# -----------------------------------------------------------------------------
def run_data_ingestion():
    """
    Lance la collecte complète des données
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = {
        'bourse_casa': None,
        'bam': None,
        'quality_report': None,
        'timestamp': datetime.now()
    }
    
    try:
        # Étape 1: Bourse de Casablanca
        status_text.text("📊 Collecte Bourse de Casablanca...")
        time.sleep(1)  # Simulation du temps de scraping
        results['bourse_casa'] = fetch_bourse_casa_data()
        progress_bar.progress(33)
        
        # Étape 2: Bank Al-Maghrib
        status_text.text("🏦 Collecte Bank Al-Maghrib...")
        time.sleep(1)  # Simulation du temps de scraping
        results['bam'] = fetch_bam_data()
        progress_bar.progress(66)
        
        # Étape 3: Validation qualité
        status_text.text("✅ Validation des données...")
        time.sleep(0.5)
        combined_data = {**results['bourse_casa'], **results['bam']}
        results['quality_report'] = validate_data_quality(combined_data)
        progress_bar.progress(100)
        
        status_text.text("✅ Collecte terminée avec succès !")
        
        # Mise à jour de l'état de session
        st.session_state.last_ingestion = datetime.now()
        st.session_state.ingestion_status = results
        st.session_state.data_cache = combined_data
        
        return results
        
    except Exception as e:
        status_text.text(f"❌ Erreur: {str(e)}")
        st.error(f"Échec de la collecte: {str(e)}")
        return None
    finally:
        time.sleep(1)
        status_text.empty()

# -----------------------------------------------------------------------------
# 4. AFFICHAGE DES RÉSULTATS DE COLLECTE
# -----------------------------------------------------------------------------
def display_ingestion_results():
    """Affiche les résultats de la dernière collecte"""
    
    if not st.session_state.ingestion_status:
        st.info("📭 Aucune collecte effectuée. Cliquez sur 'Lancer la collecte' pour commencer.")
        return
    
    results = st.session_state.ingestion_status
    
    # ---------------------------------------------------------------------
    # SECTION 1: STATUT GÉNÉRAL
    # ---------------------------------------------------------------------
    st.markdown("### 📊 Statut de la Collecte")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_bourse = results.get('bourse_casa', {}).get('status', 'unknown')
        st.metric(
            label="Bourse de Casablanca",
            value="✅ Succès" if status_bourse == 'success' else "❌ Échec",
            delta=None
        )
    
    with col2:
        status_bam = results.get('bam', {}).get('status', 'unknown')
        st.metric(
            label="Bank Al-Maghrib",
            value="✅ Succès" if status_bam == 'success' else "❌ Échec",
            delta=None
        )
    
    with col3:
        quality = results.get('quality_report', {})
        quality_score = f"{quality.get('passed', 0)}/{quality.get('total_checks', 0)}"
        st.metric(
            label="Qualité des données",
            value=quality_score,
            delta=None
        )
    
    # ---------------------------------------------------------------------
    # SECTION 2: DONNÉES COLLECTÉES (TABLEAU RÉCAPITULATIF)
    # ---------------------------------------------------------------------
    st.markdown("### 📋 Données Collectées")
    
    # Création d'un DataFrame récapitulatif
    data_rows = []
    
    # Bourse de Casablanca
    if results.get('bourse_casa'):
        bc = results['bourse_casa']
        data_rows.append({
            'Source': 'Bourse de Casablanca',
            'Indicateur': 'MASI',
            'Valeur': bc.get('masi', {}).get('value', 'N/A'),
            'Variation': f"{bc.get('masi', {}).get('change', 0):+.2f}%",
            'Volume': f"{bc.get('masi', {}).get('volume', 0):,}"
        })
        data_rows.append({
            'Source': 'Bourse de Casablanca',
            'Indicateur': 'MSI20',
            'Valeur': bc.get('msi20', {}).get('value', 'N/A'),
            'Variation': f"{bc.get('msi20', {}).get('change', 0):+.2f}%",
            'Volume': f"{bc.get('msi20', {}).get('volume', 0):,}"
        })
    
    # Bank Al-Maghrib
    if results.get('bam'):
        bam = results['bam']
        data_rows.append({
            'Source': 'Bank Al-Maghrib',
            'Indicateur': 'MONIA',
            'Valeur': f"{bam.get('monia', {}).get('value', 'N/A')}%",
            'Variation': f"{bam.get('monia', {}).get('change', 0):+.2f}%",
            'Volume': 'N/A'
        })
        data_rows.append({
            'Source': 'Bank Al-Maghrib',
            'Indicateur': 'USD/MAD',
            'Valeur': bam.get('usd_mad', {}).get('value', 'N/A'),
            'Variation': f"{bam.get('usd_mad', {}).get('change', 0):+.2f}%",
            'Volume': 'N/A'
        })
        data_rows.append({
            'Source': 'Bank Al-Maghrib',
            'Indicateur': 'EUR/MAD',
            'Valeur': bam.get('eur_mad', {}).get('value', 'N/A'),
            'Variation': f"{bam.get('eur_mad', {}).get('change', 0):+.2f}%",
            'Volume': 'N/A'
        })
    
    if data_rows:
        df = pd.DataFrame(data_rows)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("⚠️ Aucune donnée à afficher")
    
    # ---------------------------------------------------------------------
    # SECTION 3: RAPPORT DE QUALITÉ
    # ---------------------------------------------------------------------
    st.markdown("### 🔍 Contrôle Qualité")
    
    quality_report = results.get('quality_report', {})
    
    if quality_report:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if quality_report.get('warnings'):
                st.warning("⚠️ **Avertissements :**")
                for warning in quality_report['warnings']:
                    st.write(f"- {warning}")
            else:
                st.success("✅ Aucune anomalie détectée")
        
        with col2:
            # Jauge de qualité
            total = quality_report.get('total_checks', 1)
            passed = quality_report.get('passed', 0)
            score = (passed / total) * 100 if total > 0 else 0
            
            st.metric(
                label="Score de qualité",
                value=f"{score:.0f}%"
            )
    
    # ---------------------------------------------------------------------
    # SECTION 4: HISTORIQUE DES COLLECTES
    # ---------------------------------------------------------------------
    st.markdown("### 📜 Historique")
    
    if st.session_state.last_ingestion:
        st.info(f"🕐 Dernière collecte : {st.session_state.last_ingestion.strftime('%d/%m/%Y à %H:%M:%S')}")
    else:
        st.info("📭 Aucune collecte enregistrée")

# -----------------------------------------------------------------------------
# 5. FONCTION DE RENDU PRINCIPAL
# -----------------------------------------------------------------------------
def render():
    """Affiche la page Data Ingestion"""
    
    # ---------------------------------------------------------------------
    # HEADER DE LA PAGE
    # ---------------------------------------------------------------------
    st.markdown(f"""
    <div style="
        background: white;
        border-left: 5px solid {COLORS['primary']};
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    ">
        <h2 style="margin: 0; color: {COLORS['primary']};">📥 Data Ingestion</h2>
        <p style="margin: 10px 0 0 0; color: #666;">
            Collecte et validation des données depuis les sources officielles
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------
    # SECTION 1: BOUTON DE COLLECTE
    # ---------------------------------------------------------------------
    st.markdown("### 🚀 Lancer la Collecte")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        if st.button(
            "▶️ Lancer la collecte",
            type="primary",
            use_container_width=True,
            disabled=False  # Peut être désactivé si collecte en cours
        ):
            with st.spinner("Collecte en cours..."):
                results = run_data_ingestion()
                if results:
                    st.success("✅ Collecte terminée avec succès !")
                    st.rerun()
    
    # ---------------------------------------------------------------------
    # SECTION 2: SOURCES DE DONNÉES
    # ---------------------------------------------------------------------
    st.markdown("### 🌐 Sources Configurées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        ">
            <h4 style="margin: 0; color: {COLORS['primary']};">🏦 Bourse de Casablanca</h4>
            <p style="font-size: 13px; color: #666; margin: 10px 0 0 0;">
                URL: {SOURCES['bourse_casa']['base_url']}<br>
                Données: MASI, MSI20, Volumes<br>
                Fréquence: Quotidienne (fin de séance)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        ">
            <h4 style="margin: 0; color: {COLORS['primary']};">🏛️ Bank Al-Maghrib</h4>
            <p style="font-size: 13px; color: #666; margin: 10px 0 0 0;">
                URL: {SOURCES['bam']['base_url']}<br>
                Données: MONIA, BDT, Devises<br>
                Fréquence: Quotidienne (taux officiels)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------
    # SECTION 3: RÉSULTATS DE COLLECTE
    # ---------------------------------------------------------------------
    st.markdown("---")
    display_ingestion_results()
    
    # ---------------------------------------------------------------------
    # SECTION 4: OPTIONS AVANCÉES
    # ---------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### ⚙️ Options Avancées")
    
    with st.expander("🔧 Configuration du Scraping", expanded=False):
        st.markdown("""
        **Paramètres de collecte :**
        - Timeout: 10 secondes par requête
        - Retries: 3 tentatives maximum
        - Cache: 1 heure
        
        **Note :** Ces paramètres sont configurés dans `config/settings.py`
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Timeout (secondes)",
                min_value=5,
                max_value=60,
                value=10,
                disabled=True
            )
        with col2:
            st.number_input(
                "Nombre de retries",
                min_value=1,
                max_value=10,
                value=3,
                disabled=True
            )
    
    with st.expander("📁 Export des Données Brutes", expanded=False):
        if st.session_state.data_cache:
            st.info("Les données collectées sont disponibles en cache pour cette session.")
            
            # Option d'export CSV
            if st.button("📥 Exporter en CSV"):
                # Création d'un DataFrame pour export
                df_export = pd.DataFrame([st.session_state.data_cache])
                csv = df_export.to_csv(index=False)
                st.download_button(
                    label="Télécharger CSV",
                    data=csv,
                    file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("⚠️ Aucune donnée en cache. Lancez d'abord une collecte.")

# -----------------------------------------------------------------------------
# 6. POINT D'ENTRÉE POUR TEST UNITAIRE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    render()
