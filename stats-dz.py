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
        'draw_prob': draw_prob,
        'lose_prob': lose_prob
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
    # Demander à l'utilisateur de saisir la saison et l'équipe
    season = input("Entrez la saison (par exemple, '2024-2025'): ").strip()
    team_name = input("Entrez le nom de l'équipe : ").strip()

    # Construire le chemin du fichier CSV en fonction de la saison
    file_path = "data/algeria/d1-2024-2025.csv"

    try:
        # Charger les données de la saison
        season_data = load_season_data(file_path)

        # Récupérer les statistiques de l'équipe
        team_stats = get_team_stats(team_name, season_data)

        # Calculer les probabilités
        team_probabilities = calculate_team_probabilities(team_stats)

        print(f"\nStatistiques pour {team_name} ({season}): {team_stats}")
        print(f"Probabilités pour {team_name} ({season}): {team_probabilities}")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()