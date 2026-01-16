import ollama
import json
import asyncio
from typing import Dict, Optional
import os

# Import du serveur MCP (chemin corrigé)
from app.core.mcp_server import SportMusicMCPServer


class MusicAgent:
    
    def __init__(self, model_name: str = "llama3.2"):

        self.model_name = model_name
        
        self.mcp_server = SportMusicMCPServer()
        
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
        sport_display = sport.replace('_', ' ').title()
        message = f"{emoji} J'ai créé ta playlist {sport_display} de {duration} minutes avec {track_count} morceaux ({bpm_range} BPM). Tu peux la voir sur le côté !"
        
        return message
    
    async def generate_playlist(self, user_input: str) -> Dict:

        print(f"\n🎯 Requête utilisateur: {user_input}\n")
        
        params = self.extract_parameters(user_input)
        
        if not params:
            return {
                "response": "❌ Je n'ai pas compris votre demande. Exemple: 'J'ai une séance de boxe de 1h'",
                "playlist": None,
                "error": "Failed to extract parameters"
            }
        
        activity = params.get('activity')
        duration = params.get('duration', 30)
        
        valid_sports = ["boxe", "course_a_pied", "musculation", "marche_a_pied", "echauffement"]
        if activity not in valid_sports:
            return {
                "response": f"❌ Sport non reconnu: '{activity}'. Disponibles: {', '.join(valid_sports)}",
                "playlist": None,
                "error": f"Invalid sport: {activity}"
            }
        
        mcp_result = await self.get_music_from_mcp(activity, duration)
        
        if not mcp_result:
            return {
                "response": "❌ Impossible de créer la playlist. Vérifie que le fichier archive_music_data.json existe.",
                "playlist": None,
                "error": "MCP server failed"
            }
        
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