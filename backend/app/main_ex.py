# """Hephaestus Music API"""
# __version__ = "2.0.0"


# """
# Backend Hephaestus - Chatbot Sport & Musique
# Point d'entrée principal FastAPI - Version Finale Intégrée
# """

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Optional, Dict
# import requests
# import json
# import re
# import os
# from datetime import datetime

# # Import du MCP Server (chemin corrigé)
# from app.core.mcp_server import SportMusicMCPServer

# app = FastAPI(
#     title="Hephaestus API",
#     description="API Chatbot Sport & Musique avec Archive.org",
#     version="2.0.0"
# )

# # ============================================================================
# # CONFIGURATION CORS
# # ============================================================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # En production, spécifier les domaines autorisés
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ============================================================================
# # INITIALISATION MCP SERVER
# # ============================================================================

# # Le MCP utilisera le chemin par défaut: backend/data/archive_music_data.json
# mcp_server = SportMusicMCPServer()

# # ============================================================================
# # CONFIGURATION OLLAMA
# # ============================================================================

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL_NAME = "sport-music-bot"

# # ============================================================================
# # STOCKAGE TEMPORAIRE DES CONVERSATIONS
# # ============================================================================

# # En production, utiliser une vraie base de données
# conversations: Dict[str, List[dict]] = {}

# # ============================================================================
# # MODÈLES PYDANTIC
# # ============================================================================

# class Message(BaseModel):
#     role: str
#     content: str

# class ChatRequest(BaseModel):
#     message: str
#     conversation_history: Optional[List[Message]] = []

# class ChatResponse(BaseModel):
#     response: str
#     playlist: Optional[dict] = None
#     error: Optional[str] = None

# # ============================================================================
# # ROUTES
# # ============================================================================

# @app.get("/")
# async def root():
#     """Route racine - Informations sur l'API"""
#     return {
#         "app": "Hephaestus",
#         "description": "Chatbot Sport & Musique avec Archive.org",
#         "version": "2.0.0",
#         "endpoints": {
#             "health": "/health",
#             "chat": "/api/chat",
#             "history": "/api/history",
#             "categories": "/categories"
#         }
#     }

# @app.get("/health")
# async def health():
#     """Vérifie que tous les composants fonctionnent"""
#     # Test Ollama
#     try:
#         ollama_check = requests.get("http://localhost:11434/api/tags", timeout=2)
#         ollama_status = "ok" if ollama_check.status_code == 200 else "error"
#     except:
#         ollama_status = "error"
    
#     # Test MCP
#     try:
#         mcp_categories = await mcp_server.list_categories()
#         mcp_status = "ok" if mcp_categories.get("success") else "error"
#         mcp_tracks = mcp_categories.get("total_tracks", 0)
#     except:
#         mcp_status = "error"
#         mcp_tracks = 0
    
#     # Test Fichier de données
#     data_file_exists = os.path.exists(mcp_server.data_file)
    
#     overall_status = "ok" if (
#         ollama_status == "ok" and 
#         mcp_status == "ok" and 
#         data_file_exists and
#         mcp_tracks > 0
#     ) else "degraded"
    
#     return {
#         "status": overall_status,
#         "timestamp": datetime.utcnow().isoformat(),
#         "components": {
#             "ollama": ollama_status,
#             "mcp": mcp_status,
#             "api": "ok",
#             "data_file": "ok" if data_file_exists else "missing"
#         },
#         "stats": {
#             "total_tracks": mcp_tracks,
#             "data_file": mcp_server.data_file
#         },
#         "messages": {
#             "ollama": "Ollama OK" if ollama_status == "ok" else "Lance 'ollama serve'",
#             "data": f"{mcp_tracks} pistes disponibles" if mcp_tracks > 0 else "Lance 'python -m app.tools.archive_scraper'"
#         }
#     }

