# """
# Agent IA - Orchestrateur Intelligent
# =====================================
# Utilise Ollama pour analyser les requêtes et générer des playlists via MCP
# """

# import ollama
# import json
# import asyncio
# from typing import Dict, Optional
# import os

# # Import du serveur MCP (chemin corrigé)
# from app.core.mcp_server import SportMusicMCPServer


# class MusicAgent:
#     """Agent intelligent pour générer des playlists musicales personnalisées"""
    
#     def __init__(self, model_name: str = "playlist-bot-mcp"):
#         """
#         Initialise l'agent
        
#         Args:
#             model_name: Nom du modèle Ollama à utiliser
#         """
#         self.model_name = model_name
        
#         # Initialise le serveur MCP (utilise chemin par défaut)
#         self.mcp_server = SportMusicMCPServer()
        
#         # Mapping des activités vers les formats du serveur MCP
#         self.activity_mapping = {
#             "boxe": "boxe",
#             "boxing": "boxe",
#             "punch": "boxe",
#             "combat": "boxe",
            
#             "course": "course_a_pied",
#             "running": "course_a_pied",
#             "jogging": "course_a_pied",
#             "courir": "course_a_pied",
#             "run": "course_a_pied",
#             "course à pied": "course_a_pied",
            
#             "musculation": "musculation",
#             "muscu": "musculation",
#             "gym": "musculation",
#             "fitness": "musculation",
#             "workout": "musculation",
#             "training": "musculation",
            
#             "marche": "marche_a_pied",
#             "marche à pied": "marche_a_pied",
#             "walking": "marche_a_pied",
#             "walk": "marche_a_pied",
            
#             "échauffement": "echauffement",
#             "warmup": "echauffement",
#             "warm up": "echauffement",
#             "stretching": "echauffement",
#             "étirement": "echauffement",
#             "yoga": "echauffement",
#             "meditation": "echauffement"
#         }
    
#     def extract_parameters(self, user_input: str) -> Optional[Dict]:
#         """
#         Utilise Ollama pour extraire les paramètres de la requête
        
#         Args:
#             user_input: Message de l'utilisateur
            
#         Returns:
#             Dict avec activity, duration, energy ou None si échec
#         """
#         try:
#             response = ollama.chat(
#                 model=self.model_name,
#                 messages=[{
#                     'role': 'user',
#                     'content': user_input
#                 }]
#             )
            
#             # Parse le JSON retourné par le LLM
#             try:
#                 params = json.loads(response['message']['content'])
#                 print(f"📊 Paramètres extraits par Ollama: {params}")
                
#                 # Normalise l'activité
#                 activity = params.get('activity', '').lower()
#                 normalized_activity = self.activity_mapping.get(activity, activity)
#                 params['activity'] = normalized_activity
                
#                 return params
                
#             except json.JSONDecodeError as e:
#                 print(f"⚠️  Ollama n'a pas retourné du JSON: {e}")
#                 print(f"Réponse brute: {response['message']['content']}")
#                 return None
                
#         except Exception as e:
#             print(f"❌ Erreur Ollama: {e}")
#             return None
    
#     async def get_music_from_mcp(self, activity: str, duration: int) -> Optional[Dict]:
#         """
#         Appelle le serveur MCP pour récupérer les musiques
        
#         Args:
#             activity: Type d'activité sportive
#             duration: Durée en minutes
            
#         Returns:
#             Résultat MCP avec la playlist ou None
#         """
#         try:
#             result = await self.mcp_server.create_playlist(
#                 sport=activity,
#                 duration_minutes=duration,
#                 shuffle=True
#             )
            
#             if result.get('success'):
#                 print(f"🎵 Playlist créée: {result.get('track_count')} pistes")
#                 return result
#             else:
#                 print(f"❌ Erreur MCP: {result.get('error')}")
#                 return None
                
#         except Exception as e:
#             print(f"❌ Erreur lors de l'appel MCP: {e}")
#             return None
    
#     def format_playlist(self, mcp_result: Dict) -> str:
#         """
#         Formate la playlist au format texte pour l'utilisateur
        
#         Args:
#             mcp_result: Résultat du MCP
            
#         Returns:
#             Playlist formatée en texte
#         """
#         # Emoji mapping
#         emoji_map = {
#             "boxe": "🥊",
#             "course_a_pied": "🏃",
#             "musculation": "💪",
#             "marche_a_pied": "🚶",
#             "echauffement": "🧘"
#         }
        
#         sport = mcp_result.get('sport', '')
#         emoji = emoji_map.get(sport, "🎵")
#         duration = mcp_result.get('target_duration_min', 0)
#         bpm_range = mcp_result.get('bpm_range', 'N/A')
        
