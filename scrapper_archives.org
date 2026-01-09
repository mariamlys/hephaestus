"""
Scraper pour Archive.org Music - Musiques par catégorie de sport
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict
import re


class ArchiveMusicScraper:
    """Scraper pour récupérer les musiques d'Archive.org par catégorie"""

    def __init__(self):
        self.base_url = "https://archive.org"
        self.search_url = "https://archive.org/advancedsearch.php"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Catégories de sport à scraper
        self.sport_categories = {
            "course_a_pied": ["running", "jogging", "cardio", "energetic"],
            "echauffement": ["warm up", "light", "gentle", "stretching"],
            "boxe": ["boxing", "intense", "aggressive", "power", "fight"],
            "marche_a_pied": ["walking", "calm", "relaxing", "peaceful"],
            "musculation": ["workout", "gym", "training", "motivation", "fitness"]
        }

    def search_music(self, keywords: List[str], max_results: int = 20) -> List[Dict]:
        """
        Cherche des musiques sur Archive.org selon des mots-clés

        Args:
            keywords: Liste de mots-clés à chercher
            max_results: Nombre maximum de résultats

        Returns:
            Liste de dictionnaires contenant les infos des musiques
        """
        all_tracks = []

        for keyword in keywords:
            try:
                # Paramètres de recherche Archive.org
                # On cherche dans la collection audio avec le mot-clé
                params = {
                    'q': f'{keyword} AND mediatype:audio',
                    'fl[]': ['identifier', 'title', 'creator', 'description'],
                    'sort[]': 'downloads desc',
                    'rows': max_results,
                    'page': 1,
                    'output': 'json'
                }

                print(f"🔍 Recherche: {keyword}")
                response = requests.get(self.search_url, params=params, headers=self.headers, timeout=15)
                response.raise_for_status()

                data = response.json()

                if 'response' in data and 'docs' in data['response']:
                    for doc in data['response']['docs'][:max_results]:
                        try:
                            track_info = self._process_item(doc, keyword)
                            if track_info:
                                all_tracks.append(track_info)
                        except Exception as e:
                            print(f"⚠️  Erreur traitement item: {e}")
                            continue

                print(f"✅ {len(data['response']['docs'])} résultats pour '{keyword}'")

                # Délai pour être respectueux du serveur
                time.sleep(1.5)

            except Exception as e:
                print(f"❌ Erreur scraping '{keyword}': {e}")
                continue

        return all_tracks

    def _process_item(self, doc: Dict, keyword: str) -> Dict:
        """
        Traite un item de résultat Archive.org et extrait les infos
        """
        try:
            identifier = doc.get('identifier', '')
            title = doc.get('title', 'Unknown')
            creator = doc.get('creator', 'Unknown Artist')

            # Construire les URLs
            item_url = f"{self.base_url}/details/{identifier}"

            # URL de téléchargement (Archive.org structure)
            # On suppose qu'il y a un fichier MP3 disponible
            download_url = f"{self.base_url}/download/{identifier}"

            # URL de preview/streaming
            preview_url = f"{self.base_url}/embed/{identifier}"

            return {
                'identifier': identifier,
                'title': title if isinstance(title, str) else title[0] if isinstance(title, list) else 'Unknown',
                'artist': creator if isinstance(creator, str) else creator[0] if isinstance(creator,
                                                                                            list) else 'Unknown',
                'duration': 'N/A',  # Archive.org API de base ne donne pas toujours la durée
                'download_url': download_url,
                'preview_url': preview_url,
                'page_url': item_url,
                'keyword': keyword,
                'source': 'archive.org'
            }

        except Exception as e:
            print(f"⚠️  Erreur extraction: {e}")
            return None

    def get_detailed_info(self, identifier: str) -> Dict:
        """
        Récupère les informations détaillées d'un item (durée, format, etc.)
        Optionnel: pour avoir plus de détails si nécessaire
        """
        try:
            metadata_url = f"{self.base_url}/metadata/{identifier}"
            response = requests.get(metadata_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            metadata = response.json()

            # Chercher les fichiers audio dans les métadonnées
            files = metadata.get('files', [])
            audio_files = [f for f in files if f.get('format', '').lower() in ['mp3', 'ogg', 'flac']]

            if audio_files:
                # Prendre le premier fichier MP3
                audio_file = next((f for f in audio_files if f.get('format', '').lower() == 'mp3'), audio_files[0])

                duration = audio_file.get('length', 'N/A')
                filename = audio_file.get('name', '')

                return {
                    'duration': duration,
                    'filename': filename,
                    'direct_download': f"{self.base_url}/download/{identifier}/{filename}"
                }

            return {}

        except Exception as e:
            print(f"⚠️  Erreur métadonnées {identifier}: {e}")
            return {}

    def scrape_all_categories(self, tracks_per_category: int = 15) -> Dict:
        """
        Scrape toutes les catégories de sport

        Returns:
            Dictionnaire avec les musiques par catégorie
        """
        all_data = {}
