# 🎵 MCP Sport & Musique - Archive.org Edition

Projet complet : Scraper + Serveur MCP pour créer des playlists personnalisées par sport.  
Source : **Archive.org** (musiques libres de droits)

---

## 📋 Vue d'ensemble

Ce projet te permet de :
- ✅ **Scraper** des musiques depuis Archive.org par catégorie de sport
- ✅ **Créer des playlists** adaptées à ton activité (course, boxe, muscu, etc.)
- ✅ **Serveur MCP** sans SDK pour intégration avec ton chatbot
- ✅ **Rechercher** des musiques par mot-clé
- ✅ **Recommandations BPM** pour chaque sport

---

## 🚀 Installation rapide

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements_v2.txt
```

Ou directement :
```bash
pip install requests beautifulsoup4
```

### 2️⃣ Scraper les données

```bash
python archive_scraper.py
```

**Options :**
- Scraping rapide (sans durées) : choix 1
- Scraping complet (avec durées) : choix 2 ⚠️ plus lent

Cela va créer le fichier `archive_music_data.json`

### 3️⃣ Tester le MCP

```bash
python test_mcp_v2.py
```

### 4️⃣ Lancer le serveur MCP

```bash
python sport_music_mcp_v2.py
```

---

## 📁 Structure du projet

```
📦 Projet MCP Sport & Musique
├── archive_scraper.py          # Scraper Archive.org optimisé
├── sport_music_mcp_v2.py       # Serveur MCP v2
├── test_mcp_v2.py              # Tests automatiques
├── requirements_v2.txt         # Dépendances Python
├── archive_music_data.json     # Données scrapées (généré)
└── README_V2.md                # Ce fichier
```

---

## 🎯 Les 5 catégories de sport

| Sport | Emoji | BPM | Description |
|-------|-------|-----|-------------|
| Course à pied | 🏃 | 140-180 | Rythme soutenu pour le running |
| Échauffement | 🧘 | 100-130 | Tempo doux pour s'étirer |
| Boxe | 🥊 | 150-190 | Rythme intense et agressif |
| Marche | 🚶 | 90-120 | Tempo calme et relaxant |
| Musculation | 💪 | 120-160 | Musique motivante pour la salle |

---

## 🛠️ Utilisation du serveur MCP

### Lancer le serveur

```bash
python sport_music_mcp_v2.py
```

### Envoyer des requêtes JSON

#### 📋 Lister les catégories
```json
{"method": "tools/call", "params": {"name": "list_categories", "arguments": {}}}
```

#### 🏃 Info sur un sport
```json
{"method": "tools/call", "params": {"name": "get_sport_info", "arguments": {"sport": "course_a_pied"}}}
```

#### 🎵 Créer une playlist de 60 min
```json
{"method": "tools/call", "params": {"name": "create_playlist", "arguments": {"sport": "course_a_pied", "duration_minutes": 60}}}
```

#### 🔍 Chercher une musique
```json
{"method": "tools/call", "params": {"name": "search_music", "arguments": {"keyword": "motivation"}}}
```

#### 🎲 Piste aléatoire
```json
{"method": "tools/call", "params": {"name": "get_random_track", "arguments": {"sport": "boxe"}}}
```

---

## 🎼 Outils MCP disponibles

| Outil | Description | Paramètres |
|-------|-------------|------------|
| `create_playlist` | Crée une playlist pour un sport | `sport`, `duration_minutes`, `shuffle` |
| `get_sport_info` | Info BPM et description | `sport` |
| `search_music` | Recherche par mot-clé | `keyword`, `sport` (optionnel), `limit` |
| `list_categories` | Liste toutes les catégories | - |
| `get_random_track` | Piste aléatoire | `sport` |
| `get_track_details` | Détails d'une piste | `identifier` |

---

## 💡 Exemples de questions utilisateur

Ton chatbot peut répondre à :

- ✅ "Fais-moi une playlist pour un footing de 1h"
- ✅ "Quelle musique pour la boxe ?"
- ✅ "Je veux m'échauffer pendant 15 min"
- ✅ "Trouve-moi des morceaux motivants pour la muscu"
- ✅ "Musique calme pour marcher 30 min"
- ✅ "Cherche-moi des pistes avec 'workout'"

---

## ⚙️ Configuration du scraper

### Modifier les catégories

Dans `archive_scraper.py`, ligne 25-31 :

```python
self.sport_categories = {
    "course_a_pied": ["running", "jogging", "cardio"],
    "yoga": ["yoga", "meditation", "zen"],  # Ajouter une catégorie
    # ...
}
```

### Modifier le nombre de pistes

Dans `archive_scraper.py`, ligne 205 :

```python
music_data = scraper.scrape_all_categories(
    tracks_per_category=20,  # Change ici
    fetch_durations=True
)
```

---

## 🔍 Structure des données JSON

```json
{
  "course_a_pied": [
    {
      "identifier": "audio_123",
      "title": "Energetic Workout",
      "artist": "Sport Beats",
      "duration": "3:45",
      "download_url": "https://archive.org/download/audio_123",
      "preview_url": "https://archive.org/embed/audio_123",
      "page_url": "https://archive.org/details/audio_123",
      "keyword": "running",
      "source": "archive.org"
    }
  ]
}
```

---

## 🐛 Résolution de problèmes

### ❌ Erreur : `ModuleNotFoundError: No module named 'requests'`

**Solution :**
```bash
pip install requests beautifulsoup4
```

Sur Windows, utilise `python` (pas `python3`) :
```bash
python -m pip install requests beautifulsoup4
```

### ⚠️ Le fichier JSON est vide

**Cause :** Le scraper n'a pas trouvé de musiques.

**Solution :**
1. Vérifie ta connexion internet
2. Archive.org peut être temporairement indisponible
3. Réessaye plus tard ou change les mots-clés dans `sport_categories`

### 🔴 Le MCP dit "Aucune piste chargée"

**Cause :** Le fichier `archive_music_data.json` n'existe pas ou est vide.

**Solution :**
```bash
python archive_scraper.py
```

### 📊 Pas assez de pistes

**Solution :** Augmente `tracks_per_category` dans le scraper ou ajoute plus de mots-clés.

---

## 🚀 Intégration avec ton backend

### Option 1 : API REST (Flask)

```python
from flask import Flask, request, jsonify
from sport_music_mcp_v2 import SportMusicMCPServer
import asyncio

