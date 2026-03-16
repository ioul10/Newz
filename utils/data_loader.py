# =============================================================================
# NEWZ - Module Data Loader (Cache & Persistance)
# Fichier : utils/data_loader.py
# =============================================================================

import json
import pickle
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import sys
import os

# Import des configurations
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import DATA_DIR, CACHE_TTL

# -----------------------------------------------------------------------------
# 1. CONSTANTES ET CONFIGURATION
# -----------------------------------------------------------------------------
# Dossier de cache
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# Fichiers de cache
CACHE_FILES = {
    'bourse_casa': CACHE_DIR / 'bourse_casa.pkl',
    'bam': CACHE_DIR / 'bam.pkl',
    'news': CACHE_DIR / 'news.pkl',
    'inflation': CACHE_DIR / 'inflation.pkl',
    'metadata': CACHE_DIR / 'metadata.json'
}

# TTL (Time To Live) en secondes
CACHE_TTL_SECONDS = {
    'bourse_casa': 3600,      # 1 heure
    'bam': 3600,              # 1 heure
    'news': 1800,             # 30 minutes
    'inflation': 86400,       # 24 heures (donnée mensuelle)
    'metadata': 86400         # 24 heures
}

# -----------------------------------------------------------------------------
# 2. FONCTIONS DE BASE DU CACHE
# -----------------------------------------------------------------------------
def get_cache_path(key):
    """Retourne le chemin du fichier de cache pour une clé donnée"""
    return CACHE_FILES.get(key, CACHE_DIR / f'{key}.pkl')

def is_cache_valid(key):
    """
    Vérifie si le cache est valide (existe + pas expiré)
    
    Args:
        key (str): Clé du cache (ex: 'bourse_casa', 'bam')
    
    Returns:
        bool: True si le cache est valide, False sinon
    """
    cache_path = get_cache_path(key)
    
    # Check 1: Fichier existe
    if not cache_path.exists():
        return False
    
    # Check 2: TTL pas expiré
    ttl = CACHE_TTL_SECONDS.get(key, 3600)
    file_mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
    
    if datetime.now() - file_mtime > timedelta(seconds=ttl):
        return False
    
    return True

def load_from_cache(key):
    """
    Charge les données depuis le cache
    
    Args:
        key (str): Clé du cache
    
    Returns:
        dict or None: Données chargées ou None si cache invalide
    """
    if not is_cache_valid(key):
        return None
    
    cache_path = get_cache_path(key)
    
    try:
        if cache_path.suffix == '.pkl':
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
        elif cache_path.suffix == '.json':
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif cache_path.suffix == '.csv':
            data = pd.read_csv(cache_path)
        else:
            return None
        
        return data
    
    except Exception as e:
        print(f"❌ Erreur de lecture du cache [{key}]: {str(e)}")
        return None

def save_to_cache(key, data):
    """
    Sauvegarde les données dans le cache
    
    Args:
        key (str): Clé du cache
        data (any): Données à sauvegarder
    
    Returns:
        bool: True si succès, False sinon
    """
    cache_path = get_cache_path(key)
    
    try:
        # Création du dossier si nécessaire
        cache_path.parent.mkdir(exist_ok=True)
        
        # Sauvegarde selon le format
        if cache_path.suffix == '.pkl':
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        elif cache_path.suffix == '.json':
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        elif cache_path.suffix == '.csv':
            if isinstance(data, pd.DataFrame):
                data.to_csv(cache_path, index=False)
            else:
                raise ValueError("Données CSV doivent être un DataFrame pandas")
        else:
            # Défaut: pickle
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
        
        print(f"✅ Cache sauvegardé [{key}]: {cache_path}")
        return True
    
    except Exception as e:
        print(f"❌ Erreur d'écriture du cache [{key}]: {str(e)}")
        return False