# @app.get("/categories")
# async def get_categories():
#     """Liste toutes les catégories de sport disponibles"""
#     result = await mcp_server.list_categories()
#     return result

# # ============================================================================
# # ROUTE PRINCIPALE - CHAT
# # ============================================================================

# @app.post("/api/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     """
#     Endpoint principal du chatbot
#     Reçoit un message, l'analyse avec Ollama, crée une playlist via MCP
#     """
#     try:
#         print(f"\n📩 Message reçu: {request.message}")
        
#         # 1. Analyser avec Ollama (si disponible)
#         try:
#             ollama_response = await call_ollama(request.message, request.conversation_history)
#             print(f"🤖 Ollama: {ollama_response[:100]}...")
            
#             # 2. Parser l'intent (JSON ou extraction)
#             try:
#                 intent = json.loads(ollama_response.strip())
#             except json.JSONDecodeError:
#                 intent = extract_intent_from_text(ollama_response)
                
#         except HTTPException as e:
#             # Si Ollama n'est pas disponible, extraction directe
#             print(f"⚠️  Ollama inaccessible, extraction directe")
#             intent = extract_intent_from_text(request.message)
        
#         print(f"✅ Intent détecté: {intent}")
        
#         # 3. Créer la playlist via MCP
#         playlist = await create_playlist_from_intent(intent)
        
#         # 4. Gérer les erreurs
#         if "error" in playlist:
#             error_msg = playlist['error']
#             categories = await mcp_server.list_categories()
#             available = ", ".join([c['name'] for c in categories.get('categories', [])])
            
#             return ChatResponse(
#                 response=f"❌ {error_msg}\n\n💡 Catégories disponibles: {available}",
#                 error=error_msg
#             )
        
#         # 5. Formater la réponse
#         formatted_response = format_playlist_response(playlist)
        
#         print(f"✅ Playlist créée: {playlist.get('track_count')} pistes")
        
#         return ChatResponse(
#             response=formatted_response,
#             playlist=playlist
#         )
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"❌ Erreur serveur: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

# # ============================================================================
# # ROUTE HISTORIQUE
# # ============================================================================

# @app.get("/api/history")
# async def get_history():
#     """
#     Récupère l'historique global des conversations
#     """
#     try:
#         all_messages = []
#         for conv_id, messages in conversations.items():
#             all_messages.extend(messages)
        
#         # Limiter aux 50 derniers messages
#         recent_messages = all_messages[-50:] if len(all_messages) > 50 else all_messages
        
#         return {
#             "messages": recent_messages,
#             "total": len(all_messages),
#             "showing": len(recent_messages)
#         }
#     except Exception as e:
#         print(f"❌ Erreur récupération historique: {str(e)}")
#         return {
#             "messages": [],
#             "total": 0,
#             "showing": 0,
#             "error": str(e)
#         }

# # ============================================================================
# # ROUTE LEGACY (sans /api)
# # ============================================================================

# @app.post("/chat", response_model=ChatResponse)
# async def chat_legacy(request: ChatRequest):
#     """Endpoint legacy pour rétrocompatibilité"""
#     return await chat(request)

# # ============================================================================
# # FONCTIONS HELPER
# # ============================================================================

# async def call_ollama(message: str, history: List[Message]) -> str:
#     """
#     Appelle Ollama pour analyser le message
#     """
#     try:
#         # Limiter l'historique aux 5 derniers messages
#         recent_history = history[-5:] if len(history) > 5 else history
#         context = "\n".join([f"{msg.role}: {msg.content}" for msg in recent_history])
        
#         # Construire le prompt
#         prompt = f"{context}\nuser: {message}\nassistant:" if context else f"user: {message}\nassistant:"
        
#         payload = {
#             "model": MODEL_NAME,
#             "prompt": prompt,
#             "stream": False,
#             "options": {
#                 "temperature": 0.3,
#                 "num_ctx": 4096
#             }
#         }
        