app = Flask(__name__)
mcp_server = SportMusicMCPServer()

@app.route('/api/playlist', methods=['POST'])
async def create_playlist():
    data = request.json
    sport = data.get('sport')
    duration = data.get('duration', 60)
    
    result = await mcp_server.create_playlist(sport, duration)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```

### Option 2 : FastAPI

```python
from fastapi import FastAPI
from sport_music_mcp_v2 import SportMusicMCPServer

app = FastAPI()
mcp_server = SportMusicMCPServer()

@app.post("/playlist")
async def create_playlist(sport: str, duration: int = 60):
    result = await mcp_server.create_playlist(sport, duration)
    return result
```

---

## 📈 Améliorations futures

- [ ] Interface web pour visualiser les playlists
- [ ] Export en format M3U ou Spotify
- [ ] Plus de catégories (yoga, HIIT, danse, etc.)
- [ ] Filtrage par durée de piste
- [ ] Système de favoris
- [ ] Cache pour éviter de rescraper
- [ ] Support d'autres sources (YouTube Music, SoundCloud)

---

## 📄 License

Musiques provenant d'Archive.org - Vérifier les licences individuelles.  
Code du projet : Usage libre à des fins éducatives.

---

## 🤝 Contribution

Des idées ? Des bugs ? Des améliorations ?  
N'hésite pas à modifier et améliorer le code !

---

## 📞 Support

**Problème avec le scraper ?**
→ Vérifie que Archive.org est accessible

**Problème avec le MCP ?**
→ Lance d'abord `python test_mcp_v2.py` pour diagnostiquer

**Pas de musiques ?**
→ Relance le scraper avec `python archive_scraper.py`

---

## ✅ Checklist de démarrage

- [ ] Python 3.7+ installé
- [ ] Dépendances installées (`pip install -r requirements_v2.txt`)
- [ ] Scraper lancé (`python archive_scraper.py`)
- [ ] Fichier JSON créé (`archive_music_data.json`)
- [ ] Tests passés (`python test_mcp_v2.py`)
- [ ] Serveur MCP fonctionnel (`python sport_music_mcp_v2.py`)

---

**🎉 Bon coding et bon sport ! 💪🎵**
