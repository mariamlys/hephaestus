#!/usr/bin/env python3
"""
Scraper Archive.org V3 - Mots-clés musicaux précis
==================================================
Utilise des genres et artistes spécifiques pour chaque sport
"""

import requests
import json
import time
import os
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class ArchiveMusicScraper:

    def __init__(self):
        self.base_url = "https://archive.org"
        self.search_url = "https://archive.org/advancedsearch.php"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        self.sport_categories = {
            "course_a_pied": [
                "uplifting trance", "progressive house", "big room",
                "energetic techno", "festival edm", "upbeat electronic"
            ],
            "echauffement": [
                "ambient meditation", "chillout lounge", "soft piano",
                "relaxing acoustic", "calm instrumental", "yoga music"
            ],
            "boxe": [
                "aggressive hip hop", "hard rock anthems", "metal workout",
                "trap beats", "hardcore punk", "intense drum and bass"
            ],
            "marche_a_pied": [
                "indie folk acoustic", "light jazz", "easy listening",
                "soft pop", "acoustic guitar instrumental", "bossa nova"
            ],
            "musculation": [
                "gym motivation music", "workout rock", "powerful metal",
                "epic orchestral", "heavy bass trap", "motivational rap"
            ]
        }
        
        self.MIN_DURATION = 120
        self.MAX_DURATION = 420

    def search_music(self, keywords: List[str], max_results: int = 15) -> List[Dict]:
        """Cherche des collections musicales"""
        all_items = []

        for keyword in keywords:
            try:
                params = {
                    'q': f'({keyword}) AND mediatype:audio AND subject:(music OR electronic OR rock OR hip-hop)',
                    'fl[]': ['identifier', 'title', 'creator', 'downloads', 'subject'],
                    'sort[]': 'downloads desc',
                    'rows': max_results,
                    'output': 'json'
                }

                print(f"  🔍 '{keyword}'", end=' ')
                response = requests.get(
                    self.search_url, 
                    params=params, 
                    headers=self.headers, 
                    timeout=15
                )
                response.raise_for_status()

                data = response.json()

                if 'response' in data and 'docs' in data['response']:
                    docs = data['response']['docs']
                    print(f"→ {len(docs)} collections")
                    
                    for doc in docs:
                        identifier = doc.get('identifier')
                        if identifier:
                            all_items.append({
                                'identifier': identifier,
                                'title': doc.get('title', 'Unknown'),
                                'creator': doc.get('creator', ['Unknown'])[0] if isinstance(doc.get('creator'), list) else doc.get('creator', 'Unknown'),
                                'keyword': keyword
                            })
                else:
                    print("→ 0")

                time.sleep(0.3)

            except Exception as e:
                print(f"❌ {e}")
                continue

        return all_items

    def extract_tracks_from_collection(self, item: Dict, sport_key: str) -> List[Dict]:
        """
        Extrait les pistes individuelles
        """
        try:
            identifier = item['identifier']
            metadata_url = f"{self.base_url}/metadata/{identifier}"
            
            response = requests.get(metadata_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            metadata = response.json()
            files = metadata.get('files', [])
            
            audio_files = [
                f for f in files 
                if f.get('format', '').lower() in ['mp3', '128kb mp3', 'vbr mp3', 'ogg vorbis']
            ]
            
            tracks = []
            
            for audio_file in audio_files:
                length = audio_file.get('length')
                if not length:
                    continue
                
                try:
                    duration_seconds = float(length)
                except:
                    continue
                
                if sport_key in ['musculation', 'boxe']:
                    if duration_seconds < self.MIN_DURATION or duration_seconds > 420:
                        continue
                else:
                    if duration_seconds < self.MIN_DURATION or duration_seconds > 360:
                        continue
                
                minutes = int(duration_seconds // 60)
                seconds = int(duration_seconds % 60)
                duration_formatted = f"{minutes}:{seconds:02d}"
                
                filename = audio_file.get('name', '')
                
                track_title = filename.replace('.mp3', '').replace('.ogg', '')
                track_title = track_title.replace('_', ' ').replace('-', ' ')
                track_title = ' '.join(track_title.split())
                
                if not track_title or len(track_title) < 3:
                    track_title = item['title']
                
                file_url = f"https://archive.org/download/{identifier}/{filename.replace(' ', '%20')}"
                
                tracks.append({
                    'identifier': f"{identifier}_{filename}",
                    'collection_id': identifier,
                    'title': track_title[:80],
                    'artist': item['creator'][:50] if item['creator'] else 'Unknown Artist',
                    'duration': duration_formatted,
                    'duration_seconds': duration_seconds,
                    'keyword': item['keyword'],
                    'preview_url': f"https://archive.org/details/{identifier}",
                    'stream_url': file_url,
                    'format': audio_file.get('format', 'mp3')
                })
            
            return tracks
            
        except Exception as e:
            return []

    def scrape_category(self, category: str, keywords: List[str], target_tracks: int = 25) -> List[Dict]:
        """Scrape une catégorie avec les nouveaux mots-clés"""
        print(f"\n{'=' * 70}")
        print(f"📂 {category.upper().replace('_', ' ')}")
        print(f"{'=' * 70}")
        
        collections = self.search_music(keywords, max_results=10)
        
        if not collections:
            print(f"  ❌ Aucune collection")
            return []
        
        all_tracks = []
        print(f"\n  🎵 Extraction des pistes...")
        
        for item in collections:
            if len(all_tracks) >= target_tracks:
                break
            
            print(f"     • {item['title'][:45]}...", end=' ')
            tracks = self.extract_tracks_from_collection(item, category)
            
            if tracks:
                print(f"✓ {len(tracks)}")
                all_tracks.extend(tracks)
            else:
                print("✗")
            
            time.sleep(0.3)
        
        seen_titles = set()
        unique_tracks = []
        
        for track in all_tracks:
            title_key = f"{track['title'].lower()[:40]}_{track['duration']}"
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_tracks.append(track)
                
                if len(unique_tracks) >= target_tracks:
                    break
        
        print(f"\n  ✅ {len(unique_tracks)} pistes extraites")
        
        if unique_tracks:
            print(f"\n  📊 Échantillon:")
            for track in unique_tracks[:4]:
                print(f"     • {track['title'][:40]} - {track['artist'][:25]} ({track['duration']})")
        
        return unique_tracks

    def scrape_all_categories(self, tracks_per_category: int = 25) -> Dict:
        """Scrape toutes les catégories"""
        all_data = {}

        for category, keywords in self.sport_categories.items():
            tracks = self.scrape_category(category, keywords, tracks_per_category)
            all_data[category] = tracks
            time.sleep(1.5)

        return all_data

    def save_to_json(self, data: Dict, filename: str = None):
        """Sauvegarde les données"""
        if filename is None:
            if os.path.exists('data'):
                filename = 'data/archive_music_data.json'
            elif os.path.exists('../data'):
                filename = '../data/archive_music_data.json'
            else:
                filename = 'archive_music_data.json'
        
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Sauvegardé: {os.path.abspath(filename)}")
        print(f"📦 Taille: {os.path.getsize(filename) / 1024:.1f} KB")


def main():
    print("\n" + "🎵 " + "=" * 68)
    print("   SCRAPER V3 - Mots-clés musicaux PRÉCIS")
    print("=" * 72 + "\n")

    scraper = ArchiveMusicScraper()

    print("🚀 Démarrage du scraping avec mots-clés optimisés...\n")
    print("ℹ️  Genres musicaux spécifiques par sport")
    print("ℹ️  Filtrage intelligent des durées\n")

    music_data = scraper.scrape_all_categories(tracks_per_category=25)

    scraper.save_to_json(music_data)

    print("\n" + "=" * 72)
    print("📊 RÉSUMÉ FINAL:")
    print("=" * 72)
    
    total_tracks = sum(len(tracks) for tracks in music_data.values())
    total_duration = sum(
        sum(t.get('duration_seconds', 0) for t in tracks) 
        for tracks in music_data.values()
    )
    
    print(f"   🎵 Total: {total_tracks} pistes")
    print(f"   ⏱️  Durée: {int(total_duration / 60)} min\n")
    
    for category, tracks in music_data.items():
        if tracks:
            avg_duration = sum(t.get('duration_seconds', 0) for t in tracks) / len(tracks)
            category_name = category.replace('_', ' ').title()
            print(f"   {category_name:25} : {len(tracks):2} pistes (moy: {int(avg_duration)}s)")
    
    print("=" * 72)
    
    print("\n📝 EXEMPLES PAR CATÉGORIE:")
    print("-" * 72)
    for category, tracks in music_data.items():
        if tracks:
            print(f"\n   {category.replace('_', ' ').upper()}:")
            for track in tracks[:2]:
                print(f"   • {track['title'][:45]} ({track['duration']})")
    print("-" * 72)
    
    print("\n✅ Scraping terminé !")
    print("💡 Musique maintenant adaptée aux sports\n")


if __name__ == "__main__":
    main()