def clear_cache(key=None):
    """
    Efface le cache
    
    Args:
        key (str, optional): Clé spécifique à effacer. Si None, efface tout.
    
    Returns:
        int: Nombre de fichiers effacés
    """
    count = 0
    
    if key:
        # Effacer un cache spécifique
        cache_path = get_cache_path(key)
        if cache_path.exists():
            cache_path.unlink()
            count = 1
            print(f"✅ Cache effacé [{key}]")
    else:
        # Effacer tout le cache
        for cache_path in CACHE_FILES.values():
            if cache_path.exists():
                cache_path.unlink()
                count += 1
        
        # Effacer tous les autres fichiers .pkl, .json, .csv dans le dossier cache
        for file in CACHE_DIR.glob('*'):
            if file.is_file():
                file.unlink()
                count += 1
        
        print(f"✅ Tout le cache a été effacé ({count} fichiers)")
    
    return count

def get_cache_info():
    """
    Retourne des informations sur l'état du cache
    
    Returns:
        dict: Informations sur chaque cache (existe, valide, taille, âge)
    """
    info = {}
    
    for key, cache_path in CACHE_FILES.items():
        ttl = CACHE_TTL_SECONDS.get(key, 3600)
        
        file_info = {
            'exists': cache_path.exists(),
            'valid': False,
            'size_kb': 0,
            'age_minutes': 0,
            'ttl_minutes': ttl // 60
        }
        
        if cache_path.exists():
            # Taille
            file_info['size_kb'] = round(cache_path.stat().st_size / 1024, 2)
            
            # Âge
            file_mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
            age = datetime.now() - file_mtime
            file_info['age_minutes'] = round(age.total_seconds() / 60, 1)
            
            # Validité
            file_info['valid'] = age.total_seconds() < ttl
        
        info[key] = file_info
    
    return info

# -----------------------------------------------------------------------------
# 3. FONCTIONS SPÉCIFIQUES PAR TYPE DE DONNÉES
# -----------------------------------------------------------------------------
def load_bourse_casa_data():
    """Charge les données Bourse de Casablanca depuis le cache"""
    return load_from_cache('bourse_casa')

def save_bourse_casa_data(data):
    """Sauvegarde les données Bourse de Casablanca dans le cache"""
    return save_to_cache('bourse_casa', data)

def load_bam_data():
    """Charge les données Bank Al-Maghrib depuis le cache"""
    return load_from_cache('bam')

def save_bam_data(data):
    """Sauvegarde les données Bank Al-Maghrib dans le cache"""
    return save_to_cache('bam', data)

def load_news_data():
    """Charge les données news depuis le cache"""
    return load_from_cache('news')

def save_news_data(data):
    """Sauvegarde les données news dans le cache"""
    return save_to_cache('news', data)

def load_inflation_data():
    """Charge les données inflation depuis le cache"""
    return load_from_cache('inflation')

def save_inflation_data(data):
    """Sauvegarde les données inflation dans le cache"""
    return save_to_cache('inflation', data)

# -----------------------------------------------------------------------------
# 4. MÉTADONNÉES DU CACHE
# -----------------------------------------------------------------------------
def save_metadata(metadata):
    """
    Sauvegarde les métadonnées du système
    
    Args:
        metadata (dict): Métadonnées à sauvegarder
    """
    metadata['last_updated'] = datetime.now().isoformat()
    metadata['version'] = '1.0.0'
    save_to_cache('metadata', metadata)

def load_metadata():
    """
    Charge les métadonnées du système
    
    Returns:
        dict: Métadonnées ou dict vide si inexistant
    """
    data = load_from_cache('metadata')
    return data if data else {}

