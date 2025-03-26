PROMPT : Comment calculer les stats d'une équipe pour une saison ?

Pour calculer les statistiques d'une équipe pour une saison, vous pouvez extraire les données pertinentes à partir du fichier CSV de la saison concernée. Voici les étapes générales :

1. Charger les données de la saison
Utilisez pandas pour lire le fichier CSV contenant les données de la saison. Assurez-vous que le fichier contient les colonnes nécessaires, comme Team, W (victoires), D (matchs nuls), et M (matchs joués).

```python
import pandas as pd

# Charger les données de la saison
season_data = pd.read_csv('data/france/ligue1-2024-2025.csv')
```

2. Filtrer les données pour une équipe spécifique
Utilisez le nom de l'équipe pour filtrer les données. Vous pouvez normaliser les noms d'équipe (par exemple, en les mettant en minuscules) pour éviter les erreurs dues à des différences de casse ou d'espaces.

```python
def get_team_stats(team_name, season_data):
    """
    Récupère les statistiques d'une équipe à partir des données d'une saison.
    :param team_name: Nom de l'équipe (chaîne de caractères).
    :param season_data: Données de la saison (DataFrame pandas).
    :return: Dictionnaire contenant les statistiques de l'équipe.
    """
    # Normaliser les noms d'équipe
    team_stats = season_data[season_data['Team'].str.strip().str.lower() == team_name.strip().lower()]
    
    if team_stats.empty:
        raise ValueError(f"Team '{team_name}' not found in the dataset.")
    
    # Retourner les statistiques sous forme de dictionnaire
    return team_stats.iloc[0].to_dict()
```

3. Calculer les statistiques
Les statistiques d'une équipe peuvent inclure :

Nombre de victoires (W) : Nombre total de matchs gagnés.
Nombre de matchs nuls (D) : Nombre total de matchs terminés à égalité.
Nombre total de matchs joués (M) : Nombre total de matchs joués.
Probabilités :
- Probabilité de victoire : W / M
- Probabilité de match nul : D / M
- Probabilité de défaite : (M - W - D) / M
Voici un exemple de calcul des probabilités :

```python
def calculate_team_probabilities(team_stats):
    """
    Calcule les probabilités de victoire, de match nul et de défaite pour une équipe.
    :param team_stats: Dictionnaire contenant les statistiques de l'équipe.
    :return: Dictionnaire avec les probabilités.
    """
    total_matches = team_stats['M']
    win_prob = team_stats['W'] / total_matches
    draw_prob = team_stats['D'] / total_matches
    lose_prob = (total_matches - team_stats['W'] - team_stats['D']) / total_matches

    return {
        'win_prob': win_prob,
        'draw_prob': draw_prob,
        'lose_prob': lose_prob
    }
```

4. Exemple d'utilisation
Voici un exemple complet pour calculer les statistiques et probabilités d'une équipe :

```python
# Charger les données de la saison
season_data = pd.read_csv('data/france/ligue1-2024-2025.csv')

# Récupérer les statistiques d'une équipe
team_name = "PSG"
team_stats = get_team_stats(team_name, season_data)

# Calculer les probabilités
team_probabilities = calculate_team_probabilities(team_stats)

print(f"Statistiques pour {team_name}: {team_stats}")
print(f"Probabilités pour {team_name}: {team_probabilities}")
```

5. Exemple de sortie
Si les données pour PSG dans le fichier CSV sont les suivantes :

```python
Team,W,D,M
PSG,25,5,34
```

La sortie sera :

```
Statistiques pour PSG: {'Team': 'PSG', 'W': 25, 'D': 5, 'M': 34}
Probabilités pour PSG: {'win_prob': 0.7352941176470589, 'draw_prob': 0.14705882352941177, 'lose_prob': 0.11764705882352941}
```

6. Intégration dans votre projet
Vous pouvez intégrer ces fonctions dans votre fichier main.py pour les utiliser dans vos calculs de cotes (generate_odds, generate_current_season_odds, etc.).
