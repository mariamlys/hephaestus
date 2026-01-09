#!/usr/bin/env python3
"""
Scraper pour Pixabay Music - Musiques par catégorie de sport
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict
import re

class PixabayMusicScraper:
    """Scraper pour récupérer les musiques de Pixabay par catégorie"""
    
    def __init__(self):
        self.base_url = "https://pixabay.com/fr/music/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Catégories de sport à scraper
        self.sport_categories = {
            "course_a_pied": ["running", "jogging", "cardio", "energetic"],
            "echauffement": ["warm up", "light", "gentle"],
            "boxe": ["boxing", "intense", "aggressive", "power"],
            "marche_a_pied": ["walking", "calm", "relaxing"],
            "musculation": ["workout", "gym", "training", "motivation"]
        }
    
    def search_music(self, keywords: List[str], max_results: int = 20) -> List[Dict]:
        """
        Cherche des musiques sur Pixabay selon des mots-clés
        
        Args:
            keywords: Liste de mots-clés à chercher
            max_results: Nombre maximum de résultats
            
        Returns:
            Liste de dictionnaires contenant les infos des musiques
        """
        all_tracks = []
        
        for keyword in keywords:
            try:
                # URL de recherche
                search_url = f"{self.base_url}search/{keyword}/"
                
                print(f"Scraping: {search_url}")
                response = requests.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Trouver les éléments de musique (adapte les sélecteurs selon la structure réelle)
                music_items = soup.find_all('div', class_='item')
                
                for item in music_items[:max_results]:
                    try:
                        track_info = self._extract_track_info(item)
                        if track_info:
                            track_info['keyword'] = keyword
                            all_tracks.append(track_info)
                    except Exception as e:
                        print(f"Erreur extraction track: {e}")
                        continue
                
                # Délai pour éviter de surcharger le serveur
                time.sleep(2)
                
            except Exception as e:
                print(f"Erreur scraping {keyword}: {e}")
                continue
        
        return all_tracks
    
    def _extract_track_info(self, item) -> Dict:
        """
        Extrait les informations d'une piste depuis un élément HTML
        
        Note: Les sélecteurs CSS doivent être adaptés selon la structure réelle de Pixabay
        """
        try:
            # À ADAPTER selon la structure HTML réelle de Pixabay
            title = item.find('h2')
            title = title.text.strip() if title else "Unknown"
            
            # Durée
            duration = item.find('span', class_='duration')
            duration = duration.text.strip() if duration else "0:00"
            
            # Artiste/Auteur
            artist = item.find('a', class_='author')
            artist = artist.text.strip() if artist else "Unknown"
            
            # Lien de téléchargement (cherche un lien avec .mp3)
            download_link = item.find('a', href=re.compile(r'\.mp3'))
            download_url = download_link['href'] if download_link else None
            
            # URL de la page
            page_link = item.find('a', class_='link')
            page_url = page_link['href'] if page_link else None
            if page_url and not page_url.startswith('http'):
                page_url = f"https://pixabay.com{page_url}"
            
            # Tags/genres
            tags = []
            tag_elements = item.find_all('a', class_='tag')
            for tag in tag_elements:
                tags.append(tag.text.strip())
            
            return {
                'title': title,
                'artist': artist,
                'duration': duration,
                'download_url': download_url,
                'page_url': page_url,
                'tags': tags
            }
            
        except Exception as e:
            print(f"Erreur extraction: {e}")
            return None
    
    def scrape_all_categories(self, tracks_per_category: int = 15) -> Dict:
        """
        Scrape toutes les catégories de sport
        
        Returns:
            Dictionnaire avec les musiques par catégorie
        """
        all_data = {}
        
        for category, keywords in self.sport_categories.items():
            print(f"\n=== Scraping catégorie: {category} ===")
            tracks = self.search_music(keywords, max_results=tracks_per_category)
            
            # Déduplique par titre
            unique_tracks = []
            seen_titles = set()
            for track in tracks:
                if track['title'] not in seen_titles:
                    unique_tracks.append(track)
                    seen_titles.add(track['title'])
            
            all_data[category] = unique_tracks
            print(f"✅ {len(unique_tracks)} morceaux trouvés pour {category}")
        
        return all_data
    
    def save_to_json(self, data: Dict, filename: str = "pixabay_music_data.json"):
        """Sauvegarde les données dans un fichier JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Données sauvegardées dans {filename}")


def main():
    """Fonction principale pour lancer le scraping"""
    scraper = PixabayMusicScraper()
    
    print("🎵 Démarrage du scraping Pixabay Music...")
    print("=" * 50)
    
    # Scrape toutes les catégories
    music_data = scraper.scrape_all_categories(tracks_per_category=15)
    
    # Sauvegarde en JSON
    scraper.save_to_json(music_data)
    
    # Affiche un résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ:")
    total_tracks = sum(len(tracks) for tracks in music_data.values())
    print(f"Total de pistes: {total_tracks}")
    for category, tracks in music_data.items():
        print(f"  - {category}: {len(tracks)} pistes")


if __name__ == "__main__":
    main()