#         # Appel à Ollama
#         response = requests.post(OLLAMA_URL, json=payload, timeout=30)
#         response.raise_for_status()
        
#         return response.json().get("response", "")
        
#     except requests.exceptions.Timeout:
#         raise HTTPException(status_code=504, detail="Timeout Ollama (>30s)")
#     except requests.exceptions.ConnectionError:
#         raise HTTPException(
#             status_code=503, 
#             detail="❌ Ollama inaccessible. Lance 'ollama serve'"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erreur Ollama: {str(e)}")

# def extract_intent_from_text(text: str) -> dict:
#     """
#     Extrait l'intent du texte si Ollama ne retourne pas du JSON
#     Fallback intelligent basé sur des regex
#     """
#     sport_mapping = {
#         "boxe": "boxe", "boxing": "boxe", "punch": "boxe",
#         "course": "course_a_pied", "running": "course_a_pied", "courir": "course_a_pied", "run": "course_a_pied", "jogging": "course_a_pied",
#         "musculation": "musculation", "muscu": "musculation", "gym": "musculation", "workout": "musculation", "fitness": "musculation",
#         "marche": "marche_a_pied", "walking": "marche_a_pied", "walk": "marche_a_pied",
#         "echauffement": "echauffement", "warm": "echauffement", "warmup": "echauffement", "étirement": "echauffement", "yoga": "echauffement"
#     }
    
#     text_lower = text.lower()
    
#     # Détection du sport
#     activity = "course_a_pied"  # Défaut
#     for keyword, sport_value in sport_mapping.items():
#         if keyword in text_lower:
#             activity = sport_value
#             break
    
#     # Détection de la durée
#     duration = 60  # Défaut: 60 minutes
#     duration_patterns = [
#         (r'(\d+)\s*h(?:eure)?(?:s)?', 60),  # heures -> minutes
#         (r'(\d+)\s*min(?:ute)?(?:s)?', 1),  # minutes
#     ]
    
#     for pattern, multiplier in duration_patterns:
#         match = re.search(pattern, text_lower)
#         if match:
#             num = int(match.group(1))
#             duration = num * multiplier
#             break
    
#     # Détection de l'énergie
#     energy = "haute"  # Défaut
#     if any(word in text_lower for word in ["calme", "relax", "doux", "leger", "light", "chill"]):
#         energy = "calme"
#     elif any(word in text_lower for word in ["modérée", "moyen", "medium", "moderate"]):
#         energy = "modérée"
#     elif any(word in text_lower for word in ["intense", "hard", "rapide", "fast", "high"]):
#         energy = "haute"
    
#     return {
#         "activity": activity,
#         "duration": duration,
#         "energy": energy
#     }

# async def create_playlist_from_intent(intent: dict) -> dict:
#     """Crée la playlist via le serveur MCP"""
#     sport = intent.get("activity", "course_a_pied")
#     duration = intent.get("duration", 60)
    
#     print(f"🎵 Création playlist: sport={sport}, durée={duration}min")
    
#     try:
#         return await mcp_server.create_playlist(sport, duration)
#     except Exception as e:
#         print(f"❌ Erreur création playlist: {str(e)}")
#         return {
#             "error": f"Impossible de créer la playlist: {str(e)}",
#             "sport": sport,
#             "duration": duration
#         }

# def format_playlist_response(playlist: dict) -> str:
#     """Formate la playlist en texte lisible pour l'utilisateur"""
#     sport_display_map = {
#         "course_a_pied": ("🏃 Course à pied", "haute énergie"),
#         "boxe": ("🥊 Boxe", "haute intensité"),
#         "musculation": ("💪 Musculation", "motivation"),
#         "marche_a_pied": ("🚶 Marche", "calme"),
#         "echauffement": ("🧘 Échauffement", "douceur")
#     }
    
#     sport_key = playlist.get('sport', 'course_a_pied')
#     sport_display, intensity = sport_display_map.get(sport_key, (sport_key, ""))
    
