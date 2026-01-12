import ollama
import json
import asyncio
from typing import Dict, Optional
import sys
import os

# Import du serveur MCP
sys.path.append(os.path.join(os.path.dirname(__file__), 'app', 'core'))
from sport_music_mcp_v2 import SportMusicMCPServer


class PlaylistBot:
    def __init__(self):
        self.model_name = "playlist-bot-mcp"
        self.mcp_server = SportMusicMCPServer(data_file="app/archive_music_data.json")
        
        # Mapping des activités vers les formats du serveur MCP
        self.activity_mapping = {
            "boxe": "boxe",
            "boxing": "boxe",
            "course": "course_a_pied",
            "running": "course_a_pied",
            "jogging": "course_a_pied",
            "course à pied": "course_a_pied",
            "musculation": "musculation",
            "muscu": "musculation",
            "gym": "musculation",
            "fitness": "musculation",
            "marche": "marche_a_pied",
            "marche à pied": "marche_a_pied",
            "walking": "marche_a_pied",
            "échauffement": "echauffement",
            "warmup": "echauffement",
            "stretching": "echauffement",
            "yoga": "echauffement"
        }
    
    def extract_parameters(self, user_input: str) -> Optional[Dict]:
        """Utilise Ollama pour extraire les paramètres"""
        response = ollama.chat(
            model=self.model_name,
            messages=[{
                'role': 'user',
                'content': user_input
            }]
        )
        
        # Parse le JSON retourné par le LLM
        try:
            params = json.loads(response['message']['content'])
            print(f"📊 Paramètres extraits: {params}")
            
            # Normalise l'activité
            activity = params.get('activity', '').lower()
            normalized_activity = self.activity_mapping.get(activity, activity)
            params['activity'] = normalized_activity
            
            return params
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON: {e}")
            print(f"Réponse brute: {response['message']['content']}")
            return None
    
    async def get_music_from_mcp(self, activity: str, duration: int) -> Optional[Dict]:
        """Appelle le serveur MCP pour récupérer les musiques"""
        try:
            result = await self.mcp_server.create_playlist(
                sport=activity,
                duration_minutes=duration,
                shuffle=True
            )
            
            if result.get('success'):
                print(f"🎵 Playlist créée: {result.get('track_count')} tracks")
                return result
            else:
                print(f"❌ Erreur MCP: {result.get('error')}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de l'appel MCP: {e}")
            return None
    
    def format_playlist(self, mcp_result: Dict) -> str:
        """Formate la playlist au format final"""
        # Emoji mapping
        emoji_map = {
            "boxe": "🥊",
            "course_a_pied": "🏃",
            "musculation": "💪",
            "marche_a_pied": "🚶",
            "echauffement": "🧘"
        }
        
        sport = mcp_result.get('sport', '')
        emoji = emoji_map.get(sport, "🎵")
        duration = mcp_result.get('target_duration_min', 0)
        bpm_range = mcp_result.get('bpm_range', 'N/A')
        
        # Header
        playlist = f"{emoji} Playlist {sport.replace('_', ' ').title()} – {duration} minutes\n"
        playlist += f"🎯 BPM recommandé: {bpm_range}\n\n"
        
        # Tracks
        tracks = mcp_result.get('playlist', [])
        for track in tracks:
            title = track.get('title', 'Unknown')
            artist = track.get('artist', 'Unknown')
            duration_str = track.get('duration', '0:00')
            preview_url = track.get('preview_url', '#')
            
            # Format: Title – Artist (duration) ▶️ URL
            playlist += f"{title} – {artist} ({duration_str}) ▶️ {preview_url}\n"
        
        # Footer
        total_duration = mcp_result.get('actual_duration_formatted', '0:00')
        playlist += f"\n⏱ Total : {total_duration}"
        
        return playlist
    
    async def generate_playlist(self, user_input: str) -> str:
        """Pipeline complet: input → LLM → MCP → format"""
        
        print(f"\n🎯 Requête utilisateur: {user_input}\n")
        
        # 1. Extraction des paramètres avec Ollama
        params = self.extract_parameters(user_input)
        if not params:
            return "❌ Je n'ai pas compris votre demande. Exemple: 'J'ai une séance de boxe de 1h'"
        
        activity = params.get('activity')
        duration = params.get('duration', 60)
        
        # Validation
        valid_sports = ["boxe", "course_a_pied", "musculation", "marche_a_pied", "echauffement"]
        if activity not in valid_sports:
            return f"❌ Sport non reconnu: '{activity}'. Disponibles: {', '.join(valid_sports)}"
        
        # 2. Récupération des musiques via MCP
        mcp_result = await self.get_music_from_mcp(activity, duration)
        
        if not mcp_result:
            return "❌ Impossible de créer la playlist. Vérifiez que le fichier archive_music_data.json existe."
        
        # 3. Formatage de la playlist
        playlist = self.format_playlist(mcp_result)
        
        return playlist


# ============================================
# EXEMPLE D'UTILISATION AVEC FASTAPI
# ============================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Sport Music Playlist API")

# CORS pour autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = PlaylistBot()

class PlaylistRequest(BaseModel):
    user_input: str

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Sport Music Playlist API",
        "version": "1.0.0",
        "endpoints": {
            "generate_playlist": "POST /generate-playlist",
            "health": "GET /health"
        }
    }

@app.get("/health")
async def health():
    """Endpoint de santé"""
    return {"status": "ok", "model": bot.model_name}

@app.post("/generate-playlist")
async def generate_playlist(request: PlaylistRequest):
    """
    Génère une playlist personnalisée
    
    Exemple de requête:
    {
        "user_input": "J'ai une séance de boxe de 1h"
    }
    """
    try:
        playlist = await bot.generate_playlist(request.user_input)
        return {
            "success": True,
            "playlist": playlist
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# TEST EN LIGNE DE COMMANDE
# ============================================

async def test_cli():
    """Test simple en ligne de commande"""
    bot = PlaylistBot()
    
    tests = [
        "J'ai une séance de boxe de 1h",
        "Je vais courir pendant 30 minutes",
        "Besoin de musique pour ma muscu de 45 min"
    ]
    
    for test in tests:
        print("\n" + "="*80)
        result = await bot.generate_playlist(test)
        print(result)
        print("="*80)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Mode test
        asyncio.run(test_cli())
    else:
        # Mode serveur
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)