# -----------------------------------------------------------------------------
# 5. EXPORT/IMPORT DE DONNÉES (Pour backup ou partage)
# -----------------------------------------------------------------------------
def export_all_data(output_path=None):
    """
    Exporte toutes les données du cache dans un fichier unique
    
    Args:
        output_path (str, optional): Chemin du fichier de sortie.
                                     Par défaut: data/export_YYYYMMDD_HHMMSS.json
    
    Returns:
        str: Chemin du fichier exporté
    """
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = DATA_DIR / f'export_{timestamp}.json'
    else:
        output_path = Path(output_path)
    
    export_data = {
        'export_date': datetime.now().isoformat(),
        'version': '1.0.0',
        'data': {}
    }
    
    for key in CACHE_FILES.keys():
        if key != 'metadata':
            data = load_from_cache(key)
            if data:
                # Conversion pour sérialisation JSON
                if isinstance(data, pd.DataFrame):
                    data = data.to_dict('records')
                export_data['data'][key] = data
    
    try:
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Données exportées : {output_path}")
        return str(output_path)
    
    except Exception as e:
        print(f"❌ Erreur d'export : {str(e)}")
        return None

def import_all_data(input_path):
    """
    Importe des données depuis un fichier exporté
    
    Args:
        input_path (str): Chemin du fichier à importer
    
    Returns:
        bool: True si succès, False sinon
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        for key, data in import_data.get('data', {}).items():
            if key in CACHE_FILES:
                # Conversion depuis dict si nécessaire
                if key in ['bourse_casa', 'bam']:
                    save_to_cache(key, data)
                elif key == 'news':
                    save_to_cache(key, data)
        
        print(f"✅ Données importées : {input_path}")
        return True
    
    except Exception as e:
        print(f"❌ Erreur d'import : {str(e)}")
        return False

# -----------------------------------------------------------------------------
# 6. NETTOYAGE AUTOMATIQUE DU CACHE
# -----------------------------------------------------------------------------
def cleanup_old_cache(max_age_days=7):
    """
    Nettoie les fichiers de cache trop anciens
    
    Args:
        max_age_days (int): Âge maximum en jours
    
    Returns:
        int: Nombre de fichiers supprimés
    """
    count = 0
    cutoff = datetime.now() - timedelta(days=max_age_days)
    
    for file in CACHE_DIR.glob('*'):
        if file.is_file():
            file_mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if file_mtime < cutoff:
                file.unlink()
                count += 1
                print(f"🗑️ Fichier supprimé : {file.name}")
    
    print(f"✅ Nettoyage terminé : {count} fichiers supprimés")
    return count

# -----------------------------------------------------------------------------
# 7. TEST ET VALIDATION
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    """Script de test du module data_loader"""
    
    print("=" * 60)
    print("🧪 TEST DU MODULE DATA LOADER")
    print("=" * 60)
    
    # Test 1: Informations du cache
    print("\n📊 État actuel du cache :")
    info = get_cache_info()
    for key, file_info in info.items():
        status = "✅ Valide" if file_info['valid'] else "❌ Invalide" if file_info['exists'] else "⚪ Inexistant"
        print(f"  {key}: {status} ({file_info['size_kb']} KB, {file_info['age_minutes']} min)")
    
    # Test 2: Sauvegarde de données test
    print("\n💾 Test de sauvegarde...")
    test_data = {
        'test': 'data',
        'timestamp': datetime.now().isoformat(),
        'values': [1, 2, 3, 4, 5]
    }
    save_bourse_casa_data(test_data)
    
    # Test 3: Chargement de données test
    print("\n📥 Test de chargement...")
    loaded_data = load_bourse_casa_data()
    if loaded_data:
        print(f"  ✅ Données chargées : {loaded_data}")
    else:
        print("  ❌ Échec du chargement")
    
    # Test 4: Validation du cache
    print("\n✅ Test de validité...")
    is_valid = is_cache_valid('bourse_casa')
    print(f"  Cache 'bourse_casa' valide : {is_valid}")
    
    # Test 5: Informations après test
    print("\n📊 État du cache après test :")
    info = get_cache_info()
    for key, file_info in info.items():
        status = "✅ Valide" if file_info['valid'] else "❌ Invalide" if file_info['exists'] else "⚪ Inexistant"
        print(f"  {key}: {status} ({file_info['size_kb']} KB, {file_info['age_minutes']} min)")
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS")
    print("=" * 60)
