import pandas as pd

def get_team_stats(team_name, season_data):
    """
    Récupère les statistiques d'une équipe à partir des données d'une saison.
    :param team_name: Nom de l'équipe (chaîne de caractères).
    :param season_data: Données de la saison (DataFrame pandas).
    :return: Dictionnaire contenant les statistiques de l'équipe.
    """
    # Normaliser les noms d'équipe
    team_stats = season_data[season_data['Equipes'].str.strip().str.lower() == team_name.strip().lower()]
    
    if team_stats.empty:
        raise ValueError(f"Team '{team_name}' not found in the dataset.")
    
    # Retourner les statistiques sous forme de dictionnaire
    return team_stats.iloc[0].to_dict()

def calculate_team_probabilities(team_stats):
    """
    Calcule les probabilités de victoire, de match nul et de défaite pour une équipe.
    :param team_stats: Dictionnaire contenant les statistiques de l'équipe.
    :return: Dictionnaire avec les probabilités.
    """
    total_matches = team_stats['J']
    win_prob = team_stats['G'] / total_matches
    draw_prob = team_stats['N'] / total_matches
    lose_prob = (total_matches - team_stats['G'] - team_stats['N']) / total_matches

    return {
        'win_prob': win_prob,
        'lose_prob': lose_prob,
        'draw_prob': draw_prob
    }

def generate_odds(home_team, away_team, season_data):
    """
    Génère les cotes pour un match entre deux équipes en utilisant les données de la saison actuelle.
    :param home_team: Nom de l'équipe à domicile.
    :param away_team: Nom de l'équipe à l'extérieur.
    :param season_data: Données de la saison actuelle (DataFrame pandas).
    :return: Dictionnaire contenant les cotes.
    """
    # Récupérer les statistiques des deux équipes
    home_stats = get_team_stats(home_team, season_data)
    away_stats = get_team_stats(away_team, season_data)

    # Calculer les probabilités pour chaque équipe
    home_probs = calculate_team_probabilities(home_stats)
    away_probs = calculate_team_probabilities(away_stats)

    # Calculer les cotes (inverse des probabilités)
    home_win_odds = round(1 / home_probs['win_prob'], 2)
    away_win_odds = round(1 / away_probs['win_prob'], 2)
    draw_odds = round(1 / ((home_probs['draw_prob'] + away_probs['draw_prob']) / 2), 2)

    return {
        'home_win_odds': home_win_odds,
        'draw_odds': draw_odds,
        'away_win_odds': away_win_odds
    }

def load_season_data(file_path):
    """
    Charge les données d'une saison à partir d'un fichier CSV.
    :param file_path: Chemin vers le fichier CSV.
    :return: DataFrame pandas contenant les données de la saison.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier '{file_path}' est introuvable.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Le fichier '{file_path}' est vide ou corrompu.")

def main():
    # Demander à l'utilisateur de saisir les équipes
    home_team = input("Entrez le nom de l'équipe à domicile : ").strip()
    away_team = input("Entrez le nom de l'équipe à l'extérieur : ").strip()

    # Construire le chemin du fichier CSV en fonction de la saison
    file_path = "data/algeria/d1-2024-2025.csv"

    try:
        # Charger les données de la saison
        season_data = load_season_data(file_path)

        # Générer les cotes pour le match
        odds = generate_odds(home_team, away_team, season_data)

        print(f"\nCotes pour {home_team} vs {away_team} ({2024-2025}): {odds}")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()