#         # Header
#         sport_display = sport.replace('_', ' ').title()
#         playlist = f"{emoji} **Playlist {sport_display}** – {duration} minutes\n"
#         playlist += f"🎯 BPM recommandé: {bpm_range}\n\n"
        
#         # Tracks
#         tracks = mcp_result.get('playlist', [])
#         display_count = min(10, len(tracks))  # Max 10 pistes affichées
        
#         for i, track in enumerate(tracks[:display_count], 1):
#             title = track.get('title', 'Unknown')
#             artist = track.get('artist', 'Unknown')
#             duration_str = track.get('duration', '0:00')
#             preview_url = track.get('preview_url', '#')
            
#             # Format: Numéro. Title – Artist (duration)
#             playlist += f"**{i}.** {title} – {artist} ({duration_str})\n"
#             playlist += f"    🔗 {preview_url}\n"
        
#         # Indication si plus de pistes
#         if len(tracks) > display_count:
#             playlist += f"\n*... et {len(tracks) - display_count} autres pistes*\n"
        
#         # Footer avec stats
#         total_duration = mcp_result.get('actual_duration_formatted', '0:00')
#         unique_tracks = mcp_result.get('unique_tracks', len(tracks))
        
#         playlist += f"\n⏱ **Durée totale**: {total_duration}"
#         playlist += f"\n🎼 **Pistes**: {len(tracks)} ({unique_tracks} uniques)"
        
#         return playlist
    
#     async def generate_playlist(self, user_input: str) -> Dict:
#         """
#         Pipeline complet: input → LLM → MCP → format
        
#         Args:
#             user_input: Message de l'utilisateur
            
#         Returns:
#             Dict avec 'response' (texte formaté) et 'playlist' (données brutes)
#         """
#         print(f"\n🎯 Requête utilisateur: {user_input}\n")
        
#         # 1. Extraction des paramètres avec Ollama
#         params = self.extract_parameters(user_input)
        
#         if not params:
#             return {
#                 "response": "❌ Je n'ai pas compris votre demande. Exemple: 'J'ai une séance de boxe de 1h'",
#                 "playlist": None,
#                 "error": "Failed to extract parameters"
#             }
        
#         activity = params.get('activity')
#         duration = params.get('duration', 60)
        
#         # Validation
#         valid_sports = ["boxe", "course_a_pied", "musculation", "marche_a_pied", "echauffement"]
#         if activity not in valid_sports:
#             return {
#                 "response": f"❌ Sport non reconnu: '{activity}'. Disponibles: {', '.join(valid_sports)}",
#                 "playlist": None,
#                 "error": f"Invalid sport: {activity}"
#             }
        
#         # 2. Récupération des musiques via MCP
#         mcp_result = await self.get_music_from_mcp(activity, duration)
        
#         if not mcp_result:
#             return {
#                 "response": "❌ Impossible de créer la playlist. Vérifiez que le fichier archive_music_data.json existe.",
#                 "playlist": None,
#                 "error": "MCP server failed"
#             }
        
#         # 3. Formatage de la playlist
#         formatted_text = self.format_playlist(mcp_result)
        
#         return {
#             "response": formatted_text,
#             "playlist": mcp_result,
#             "error": None
#         }


# # ============================================================================
# # TEST EN LIGNE DE COMMANDE
# # ============================================================================

# async def test_agent():
#     """Test de l'agent en ligne de commande"""
#     print("\n" + "="*80)
#     print("🧪 TEST DE L'AGENT IA")
#     print("="*80 + "\n")
    
#     agent = MusicAgent()
    
#     tests = [
#         "J'ai une séance de boxe de 1h",
#         "Je vais courir pendant 30 minutes",
#         "Besoin de musique pour ma muscu de 45 min"
#     ]
    
#     for test in tests:
#         print("\n" + "="*80)
#         result = await agent.generate_playlist(test)
#         print(result['response'])
#         print("="*80)
        
#         if result.get('error'):
#             print(f"\n❌ Erreur: {result['error']}")


# if __name__ == "__main__":
#     asyncio.run(test_agent())

"""
Agent IA - Orchestrateur Intelligent
=====================================
Utilise Ollama pour analyser les requêtes et générer des playlists via MCP
"""

import ollama
import json
import asyncio
from typing import Dict, Optional
import os

# Import du serveur MCP (chemin corrigé)
from app.core.mcp_server import SportMusicMCPServer