#     # En-tête
#     response = f"🎵 **Playlist {sport_display}** – {playlist['target_duration_min']} minutes ({intensity})\n\n"
    
#     # Liste des pistes
#     tracks = playlist.get('playlist', [])
#     display_count = min(10, len(tracks))  # Afficher max 10 pistes
    
#     for i, track in enumerate(tracks[:display_count], 1):
#         title = track.get('title', 'Unknown')
#         artist = track.get('artist', 'Unknown')
#         duration = track.get('duration', '0:00')
#         preview_url = track.get('preview_url', '#')
        
#         response += f"**{i}.** {title} – {artist} ({duration})\n"
#         response += f"    🔗 {preview_url}\n"
    
#     # Indication s'il y a plus de pistes
#     if len(tracks) > display_count:
#         response += f"\n*... et {len(tracks) - display_count} autres pistes*\n"
    
#     # Statistiques
#     response += f"\n⏱ **Durée totale**: {playlist['actual_duration_min']} min"
#     response += f"\n🎯 **BPM**: {playlist['bpm_range']}"
#     response += f"\n🎼 **Pistes**: {len(tracks)} ({playlist.get('unique_tracks', len(tracks))} uniques)"
    
#     return response

# # ============================================================================
# # POINT D'ENTRÉE
# # ============================================================================

# if __name__ == "__main__":
#     import uvicorn
    
#     print("\n" + "="*70)
#     print("🚀 Démarrage Hephaestus Backend v2.0")
#     print("="*70)
#     print("📍 Serveur:        http://localhost:8000")
#     print("📚 Documentation:  http://localhost:8000/docs")
#     print("🏥 Health Check:   http://localhost:8000/health")
#     print("💬 Chat API:       POST http://localhost:8000/api/chat")
#     print("="*70)
#     print("💡 Assure-toi que:")
#     print("   1. Ollama est lancé: ollama serve")
#     print("   2. Les données sont générées: python -m app.tools.archive_scraper")
#     print("="*70 + "\n")
    
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

=========================================================





















"""Hephaestus Music API"""
__version__ = "2.0.0"

"""
Backend Hephaestus - Chatbot Sport & Musique
Point d'entrée principal FastAPI - Version Finale Intégrée
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import requests
import json
import re
import os
from datetime import datetime

# Import du MCP Server (chemin corrigé)
from app.core.mcp_server import SportMusicMCPServer

app = FastAPI(
    title="Hephaestus API",
    description="API Chatbot Sport & Musique avec Archive.org",
    version="2.0.0"
)

# ============================================================================
# CONFIGURATION CORS
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# INITIALISATION MCP SERVER
# ============================================================================

mcp_server = SportMusicMCPServer()

# ============================================================================
# CONFIGURATION OLLAMA
# ============================================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "sport-music-bot"

# ============================================================================
# STOCKAGE TEMPORAIRE DES CONVERSATIONS
# ============================================================================

conversations: Dict[str, List[dict]] = {}

# ============================================================================
# MODÈLES PYDANTIC
# ============================================================================

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    playlist: Optional[dict] = None
    error: Optional[str] = None

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/")
async def root():
    """Route racine - Informations sur l'API"""
    return {
        "app": "Hephaestus",
        "description": "Chatbot Sport & Musique avec Archive.org",
        "version": "2.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/api/chat",
            "history": "/api/history",
            "categories": "/categories"
        }
    }

