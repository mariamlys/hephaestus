#!/usr/bin/env python3
"""
Script de test complet pour le MCP Sport & Musique
"""

import asyncio
import json
from sport_music_mcp_v2 import SportMusicMCPServer


async def test_mcp():
    """Teste toutes les fonctionnalités du MCP"""
    
    print("=" * 62)
    print("   TESTS DU MCP SPORT & MUSIQUE (ARCHIVE.ORG)")
    print("=" * 62 + "\n")
    
    server = SportMusicMCPServer()
    
    # Test 1: Initialize
    print("Test 1: Initialisation du serveur")
    print("-" * 62)
    result = await server.handle_request({"method": "initialize"})
    print(f"  Protocol: {result['protocolVersion']}")
    print(f"  Server: {result['serverInfo']['name']} v{result['serverInfo']['version']}")
    print(f"  Source: {result['serverInfo']['source']}")
    
    # Test 2: Liste des outils
    print("\nTest 2: Liste des outils disponibles")
    print("-" * 62)
    result = await server.handle_request({"method": "tools/list"})
    tools = result['tools']
    print(f"  Nombre d'outils: {len(tools)}")
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool['name']}")
        print(f"     -> {tool['description']}")
    
    # Test 3: Liste des catégories
    print("\nTest 3: Liste des catégories")
    print("-" * 62)
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "list_categories",
            "arguments": {}
        }
    })
    content = json.loads(result['content'][0]['text'])
    
    if content.get('success'):
        print(f"  Total catégories: {content['total_categories']}")
        print(f"  Total pistes: {content['total_tracks']}\n")
        
        for cat in content['categories']:
            status = "OK" if cat['has_tracks'] else "VIDE"
            print(f"  [{status}] {cat['name'].replace('_', ' ').title():20} "
                  f"({cat['track_count']:3} pistes) - BPM: {cat['bpm_min']}-{cat['bpm_max']}")
    else:
        print(f"  {content.get('error', 'Erreur inconnue')}")
    
    # Test 4: Info sur un sport
    print("\nTest 4: Informations sur la course à pied")
    print("-" * 62)
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "get_sport_info",
            "arguments": {"sport": "course_a_pied"}
        }
    })
    content = json.loads(result['content'][0]['text'])
    
    if content.get('success'):
        print(f"  Sport: {content['sport']}")
        print(f"  BPM: {content['bpm_min']}-{content['bpm_max']}")
        print(f"  Description: {content['description']}")
        print(f"  Pistes disponibles: {content['available_tracks']}")
    else:
        print(f"  {content.get('error', 'Erreur')}")
    
    # Test 5: Créer une playlist
    print("\nTest 5: Création d'une playlist (30 min de course)")
    print("-" * 62)
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "create_playlist",
            "arguments": {
                "sport": "course_a_pied",
                "duration_minutes": 30,
                "shuffle": True
            }
        }
    })
    content = json.loads(result['content'][0]['text'])
    
    if content.get('success'):
        print(f"  Sport: {content['sport']}")
        print(f"  Durée cible: {content['target_duration_min']} min")
        print(f"  Durée réelle: {content['actual_duration_min']} min ({content['actual_duration_formatted']})")
        print(f"  Nombre de pistes: {content['track_count']} ({content['unique_tracks']} uniques)")
        print(f"  BPM recommandé: {content['bpm_range']}")
        print(f"  {content['recommendation']}")
        
        if content.get('playlist') and len(content['playlist']) > 0:
            print("\n  Premières pistes:")
            for i, track in enumerate(content['playlist'][:5], 1):
                duration = track.get('duration', 'N/A')
                print(f"    {i}. {track['title'][:50]}")
                print(f"       {track['artist'][:40]} ({duration})")
    else:
        print(f"  {content.get('error', 'Erreur')}")
    
    # Test 6: Recherche
    print("\nTest 6: Recherche de musique avec 'workout'")
    print("-" * 62)
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "search_music",
            "arguments": {"keyword": "workout", "limit": 5}
        }
    })
    content = json.loads(result['content'][0]['text'])
    
    if content.get('success'):
        print(f"  Résultats: {content['results_count']} pistes trouvées")
        print(f"  Affichage: {content['showing']} premiers résultats\n")
        
        for i, track in enumerate(content['tracks'][:3], 1):
            cat = track['category'].replace('_', ' ').title()
            print(f"    {i}. {track['title'][:45]}")
            print(f"       {track['artist'][:40]} - Catégorie: {cat}")
    else:
        print(f"  {content.get('error', 'Erreur')}")
    
    # Test 7: Piste aléatoire
    print("\nTest 7: Piste aléatoire pour la boxe")
    print("-" * 62)
    result = await server.handle_request({
        "method": "tools/call",
        "params": {
            "name": "get_random_track",
            "arguments": {"sport": "boxe"}
        }
    })
    content = json.loads(result['content'][0]['text'])
    
    if content.get('success'):
        track = content['track']
        print(f"  Sport: {content['sport']}")
        print(f"  Titre: {track['title']}")
        print(f"  Artiste: {track['artist']}")
        print(f"  Durée: {track.get('duration', 'N/A')}")
    else:
        print(f"  {content.get('error', 'Erreur')}")
    
    # Résumé
    print("\n" + "=" * 62)
    print("Tous les tests terminés avec succès!")
    print("=" * 62)


if __name__ == "__main__":
    asyncio.run(test_mcp())
