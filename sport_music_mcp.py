#!/usr/bin/env python3
"""
MCP Server pour Chatbot Sport & Musique
Utilise les données scrapées de Pixabay Music
"""

import asyncio
import json
from typing import List, Dict, Optional
import random

class SportMusicMCPServer:
    """Serveur MCP pour recommandations musique/sport"""
    
    def __init__(self, data_file: str = "pixabay_music_data.json"):
        self.data_file = data_file
        self.music_data = self._load_music_data()
        
        # Mapping sport -> BPM recommandés
        self.sport_bpm = {
            "course_a_pied": {"min": 140, "max": 180, "desc": "Rythme soutenu pour la course"},
            "echauffement": {"min": 100, "max": 130, "desc": "Tempo doux pour l'échauffement"},
            "boxe": {"min": 150, "max": 190, "desc": "Rythme intense pour la boxe"},
            "marche_a_pied": {"min": 90, "max": 120, "desc": "Tempo calme pour la marche"},
            "musculation": {"min": 120, "max": 160, "desc": "Rythme motivant pour la muscu"}
        }
        
        # Outils disponibles
        self.tools = {
            "create_playlist": self.create_playlist,
            "get_sport_info": self.get_sport_info,
            "search_music": self.search_music,
            "list_categories": self.list_categories,
            "get_random_track": self.get_random_track
        }
    
    def _load_music_data(self) -> Dict:
        """Charge les données musicales depuis le JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Fichier {self.data_file} non trouvé. Utilisation de données vides.")
            return {
                "course_a_pied": [],
                "echauffement": [],
                "boxe": [],
                "marche_a_pied": [],
                "musculation": []
            }
    
    def _parse_duration(self, duration_str: str) -> int:
        """Convertit une durée "3:45" en secondes"""
        try:
            parts = duration_str.split(':')
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            return 0
        except:
            return 180  # Durée par défaut: 3 minutes
    
    async def create_playlist(self, sport: str, duration_minutes: int = 60) -> dict:
        """
        Crée une playlist pour un sport donné et une durée cible
        
        Args:
            sport: Type de sport (course_a_pied, boxe, etc.)
            duration_minutes: Durée souhaitée en minutes
        """
        # Normalise le nom du sport
        sport = sport.lower().replace(" ", "_").replace("à", "a")
        
        if sport not in self.music_data:
            available = ", ".join(self.music_data.keys())
            return {
                "error": f"Sport '{sport}' non trouvé. Disponibles: {available}"
            }
        
        tracks = self.music_data[sport]
        
        if not tracks:
            return {
                "error": f"Aucune musique disponible pour {sport}. Lance d'abord le scraper!"
            }
        
        # Sélectionne des pistes aléatoires jusqu'à atteindre la durée
        target_seconds = duration_minutes * 60
        playlist = []
        total_duration = 0
        available_tracks = tracks.copy()
        random.shuffle(available_tracks)
        
        for track in available_tracks:
            if total_duration >= target_seconds:
                break
            
            track_seconds = self._parse_duration(track.get('duration', '3:00'))
            playlist.append(track)
            total_duration += track_seconds
        
        # Infos BPM pour ce sport
        bpm_info = self.sport_bpm.get(sport, {})
        
        return {
            "sport": sport,
            "target_duration_min": duration_minutes,
            "actual_duration_min": round(total_duration / 60, 1),
            "track_count": len(playlist),
            "bpm_range": f"{bpm_info.get('min', 'N/A')}-{bpm_info.get('max', 'N/A')} BPM",
            "recommendation": bpm_info.get('desc', ''),
            "playlist": playlist
        }
    
    async def get_sport_info(self, sport: str) -> dict:
        """Récupère les infos (BPM, description) pour un sport"""
        sport = sport.lower().replace(" ", "_").replace("à", "a")
        
        if sport not in self.sport_bpm:
            return {"error": f"Sport '{sport}' non reconnu"}
        
        info = self.sport_bpm[sport]
        track_count = len(self.music_data.get(sport, []))
        
        return {
            "sport": sport,
            "bpm_min": info['min'],
            "bpm_max": info['max'],
            "description": info['desc'],
            "available_tracks": track_count
        }
    
    async def search_music(self, keyword: str, sport: Optional[str] = None) -> dict:
        """Cherche des musiques par mot-clé"""
        results = []
        
        categories_to_search = [sport] if sport else self.music_data.keys()
        
        for category in categories_to_search:
            if category not in self.music_data:
                continue
            
            for track in self.music_data[category]:
                # Cherche dans le titre, artiste et tags
                if (keyword.lower() in track.get('title', '').lower() or
                    keyword.lower() in track.get('artist', '').lower() or
                    any(keyword.lower() in tag.lower() for tag in track.get('tags', []))):
                    
                    track_copy = track.copy()
                    track_copy['category'] = category
                    results.append(track_copy)
        
        return {
            "keyword": keyword,
            "results_count": len(results),
            "tracks": results[:20]  # Limite à 20 résultats
        }
    
    async def list_categories(self) -> dict:
        """Liste toutes les catégories disponibles"""
        categories = []
        
        for cat_name, tracks in self.music_data.items():
            categories.append({
                "name": cat_name,
                "track_count": len(tracks),
                "bpm_info": self.sport_bpm.get(cat_name, {})
            })
        
        return {"categories": categories}
    
    async def get_random_track(self, sport: str) -> dict:
        """Récupère une piste aléatoire pour un sport"""
        sport = sport.lower().replace(" ", "_").replace("à", "a")
        
        if sport not in self.music_data or not self.music_data[sport]:
            return {"error": f"Pas de musique disponible pour {sport}"}
        
        track = random.choice(self.music_data[sport])
        return {
            "sport": sport,
            "track": track
        }
    
    async def handle_request(self, request: dict) -> dict:
        """Traite une requête MCP"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "sport-music-mcp",
                    "version": "1.0.0"
                }
            }
        
        elif method == "tools/list":
            return {
                "tools": [
                    {
                        "name": "create_playlist",
                        "description": "Crée une playlist personnalisée pour un sport (ex: course à pied, boxe)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "sport": {
                                    "type": "string",
                                    "description": "Type de sport (course_a_pied, boxe, musculation, marche_a_pied, echauffement)"
                                },
                                "duration_minutes": {
                                    "type": "integer",
                                    "description": "Durée souhaitée en minutes",
                                    "default": 60
                                }
                            },
                            "required": ["sport"]
                        }
                    },
                    {
                        "name": "get_sport_info",
                        "description": "Récupère les infos (BPM recommandé, description) pour un sport",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "sport": {"type": "string"}
                            },
                            "required": ["sport"]
                        }
                    },
                    {
                        "name": "search_music",
                        "description": "Cherche des musiques par mot-clé",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "keyword": {"type": "string"},
                                "sport": {"type": "string"}
                            },
                            "required": ["keyword"]
                        }
                    },
                    {
                        "name": "list_categories",
                        "description": "Liste toutes les catégories de sport disponibles",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "get_random_track",
                        "description": "Récupère une piste aléatoire pour un sport",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "sport": {"type": "string"}
                            },
                            "required": ["sport"]
                        }
                    }
                ]
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name in self.tools:
                try:
                    result = await self.tools[tool_name](**tool_args)
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                except Exception as e:
                    return {"error": f"Erreur dans {tool_name}: {str(e)}"}
            else:
                return {"error": f"Outil inconnu: {tool_name}"}
        
        return {"error": "Méthode non supportée"}
    
    async def run_stdio(self):
        """Lance le serveur en mode stdio (entrée/sortie standard)"""
        print("🎵 Serveur MCP Sport & Musique démarré!", flush=True)
        print(f"📁 Fichier de données: {self.data_file}", flush=True)
        print(f"🎯 Catégories chargées: {', '.join(self.music_data.keys())}", flush=True)
        
        total_tracks = sum(len(tracks) for tracks in self.music_data.values())
        print(f"🎼 Total de pistes: {total_tracks}\n", flush=True)
        
        while True:
            try:
                line = input("Requête JSON (ou 'quit'): ")
                if line.lower() == 'quit':
                    break
                
                request = json.loads(line)
                response = await self.handle_request(request)
                print(json.dumps(response, ensure_ascii=False, indent=2))
                
            except json.JSONDecodeError:
                print(json.dumps({"error": "JSON invalide"}))
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(json.dumps({"error": str(e)}))


async def main():
    server = SportMusicMCPServer()
    await server.run_stdio()


if __name__ == "__main__":
    asyncio.run(main())
