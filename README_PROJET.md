# 🎵 MCP Sport & Musique - Chatbot avec Scraping Pixabay

Un serveur MCP complet pour créer des playlists personnalisées par sport, utilisant des musiques scrapées depuis Pixabay Music.

## 📋 Fonctionnalités

- **Scraping automatique** de Pixabay Music par catégorie de sport
- **5 catégories** : Course à pied, Échauffement, Boxe, Marche à pied, Musculation
- **Création de playlists** adaptées à la durée et au sport
- **Recommandations BPM** par type d'activité
- **Recherche** de musiques par mot-clé
- **Stockage JSON** des données

## 🚀 Installation

### Prérequis
- Python 3.7+
- pip

### Dépendances

```bash
pip install requests beautifulsoup4
```

Ou avec le fichier requirements :
```bash
pip install -r requirements.txt
```

## 📁 Structure du projet

```
├── pixabay_scraper.py        # Script de scraping
├── sport_music_mcp.py         # Serveur MCP
├── test_mcp.py                # Tests
├── pixabay_music_data.json    # Données scrapées (généré)
└── README.md
```

## 🔧 Utilisation

### Étape 1 : Scraper les données

```bash
python3 pixabay_scraper.py
```

Cela va :
- Scraper Pixabay Music pour chaque catégorie de sport
- Sauvegarder les résultats dans `pixabay_music_data.json`
- Afficher un résumé des pistes trouvées

**⚠️ Note importante** : Le script contient des sélecteurs CSS génériques. Tu devras probablement les adapter selon la structure HTML réelle de Pixabay. Inspecte la page avec F12 pour voir les vrais sélecteurs.

### Étape 2 : Tester le MCP

```bash
python3 test_mcp.py
```

### Étape 3 : Utiliser le MCP

```bash
python3 sport_music_mcp.py
```

Ensuite, envoie des requêtes JSON :

#### Créer une playlist pour 1h de course
```json
{"method": "tools/call", "params": {"name": "create_playlist", "arguments": {"sport": "course_a_pied", "duration_minutes": 60}}}
```

#### Lister les catégories
```json
{"method": "tools/call", "params": {"name": "list_categories", "arguments": {}}}
```

#### Info sur un sport
```json
{"method": "tools/call", "params": {"name": "get_sport_info", "arguments": {"sport": "boxe"}}}
```

#### Chercher une musique
```json
{"method": "tools/call", "params": {"name": "search_music", "arguments": {"keyword": "energy"}}}
```

## 🎯 Exemples de questions utilisateur

Le chatbot peut répondre à :
- "Fais-moi une playlist pour un footing de 1h"
- "Quelle musique pour la boxe ?"
- "Je veux m'échauffer pendant 15 min"
- "Trouve-moi des morceaux motivants pour la muscu"
- "Musique calme pour marcher 30 min"

## 🛠️ Outils MCP disponibles

| Outil | Description | Paramètres |
|-------|-------------|------------|
| `create_playlist` | Crée une playlist pour un sport | `sport`, `duration_minutes` |
| `get_sport_info` | Info BPM et description d'un sport | `sport` |
| `search_music` | Recherche par mot-clé | `keyword`, `sport` (optionnel) |
| `list_categories` | Liste toutes les catégories | - |
| `get_random_track` | Piste aléatoire | `sport` |

## 🎵 Catégories et BPM recommandés

| Sport | BPM | Description |
|-------|-----|-------------|
| Course à pied | 140-180 | Rythme soutenu pour la course |
| Échauffement | 100-130 | Tempo doux pour l'échauffement |
| Boxe | 150-190 | Rythme intense pour la boxe |
| Marche à pied | 90-120 | Tempo calme pour la marche |
| Musculation | 120-160 | Rythme motivant pour la muscu |

## 🔍 Adapter le scraper

Le scraper utilise des sélecteurs CSS génériques. Voici comment les adapter :

1. Ouvre https://pixabay.com/fr/music/ dans ton navigateur
2. Fais clic droit > Inspecter (F12)
3. Trouve les éléments HTML des musiques
4. Remplace dans `pixabay_scraper.py` :

```python
# Exemple à adapter selon Pixabay
music_items = soup.find_all('div', class_='VRAI_NOM_DE_CLASSE')
title = item.find('h2', class_='VRAI_NOM_TITRE')
# etc.
```

## 📊 Format des données JSON

```json
{
  "course_a_pied": [
    {
      "title": "Energetic Workout",
      "artist": "John Doe",
      "duration": "3:45",
      "download_url": "https://...",
      "page_url": "https://...",
      "tags": ["energetic", "workout"],
      "keyword": "running"
    }
  ]
}
```

## 🚧 Améliorations possibles

- [ ] Ajouter plus de catégories de sport
- [ ] Filtrer par BPM réel (si disponible sur Pixabay)
- [ ] Export de playlist en M3U
- [ ] Interface web pour le scraper
- [ ] Cache des données scrapées
- [ ] Intégration avec d'autres sources musicales

## ⚠️ Avertissements

- **Respecte les conditions d'utilisation de Pixabay**
- Ajoute des délais entre les requêtes (déjà inclus : 2s)
- Ne surcharge pas leurs serveurs
- Les données sont pour usage personnel

## 📝 License

Ce projet est fourni tel quel, à des fins éducatives.

## 🤝 Contribution

Pour intégrer ce MCP dans ton chatbot :

1. Lance le serveur MCP
2. Connecte-le à ton backend (API REST ou autre)
3. Utilise les outils MCP pour répondre aux questions utilisateur
4. Ton frontend envoie les questions → backend → MCP → réponse

## 📞 Support

Si tu as des questions ou besoin d'aide pour :
- Adapter les sélecteurs CSS
- Intégrer avec ton backend
- Ajouter de nouvelles fonctionnalités

N'hésite pas !