@app.get("/health")
async def health():
    """Vérifie que tous les composants fonctionnent"""
    try:
        ollama_check = requests.get("http://localhost:11434/api/tags", timeout=2)
        ollama_status = "ok" if ollama_check.status_code == 200 else "error"
    except:
        ollama_status = "error"
    
    try:
        mcp_categories = await mcp_server.list_categories()
        mcp_status = "ok" if mcp_categories.get("success") else "error"
        mcp_tracks = mcp_categories.get("total_tracks", 0)
    except:
        mcp_status = "error"
        mcp_tracks = 0
    
    data_file_exists = os.path.exists(mcp_server.data_file)
    
    overall_status = "ok" if (
        ollama_status == "ok" and 
        mcp_status == "ok" and 
        data_file_exists and
        mcp_tracks > 0
    ) else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "ollama": ollama_status,
            "mcp": mcp_status,
            "api": "ok",
            "data_file": "ok" if data_file_exists else "missing"
        },
        "stats": {
            "total_tracks": mcp_tracks,
            "data_file": mcp_server.data_file
        },
        "messages": {
            "ollama": "Ollama OK" if ollama_status == "ok" else "Lance 'ollama serve'",
            "data": f"{mcp_tracks} pistes disponibles" if mcp_tracks > 0 else "Lance 'python -m app.tools.archive_scraper'"
        }
    }

@app.get("/categories")
async def get_categories():
    """Liste toutes les catégories de sport disponibles"""
    result = await mcp_server.list_categories()
    return result

# ============================================================================
# ROUTE PRINCIPALE - CHAT
# ============================================================================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal du chatbot
    Reçoit un message, l'analyse, crée une playlist via MCP
    """
    try:
        print(f"\n📩 Message reçu: {request.message}")
        
        # 1. Extraire l'intent depuis le message
        intent = extract_intent_from_text(request.message)
        print(f"✅ Intent détecté: {intent}")
        
        # 2. Créer la playlist via MCP
        playlist = await create_playlist_from_intent(intent)
        
        # 3. Gérer les erreurs
        if "error" in playlist:
            error_msg = playlist['error']
            categories = await mcp_server.list_categories()
            available = ", ".join([c['name'] for c in categories.get('categories', [])])
            
            return ChatResponse(
                response=f"❌ {error_msg}\n\n💡 Catégories disponibles: {available}",
                error=error_msg
            )
        
        # 4. Formater la réponse TEXTE pour le chat
        formatted_response = format_playlist_text_response(playlist, intent)
        
        print(f"✅ Playlist créée: {playlist.get('track_count')} pistes")
        
        # 5. Retourner TEXTE + DONNÉES JSON
        return ChatResponse(
            response=formatted_response,
            playlist=playlist  # ← Données brutes pour le composant PlaylistView
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur serveur: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

# ============================================================================
# ROUTE HISTORIQUE
# ============================================================================

@app.get("/api/history")
async def get_history():
    """Récupère l'historique global des conversations"""
    try:
        all_messages = []
        for conv_id, messages in conversations.items():
            all_messages.extend(messages)
        
        recent_messages = all_messages[-50:] if len(all_messages) > 50 else all_messages
        
        return {
            "messages": recent_messages,
            "total": len(all_messages),
            "showing": len(recent_messages)
        }
    except Exception as e:
        print(f"❌ Erreur récupération historique: {str(e)}")
        return {
            "messages": [],
            "total": 0,
            "showing": 0,
            "error": str(e)
        }

# ============================================================================
# ROUTE LEGACY
# ============================================================================

@app.post("/chat", response_model=ChatResponse)
async def chat_legacy(request: ChatRequest):
    """Endpoint legacy pour rétrocompatibilité"""
    return await chat(request)

# ============================================================================
# FONCTIONS HELPER
# ============================================================================

