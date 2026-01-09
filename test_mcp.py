#!/usr/bin/env python3
"""
Script de test pour le MCP Sport & Musique
"""

import asyncio
import json
from sport_music_mcp import SportMusicMCPServer

async def test_mcp():
    """Teste toutes les fonctionnalités du MCP"""
    
    print("🧪 TESTS DU MCP SPORT & MUSIQUE")
    print("=" * 60)
    
    server = SportMusicMCPServer()
    
    # Test 1: Initialize
    print("\n✅ Test 1: Initialize")
    result = await server.handle_request({"method": "initialize"})
    print(json.dumps(result, indent=2))
    
    # Test 2: Liste des outils
    print("\n✅ Test 2: Liste des outils")
    result = await server.handle_request({"method": "tools/list"})
    print(f"Nombre d'outils: {len(result['tools'])}")
    for tool in result['tools']:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # Test 3: Liste des catégories
    print("\n✅ Test 3: Liste des catégories")
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "list_categories",
            "arguments": {}
        }
    })
    print(result['content'][0]['text'])
    
    # Test 4: Info sur un sport
    print("\n✅ Test 4: Info sur la course à pied")
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "get_sport_info",
            "arguments": {"sport": "course_a_pied"}
        }
    })
    print(result['content'][0]['text'])
    
    # Test 5: Créer une playlist
    print("\n✅ Test 5: Créer une playlist pour 30min de course")
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "create_playlist",
            "arguments": {
                "sport": "course_a_pied",
                "duration_minutes": 30
            }
        }
    })
    content = json.loads(result['content'][0]['text'])
    print(f"Sport: {content.get('sport')}")
    print(f"Durée cible: {content.get('target_duration_min')} min")
    print(f"Durée réelle: {content.get('actual_duration_min')} min")
    print(f"Nombre de pistes: {content.get('track_count')}")
    print(f"BPM recommandé: {content.get('bpm_range')}")
    
    if content.get('playlist'):
        print("\nPremières pistes:")
        for i, track in enumerate(content['playlist'][:3], 1):
            print(f"  {i}. {track['title']} - {track['artist']} ({track['duration']})")
    
    # Test 6: Recherche
    print("\n✅ Test 6: Recherche de musique avec 'energy'")
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "search_music",
            "arguments": {"keyword": "energy"}
        }
    })
    content = json.loads(result['content'][0]['text'])
    print(f"Résultats trouvés: {content.get('results_count')}")
    
    # Test 7: Piste aléatoire
    print("\n✅ Test 7: Piste aléatoire pour la boxe")
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "get_random_track",
            "arguments": {"sport": "boxe"}
        }
    })
    print(result['content'][0]['text'])
    
    print("\n" + "=" * 60)
    print("✅ Tous les tests terminés!")


if __name__ == "__main__":
    asyncio.run(test_mcp())
