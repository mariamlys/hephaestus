#!/usr/bin/env python3
"""
MCP Server pour Chatbot Sport & Musique

"""

import asyncio
import json
from typing import List, Dict, Optional
import random
import os


class SportMusicMCPServer:
    """Serveur MCP pour recommandations musique/sport"""
    
    def __init__(self, data_file: str = "archive_music_data.json"):
        self.data_file = data_file
        self.music_data = self._load_music_data()
        
        # BPM recommandés et descriptions
        self.sport_bpm = {
            "course_a_pied": {
                "min": 140, 
                "max": 180, 
                "desc": "Rythme soutenu pour la course à pied"
            },
            "echauffement": {
                "min": 100, 
                "max": 130, 
                "desc": "Tempo doux pour l'échauffement et les étirements"
            },
            "boxe": {
                "min": 150, 
                "max": 190, 
                "desc": "Rythme intense et agressif pour la boxe"
            },
            "marche_a_pied": {
                "min": 90, 
                "max": 120, 
                "desc": "Tempo calme et relaxant pour la marche"
            },
            "musculation": {
                "min": 120, 
                "max": 160, 
                "desc": "Rythme motivant pour la musculation et le fitness"
            }
        }
        
        # Outils 
        self.tools = {
            "create_playlist": self.create_playlist,
            "get_sport_info": self.get_sport_info,
            "search_music": self.search_music,
            "list_categories": self.list_categories,
            "get_random_track": self.get_random_track,
            "get_track_details": self.get_track_details
        }
    
    def _load_music_data(self) -> Dict:
        """Charge les données musicales depuis le JSON"""
        try:
            if not os.path.exists(self.data_file):
                print(f"Fichier {self.data_file} non trouvé.")
                print(f"Lance d'abord: python archive_scraper.py")
                return self._get_empty_categories()
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Valider que les données ont la bonne structure
            if not isinstance(data, dict):
                print("Format de données invalide.")
                return self._get_empty_categories()
                
            return data
            
        except json.JSONDecodeError:
            print(f"Erreur de lecture du fichier {self.data_file}")
            return self._get_empty_categories()
        except Exception as e:
            print(f"Erreur: {e}")
            return self._get_empty_categories()
    
    def _get_empty_categories(self) -> Dict:
        """Retourne une structure vide pour toutes les catégories"""
        return {
            "course_a_pied": [],
            "echauffement": [],
            "boxe": [],
            "marche_a_pied": [],
            "musculation": []
        }
    
    def _parse_duration(self, duration_str: str) -> int:
        """
        Convertit une durée "3:45" ou "3.5" en secondes
        """
        try:
            if ':' in str(duration_str):
                parts = str(duration_str).split(':')
                if len(parts) == 2:
                    return int(parts[0]) * 60 + int(parts[1])
            else:
                # Si c'est juste un nombre
                return int(float(duration_str))
        except:
            pass
        
        return 180  # Durée par défaut: 3 minutes
    
    def _format_duration(self, seconds: int) -> str:
        """Convertit des secondes en format MM:SS"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"
    
    async def create_playlist(
        self, 
        sport: str, 
        duration_minutes: int = 60,
        shuffle: bool = True
    ) -> dict:
        """
        Crée une playlist personnalisée pour un sport donné
        
    
        """
        # Normalise le nom du sport
        sport = sport.lower().replace(" ", "_").replace("à", "a").replace("é", "e")
        
        if sport not in self.music_data:
            available = ", ".join(self.music_data.keys())
            return {
                "error": f"Sport '{sport}' non trouvé. Disponibles: {available}"
            }
        
        tracks = self.music_data[sport]
        
        if not tracks:
            return {
                "error": f"Aucune musique disponible pour {sport}. Lance d'abord: python archive_scraper.py"
            }
        
        # Sélectionne des pistes jusqu'à atteindre la durée cible
        target_seconds = duration_minutes * 60
        playlist = []
        total_duration = 0
        available_tracks = tracks.copy()
        
        if shuffle:
            random.shuffle(available_tracks)
        
        for track in available_tracks:
            if total_duration >= target_seconds:
                break
            
            track_seconds = self._parse_duration(track.get('duration', '3:00'))
            playlist.append(track)
            total_duration += track_seconds
        
        # Si pas assez de pistes, on boucle
        if playlist and total_duration < target_seconds:
            while total_duration < target_seconds:
                for track in available_tracks:
                    if total_duration >= target_seconds:
                        break
                    track_seconds = self._parse_duration(track.get('duration', '3:00'))
                    playlist.append(track)
                    total_duration += track_seconds
        
        # Infos BPM pour ce sport
        bpm_info = self.sport_bpm.get(sport, {})
        
        return {
            "success": True,
            "sport": sport,
            "target_duration_min": duration_minutes,
            "actual_duration_min": round(total_duration / 60, 1),
            "actual_duration_formatted": self._format_duration(total_duration),
            "track_count": len(playlist),
            "unique_tracks": len(set(t['identifier'] for t in playlist)),
            "bpm_range": f"{bpm_info.get('min', 'N/A')}-{bpm_info.get('max', 'N/A')} BPM",
            "recommendation": bpm_info.get('desc', ''),
            "playlist": playlist
        }
    
    async def get_sport_info(self, sport: str) -> dict:
        """Récupère les informations complètes sur un sport"""
        sport = sport.lower().replace(" ", "_").replace("à", "a").replace("é", "e")
        
        if sport not in self.sport_bpm:
            return {"error": f"Sport '{sport}' non reconnu"}
        
        info = self.sport_bpm[sport]
        track_count = len(self.music_data.get(sport, []))
        
        return {
            "success": True,
            "sport": sport,
            "bpm_min": info['min'],
            "bpm_max": info['max'],
            "description": info['desc'],
            "available_tracks": track_count,
            "has_tracks": track_count > 0
        }
    
    async def search_music(
        self, 
        keyword: str, 
        sport: Optional[str] = None,
        limit: int = 20
    ) -> dict:
        """
        Cherche des musiques par mot-clé
        
        """
        results = []
        
        categories_to_search = [sport] if sport else self.music_data.keys()
        
        for category in categories_to_search:
            if category not in self.music_data:
                continue
            
            for track in self.music_data[category]:
                # Cherche dans le titre, artiste et keyword
                keyword_lower = keyword.lower()
                if (keyword_lower in track.get('title', '').lower() or
                    keyword_lower in track.get('artist', '').lower() or
                    keyword_lower in track.get('keyword', '').lower()):
                    
                    track_copy = track.copy()
                    track_copy['category'] = category
                    results.append(track_copy)
        
        return {
            "success": True,
            "keyword": keyword,
            "results_count": len(results),
            "showing": min(len(results), limit),
            "tracks": results[:limit]
        }
    
    async def list_categories(self) -> dict:
        """Liste toutes les catégories de sport disponibles"""
        categories = []
        
        for cat_name, tracks in self.music_data.items():
            bpm_info = self.sport_bpm.get(cat_name, {})
            categories.append({
                "name": cat_name,
                "track_count": len(tracks),
                "bpm_min": bpm_info.get('min', 'N/A'),
                "bpm_max": bpm_info.get('max', 'N/A'),
                "description": bpm_info.get('desc', ''),
                "has_tracks": len(tracks) > 0
            })
        
        total_tracks = sum(len(tracks) for tracks in self.music_data.values())
        
        return {
            "success": True,
            "total_categories": len(categories),
            "total_tracks": total_tracks,
            "categories": categories
        }
    
    async def get_random_track(self, sport: str) -> dict:
        """Récupère une piste aléatoire pour un sport"""
        sport = sport.lower().replace(" ", "_").replace("à", "a").replace("é", "e")
        
        if sport not in self.music_data or not self.music_data[sport]:
            return {
                "error": f"Pas de musique disponible pour {sport}"
            }
        
        track = random.choice(self.music_data[sport])
        
        return {
            "success": True,
            "sport": sport,
            "track": track
        }
    
    async def get_track_details(self, identifier: str) -> dict:
        """Récupère les détails complets d'une piste"""
        for category, tracks in self.music_data.items():
            for track in tracks:
                if track.get('identifier') == identifier:
                    bpm_info = self.sport_bpm.get(category, {})
                    return {
                        "success": True,
                        "track": track,
                        "category": category,
                        "bpm_recommendation": f"{bpm_info.get('min', 'N/A')}-{bpm_info.get('max', 'N/A')} BPM"
                    }
        
        return {
            "error": f"Piste avec identifier '{identifier}' non trouvée"
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
                    "name": "sport-music-mcp-archive",
                    "version": "2.0.0",
                    "source": "archive.org"
                }
            }
        
        elif method == "tools/list":
            return {
                "tools": [
                    {
                        "name": "create_playlist",
                        "description": "Crée une playlist personnalisée pour un sport (course à pied, boxe, musculation, etc.)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "sport": {
                                    "type": "string",
                                    "description": "Type de sport: course_a_pied, boxe, musculation, marche_a_pied, echauffement"
                                },
                                "duration_minutes": {
                                    "type": "integer",
                                    "description": "Durée souhaitée en minutes",
                                    "default": 60
                                },
                                "shuffle": {
                                    "type": "boolean",
                                    "description": "Mélanger les pistes aléatoirement",
                                    "default": True
                                }
                            },
                            "required": ["sport"]
                        }
                    },
                    {
                        "name": "get_sport_info",
                        "description": "Récupère les infos complètes (BPM, description) pour un sport",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "sport": {"type": "string", "description": "Type de sport"}
                            },
                            "required": ["sport"]
                        }
                    },
                    {
                        "name": "search_music",
                        "description": "Cherche des musiques par mot-clé dans toutes les catégories",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "keyword": {"type": "string", "description": "Mot-clé à rechercher"},
                                "sport": {"type": "string", "description": "Catégorie optionnelle"},
                                "limit": {"type": "integer", "description": "Nombre max de résultats", "default": 20}
                            },
                            "required": ["keyword"]
                        }
                    },
                    {
                        "name": "list_categories",
                        "description": "Liste toutes les catégories de sport disponibles avec statistiques",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "get_random_track",
                        "description": "Récupère une piste aléatoire pour un sport donné",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "sport": {"type": "string", "description": "Type de sport"}
                            },
                            "required": ["sport"]
                        }
                    },
                    {
                        "name": "get_track_details",
                        "description": "Récupère les détails complets d'une piste via son identifier",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "identifier": {"type": "string", "description": "Identifier Archive.org de la piste"}
                            },
                            "required": ["identifier"]
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
                    return {
                        "error": f"Erreur dans {tool_name}: {str(e)}",
                        "tool": tool_name,
                        "arguments": tool_args
                    }
            else:
                return {"error": f"Outil inconnu: {tool_name}"}
        
        return {"error": "Méthode non supportée"}
    
    async def run_stdio(self):
        """Lance le serveur en mode stdio (entrée/sortie standard)"""
        print("Serveur MCP Sport & Musique (Archive.org) démarré!", flush=True)
        print(f"Fichier de données: {self.data_file}", flush=True)
        print(f"Catégories chargées: {', '.join(self.music_data.keys())}", flush=True)
        
        total_tracks = sum(len(tracks) for tracks in self.music_data.values())
        print(f"Total de pistes: {total_tracks}\n", flush=True)
        
        if total_tracks == 0:
            print("Aucune piste chargée ! Lance: python archive_scraper.py\n", flush=True)
        
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