def extract_intent_from_text(text: str) -> dict:
    """
    Extrait l'intent du texte avec détection INTELLIGENTE du sport
    """
    sport_keywords = {
        "boxe": ["boxe", "boxing", "punch", "combat", "frappe"],
        "course_a_pied": ["course", "running", "courir", "run", "jogging", "cardio"],
        "musculation": ["musculation", "muscu", "gym", "workout", "fitness", "training", "poids", "haltère"],
        "marche_a_pied": ["marche", "walking", "walk", "promenade"],
        "echauffement": ["echauffement", "warm", "warmup", "étirement", "stretch", "yoga", "meditation", "relax"]
    }
    
    text_lower = text.lower()
    
    # Détection INTELLIGENTE du sport (cherche tous les mots-clés)
    detected_sport = None
    max_matches = 0
    
    for sport, keywords in sport_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in text_lower)
        if matches > max_matches:
            max_matches = matches
            detected_sport = sport
    
    # Si aucun sport détecté, demander à l'utilisateur
    if not detected_sport or max_matches == 0:
        detected_sport = None  # Sera géré comme une erreur
    
    activity = detected_sport
    
    # Détection de la durée
    duration = 30  # Défaut: 30 minutes
    duration_patterns = [
        (r'(\d+)\s*h(?:eure)?(?:s)?', 60),  # heures -> minutes
        (r'(\d+)\s*min(?:ute)?(?:s)?', 1),  # minutes
    ]
    
    for pattern, multiplier in duration_patterns:
        match = re.search(pattern, text_lower)
        if match:
            num = int(match.group(1))
            duration = num * multiplier
            break
    
    # Détection de l'énergie
    energy = "haute"
    if any(word in text_lower for word in ["calme", "relax", "doux", "leger", "light", "chill", "zen"]):
        energy = "calme"
    elif any(word in text_lower for word in ["modérée", "moyen", "medium", "moderate"]):
        energy = "modérée"
    elif any(word in text_lower for word in ["intense", "hard", "rapide", "fast", "high", "explosif"]):
        energy = "haute"
    
    return {
        "activity": activity,
        "duration": duration,
        "energy": energy
    }

async def create_playlist_from_intent(intent: dict) -> dict:
    """Crée la playlist via le serveur MCP"""
    sport = intent.get("activity")
    
    # Vérification que le sport a été détecté
    if not sport:
        return {
            "error": "Je n'ai pas compris quel sport tu veux faire. Peux-tu préciser ? (course, boxe, musculation, marche, échauffement)"
        }
    
    duration = intent.get("duration", 30)
    
    print(f"🎵 Création playlist: sport={sport}, durée={duration}min")
    
    try:
        return await mcp_server.create_playlist(sport, duration)
    except Exception as e:
        print(f"❌ Erreur création playlist: {str(e)}")
        return {
            "error": f"Impossible de créer la playlist: {str(e)}",
            "sport": sport,
            "duration": duration
        }

def format_playlist_text_response(playlist: dict, intent: dict) -> str:
    """Formate la playlist en texte lisible pour le CHAT uniquement"""
    sport_display_map = {
        "course_a_pied": "🏃 Course à pied",
        "boxe": "🥊 Boxe",
        "musculation": "💪 Musculation",
        "marche_a_pied": "🚶 Marche",
        "echauffement": "🧘 Échauffement"
    }
    
    sport_key = playlist.get('sport', 'course_a_pied')
    sport_display = sport_display_map.get(sport_key, sport_key)
    
    # Message simple et élégant pour le chat
    response = f"✨ J'ai créé ta playlist {sport_display} !\n\n"
    response += f"🎵 {playlist['track_count']} morceaux • {playlist['actual_duration_min']} minutes\n"
    response += f"🎯 {playlist['bpm_range']} BPM\n\n"
    response += f"La playlist s'affiche à droite. Profite bien de ta session ! 💪"
    
    return response

# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🚀 Démarrage Hephaestus Backend v2.0")
    print("="*70)
    print("📍 Serveur:        http://localhost:8000")
    print("📚 Documentation:  http://localhost:8000/docs")
    print("🏥 Health Check:   http://localhost:8000/health")
    print("💬 Chat API:       POST http://localhost:8000/api/chat")
    print("="*70)
    print("💡 Assure-toi que:")
    print("   1. Ollama est lancé: ollama serve (optionnel)")
    print("   2. Les données sont générées: python -m app.tools.archive_scraper")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")