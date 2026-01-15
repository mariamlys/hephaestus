#!/usr/bin/env python3
"""
Scrapping pour Archive.org
"""

import requests
import json
import time
import os
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class ArchiveMusicScraper:
    """Scraper pour récupérer les musiques d'Archive.org par catégorie"""

    def __init__(self):
        self.base_url = "https://archive.org"
        self.search_url = "https://archive.org/advancedsearch.php"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # Catégories de sport à scraper
        self.sport_categories = {
            "course_a_pied": ["running", "jogging", "cardio", "energetic"],
            "echauffement": ["warm up", "stretching", "gentle", "meditation"],
            "boxe": ["boxing", "intense", "aggressive", "power", "fight"],
            "marche_a_pied": ["walking", "calm", "relaxing", "peaceful"],
            "musculation": ["workout", "gym", "training", "motivation", "fitness"]
        }

    def search_music(self, keywords: List[str], max_results: int = 10) -> List[Dict]:
        """
        Cherche des musiques sur Archive.org selon des mots-clés
        """
        all_tracks = []

        for keyword in keywords:
            try:
                # Paramètres de recherche Archive.org
                params = {
                    'q': f'{keyword} AND mediatype:audio',
                    'fl[]': ['identifier', 'title', 'creator', 'date', 'downloads'],
                    'sort[]': 'downloads desc',
                    'rows': max_results,
                    'page': 1,
                    'output': 'json'
                }

                print(f"🔍 Recherche: '{keyword}'", end=' ')
                response = requests.get(
                    self.search_url, 
                    params=params, 
                    headers=self.headers, 
                    timeout=15
                )
                response.raise_for_status()

                data = response.json()

                if 'response' in data and 'docs' in data['response']:
                    docs = data['response']['docs'][:max_results]
                    print(f"→ {len(docs)} résultats")
                    
                    for doc in docs:
                        try:
                            track_info = self._process_item(doc, keyword)
                            if track_info:
                                all_tracks.append(track_info)
                        except Exception as e:
                            print(f"⚠️ Erreur item: {e}")
                            continue
                else:
                    print("→ 0 résultats")

                # Délai pour être respectueux du serveur
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"❌ Erreur réseau pour '{keyword}': {e}")
                continue
            except Exception as e:
                print(f"⚠️ Erreur pour '{keyword}': {e}")
                continue

        return all_tracks

    def _process_item(self, doc: Dict, keyword: str) -> Optional[Dict]:
        """
        Traite un item de résultat Archive.org et extrait les infos
        """
        try:
            identifier = doc.get('identifier', '')
            if not identifier:
                return None

            title = doc.get('title', 'Unknown')
            creator = doc.get('creator', 'Unknown Artist')

            # Gestion des listes
            if isinstance(title, list):
                title = title[0] if title else 'Unknown'
            if isinstance(creator, list):
                creator = creator[0] if creator else 'Unknown Artist'

            return {
                'identifier': identifier,
                'title': title,
                'artist': creator,
                'creator': creator,  # Ajouter aussi 'creator' pour compatibilité
                'duration': 'N/A',
                'keyword': keyword
            }

        except Exception as e:
            print(f"⚠️ Erreur extraction: {e}")
            return None

    def fetch_duration(self, track: Dict) -> Dict:
        """
        Récupère la durée réelle d'une piste depuis les métadonnées
        """
        try:
            identifier = track['identifier']
            metadata_url = f"{self.base_url}/metadata/{identifier}"
            
            response = requests.get(metadata_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            metadata = response.json()
            
            # Chercher les fichiers audio
            files = metadata.get('files', [])
            audio_files = [
                f for f in files 
                if f.get('format', '').lower() in ['mp3', 'ogg', 'vorbis', 'flac']
            ]
            
            if audio_files:
                # Prendre le premier MP3 ou le premier fichier audio
                audio_file = next(
                    (f for f in audio_files if f.get('format', '').lower() == 'mp3'),
                    audio_files[0]
                )
                
                # Récupérer la durée
                length = audio_file.get('length')
                if length:
                    # Convertir en format MM:SS
                    try:
                        seconds = float(length)
                        minutes = int(seconds // 60)
                        secs = int(seconds % 60)
                        track['duration'] = f"{minutes}:{secs:02d}"
                    except:
                        track['duration'] = str(length)
            
            return track
            
        except Exception as e:
            # En cas d'erreur, on garde 'N/A'
            return track

    def enrich_with_durations(self, tracks: List[Dict], max_workers: int = 5) -> List[Dict]:
        """
        Enrichit les pistes avec leurs durées en parallèle
        """
        print("\n   📊 Récupération des durées...", end=' ')
        
        enriched_tracks = []
        
        # Traitement parallèle pour aller plus vite
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.fetch_duration, track): track for track in tracks}
            
            for future in as_completed(futures):
                try:
                    enriched_track = future.result()
                    enriched_tracks.append(enriched_track)
                except Exception as e:
                    # Si erreur, on garde la piste sans durée
                    enriched_tracks.append(futures[future])
        
        print("✓")
        return enriched_tracks

    def scrape_all_categories(
        self, 
        tracks_per_category: int = 10,
        fetch_durations: bool = True
    ) -> Dict:
        """
        Scrape toutes les catégories de sport
        """
        all_data = {}

        for category, keywords in self.sport_categories.items():
            print(f"\n{'=' * 60}")
            print(f"📂 Catégorie: {category.upper().replace('_', ' ')}")
            print(f"{'=' * 60}")

            # Recherche des pistes
            tracks = self.search_music(keywords, max_results=tracks_per_category)

            # Déduplique par identifier
            unique_tracks = []
            seen_ids = set()
            for track in tracks:
                if track['identifier'] not in seen_ids:
                    unique_tracks.append(track)
                    seen_ids.add(track['identifier'])

            # Enrichissement avec les durées
            if fetch_durations and unique_tracks:
                unique_tracks = self.enrich_with_durations(unique_tracks)

            all_data[category] = unique_tracks
            print(f"  ✅ {len(unique_tracks)} pistes trouvées\n")

            # Pause entre catégories
            time.sleep(2)

        return all_data

    def save_to_json(self, data: Dict, filename: str = None):
        """Sauvegarde les données dans un fichier JSON"""
        if filename is None:
            # Détection automatique du chemin correct
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Si on est dans app/tools/, remonter de 2 niveaux vers backend/
            if 'app' in current_dir and 'tools' in current_dir:
                base_dir = os.path.dirname(os.path.dirname(current_dir))
            else:
                # Sinon on est déjà dans backend/
                base_dir = current_dir
            
            # Créer le dossier data/ s'il n'existe pas
            data_dir = os.path.join(base_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            
            filename = os.path.join(data_dir, "archive_music_data.json")
        
        # Sauvegarder
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Données sauvegardées dans: {filename}")
        print(f"📁 Taille du fichier: {os.path.getsize(filename) / 1024:.1f} KB")


def main():
    """Fonction principale pour lancer le scraping"""
    print("🎵 " + "=" * 58)
    print("   SCRAPER ARCHIVE.ORG - Musiques Sport & Fitness")
    print("=" * 62 + "\n")

    scraper = ArchiveMusicScraper()

    print("🚀 Démarrage du scraping complet (avec durées)...\n")

    # Scrape toutes les catégories avec durées
    music_data = scraper.scrape_all_categories(
        tracks_per_category=10,
        fetch_durations=True
    )

    # Sauvegarde en JSON
    scraper.save_to_json(music_data)

    # Affiche un résumé
    print("\n" + "=" * 62)
    print("📊 RÉSUMÉ FINAL:")
    print("=" * 62)
    total_tracks = sum(len(tracks) for tracks in music_data.values())
    print(f"🎵 Total de pistes: {total_tracks}")
    print()
    
    for category, tracks in music_data.items():
        category_name = category.replace('_', ' ').title()
        print(f"  {category_name:25} : {len(tracks):3} pistes")
    print("=" * 62)

    # Affiche quelques exemples
    if total_tracks > 0:
        print("\n💿 Exemples de pistes trouvées:")
        print("-" * 62)
        for category, tracks in list(music_data.items())[:2]:
            if tracks:
                print(f"\n{category.replace('_', ' ').upper()}:")
                for track in tracks[:3]:
                    duration = track.get('duration', 'N/A')
                    print(f"   • {track['title']} - {track['artist']} ({duration})")
        print("-" * 62)
    
    print("\n✅ Scraping terminé avec succès !\n")


if __name__ == "__main__":
    main()