class MusicAgent:
    """Agent intelligent pour générer des playlists musicales personnalisées"""
    
    def __init__(self, model_name: str = "llama3.2"):
        """
        Initialise l'agent
        
        Args:
            model_name: Nom du modèle Ollama à utiliser
        """
        self.model_name = model_name
        
        # Initialise le serveur MCP (utilise chemin par défaut)
        self.mcp_server = SportMusicMCPServer()
        
        # Mapping des activités vers les formats du serveur MCP
        self.activity_mapping = {
            "boxe": "boxe",
            "boxing": "boxe",
            "punch": "boxe",
            "combat": "boxe",
            "fight": "boxe",
            
            "course": "course_a_pied",
            "running": "course_a_pied",
            "jogging": "course_a_pied",
            "courir": "course_a_pied",
            "run": "course_a_pied",
            "course à pied": "course_a_pied",
            "cardio": "course_a_pied",
            
            "musculation": "musculation",
            "muscu": "musculation",
            "gym": "musculation",
            "fitness": "musculation",
            "workout": "musculation",
            "training": "musculation",
            "weight": "musculation",
            
            "marche": "marche_a_pied",
            "marche à pied": "marche_a_pied",
            "walking": "marche_a_pied",
            "walk": "marche_a_pied",
            "promenade": "marche_a_pied",
            
            "échauffement": "echauffement",
            "warmup": "echauffement",
            "warm up": "echauffement",
            "stretching": "echauffement",
            "étirement": "echauffement",
            "yoga": "echauffement",
            "meditation": "echauffement",
            "relax": "echauffement"
        }
    
    def extract_parameters(self, user_input: str) -> Optional[Dict]:
        """
        Utilise Ollama pour extraire les paramètres de la requête
        
        Args:
            user_input: Message de l'utilisateur
            
        Returns:
            Dict avec activity, duration, energy ou None si échec
        """
        try:
            system_prompt = """Tu es un assistant qui extrait les paramètres d'une demande de playlist musicale.
            
Réponds UNIQUEMENT avec un objet JSON au format:
{
  "activity": "le sport détecté (boxe, course_a_pied, musculation, marche_a_pied, echauffement)",
  "duration": durée en minutes (nombre entier),
  "energy": "low/medium/high"
}

Exemples:
"J'ai une séance de boxe de 1h" -> {"activity": "boxe", "duration": 60, "energy": "high"}
"Je vais courir 30 minutes" -> {"activity": "course_a_pied", "duration": 30, "energy": "high"}
"Musique relaxante pour 20 min" -> {"activity": "echauffement", "duration": 20, "energy": "low"}

Si aucun sport n'est mentionné clairement, choisis celui qui correspond le mieux au contexte."""

            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_input}
                ]
            )
            
            # Parse le JSON retourné par le LLM
            try:
                content = response['message']['content'].strip()
                # Nettoyer les markdown code blocks si présents
                if content.startswith('```'):
                    content = content.split('```')[1]
                    if content.startswith('json'):
                        content = content[4:]
                    content = content.strip()
                
                params = json.loads(content)
                print(f"📊 Paramètres extraits par Ollama: {params}")
                
                # Normalise l'activité
                activity = params.get('activity', '').lower()
                normalized_activity = self.activity_mapping.get(activity, activity)
                params['activity'] = normalized_activity
                
                return params
                
            except json.JSONDecodeError as e:
                print(f"⚠️ Ollama n'a pas retourné du JSON: {e}")
                print(f"Réponse brute: {response['message']['content']}")
                # Fallback: extraction manuelle
                return self._extract_parameters_fallback(user_input)
                
        except Exception as e:
            print(f"❌ Erreur Ollama: {e}")
            # Fallback: extraction manuelle
            return self._extract_parameters_fallback(user_input)
    
    def _extract_parameters_fallback(self, user_input: str) -> Dict:
        """
        Extraction manuelle des paramètres si Ollama échoue
        
        Args:
            user_input: Message de l'utilisateur
            
        Returns:
            Dict avec activity, duration, energy
        """
        import re
        
        text_lower = user_input.lower()
        
        # Détection du sport (cherche le premier mot-clé trouvé)
        activity = None
        for keyword, sport_value in self.activity_mapping.items():
            if keyword in text_lower:
                activity = sport_value
                break
        
        # Si aucun sport détecté, essayer de deviner par le contexte
        if not activity:
            if any(word in text_lower for word in ["énergique", "intense", "rapide", "fort", "power"]):
                activity = "course_a_pied"
            elif any(word in text_lower for word in ["calme", "relax", "doux", "zen", "meditation"]):
                activity = "echauffement"
            elif any(word in text_lower for word in ["force", "muscle", "poids", "weight"]):
                activity = "musculation"
            else:
                # Défaut : échauffement (plus neutre que course)
                activity = "echauffement"
        
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
        energy = "medium"  # Défaut
        if any(word in text_lower for word in ["calme", "relax", "doux", "leger", "light", "chill", "zen"]):
            energy = "low"
        elif any(word in text_lower for word in ["intense", "hard", "rapide", "fast", "high", "fort", "power"]):
            energy = "high"
        
        print(f"📊 Paramètres extraits (fallback): activity={activity}, duration={duration}, energy={energy}")
        
        return {
            "activity": activity,
            "duration": duration,
            "energy": energy
        }
    
    async def get_music_from_mcp(self, activity: str, duration: int) -> Optional[Dict]:
        """
        Appelle le serveur MCP pour récupérer les musiques
        
        Args:
            activity: Type d'activité sportive
            duration: Durée en minutes
            
        Returns:
            Résultat MCP avec la playlist ou None
        """
        try:
            result = await self.mcp_server.create_playlist(
                sport=activity,
                duration_minutes=duration,
                shuffle=True
            )
            
            if result.get('success'):
                print(f"🎵 Playlist créée: {result.get('track_count')} pistes")
                return result
            else:
                print(f"❌ Erreur MCP: {result.get('error')}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de l'appel MCP: {e}")
            return None
    
    def format_playlist(self, mcp_result: Dict) -> str:
        """
        Formate la playlist en message simple pour l'utilisateur
        
        Args:
            mcp_result: Résultat du MCP
            
        Returns:
            Message simple
        """
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
        track_count = mcp_result.get('track_count', 0)
        
        # Message simple et clair
        sport_display = sport.replace('_', ' ').title()
        message = f"{emoji} J'ai créé ta playlist {sport_display} de {duration} minutes avec {track_count} morceaux ({bpm_range} BPM). Tu peux la voir sur le côté !"
        
        return message
    
    async def generate_playlist(self, user_input: str) -> Dict:
        """
        Pipeline complet: input → LLM → MCP → format
        
        Args:
            user_input: Message de l'utilisateur
            
        Returns:
            Dict avec 'response' (texte formaté) et 'playlist' (données brutes)
        """
        print(f"\n🎯 Requête utilisateur: {user_input}\n")
        
        # 1. Extraction des paramètres avec Ollama (ou fallback)
        params = self.extract_parameters(user_input)
        
        if not params:
            return {
                "response": "❌ Je n'ai pas compris votre demande. Exemple: 'J'ai une séance de boxe de 1h'",
                "playlist": None,
                "error": "Failed to extract parameters"
            }
        
        activity = params.get('activity')
        duration = params.get('duration', 30)
        
        # Validation
        valid_sports = ["boxe", "course_a_pied", "musculation", "marche_a_pied", "echauffement"]
        if activity not in valid_sports:
            return {
                "response": f"❌ Sport non reconnu: '{activity}'. Disponibles: {', '.join(valid_sports)}",
                "playlist": None,
                "error": f"Invalid sport: {activity}"
            }
        
        # 2. Récupération des musiques via MCP
        mcp_result = await self.get_music_from_mcp(activity, duration)
        
        if not mcp_result:
            return {
                "response": "❌ Impossible de créer la playlist. Vérifie que le fichier archive_music_data.json existe.",
                "playlist": None,
                "error": "MCP server failed"
            }
        
        # 3. Formatage du message simple
        formatted_text = self.format_playlist(mcp_result)
        
        return {
            "response": formatted_text,
            "playlist": mcp_result,
            "error": None
        }


# ============================================================================
# TEST EN LIGNE DE COMMANDE
# ============================================================================

async def test_agent():
    """Test de l'agent en ligne de commande"""
    print("\n" + "="*80)
    print("🧪 TEST DE L'AGENT IA")
    print("="*80 + "\n")
    
    agent = MusicAgent()
    
    tests = [
        "J'ai une séance de boxe de 1h",
        "Je vais courir pendant 30 minutes",
        "Besoin de musique pour ma muscu de 45 min",
        "Salut"  # Test d'une requête ambiguë
    ]
    
    for test in tests:
        print("\n" + "="*80)
        result = await agent.generate_playlist(test)
        print(result['response'])
        if result.get('playlist'):
            print(f"\n📊 Playlist: {result['playlist'].get('track_count')} pistes")
        print("="*80)
        
        if result.get('error'):
            print(f"\n❌ Erreur: {result['error']}")


if __name__ == "__main__":
    asyncio.run(test_agent())