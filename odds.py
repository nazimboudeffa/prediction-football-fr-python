import pandas as pd

def get_team_stats(team_name, season_data):
    # Normalize team names and handle missing data
    team_stats = season_data[season_data['Team'].str.strip().str.lower() == team_name.strip().lower()]
    if team_stats.empty:
        raise ValueError(f"Team '{team_name}' not found in the dataset.")
    return team_stats.iloc[0]

def generate_odds(home_team, away_team):
    season_2023_2024_data = pd.read_csv('data/france/ligue1-2023-2024.csv')

    home_stats = get_team_stats(home_team, season_2023_2024_data)
    away_stats = get_team_stats(away_team, season_2023_2024_data)

    home_win_prob = home_stats['W'] / 34
    away_win_prob = away_stats['W'] / 34
    draw_prob = (home_stats['D'] + away_stats['D']) / 34

    total_prob = home_win_prob + away_win_prob + draw_prob

    odds_home = round(1 / (home_win_prob / total_prob), 2) if home_win_prob > 0 else float('inf')
    odds_away = round(1 / (away_win_prob / total_prob), 2) if away_win_prob > 0 else float('inf')
    odds_draw = round(1 / (draw_prob / total_prob), 2) if draw_prob > 0 else float('inf')

    return {
        'home_win_odds': odds_home,
        'away_win_odds': odds_away,
        'draw_odds': odds_draw
    }

def generate_current_season_odds(home_team, away_team):
    # Filter data for the current season
    current_season_data = pd.read_csv('data/france/ligue1-2024-2025.csv')

    home_stats = get_team_stats(home_team, current_season_data)
    away_stats = get_team_stats(away_team, current_season_data)

    home_win_prob = home_stats['W'] / home_stats['M']
    away_win_prob = away_stats['W'] / away_stats['M']
    draw_prob = (home_stats['D'] + away_stats['D']) / (home_stats['M'] + away_stats['M'])

    total_prob = home_win_prob + away_win_prob + draw_prob

    odds_home = round(1 / (home_win_prob / total_prob), 2) if home_win_prob > 0 else float('inf')
    odds_away = round(1 / (away_win_prob / total_prob), 2) if away_win_prob > 0 else float('inf')
    odds_draw = round(1 / (draw_prob / total_prob), 2) if draw_prob > 0 else float('inf')

    return {
        'home_win_odds': odds_home,
        'away_win_odds': odds_away,
        'draw_odds': odds_draw
    }

'''
Explanation:
New Method: generate_combined_odds calculates odds by combining data from the 2023-2024 season and the current season.
- Weighting: The weight_current_season parameter allows you to adjust the importance of the current season's data relative to the previous season's data. By default, it is set to 0.6 (60% weight for the current season).
- Probability Combination: Probabilities for home wins, away wins, and draws are calculated for both seasons and then combined using the specified weights.
- Odds Calculation: The combined probabilities are used to calculate the final odds.
This method provides a more balanced prediction by considering both historical and recent performance.'
'''

def generate_combined_odds(home_team, away_team, weight_current_season=0.6):
    # Load data for the 2023-2024 season and the current season from separate CSV files
    season_2023_2024_data = pd.read_csv('data/france/ligue1-2023-2024.csv')
    current_season_data = pd.read_csv('data/france/ligue1-2024-2025.csv')

    # Get stats for both seasons
    home_stats_2023_2024 = get_team_stats(home_team, season_2023_2024_data)
    away_stats_2023_2024 = get_team_stats(away_team, season_2023_2024_data)

    home_stats_current = get_team_stats(home_team, current_season_data)
    away_stats_current = get_team_stats(away_team, current_season_data)

    # Calculate probabilities for both seasons
    home_win_prob_2023_2024 = home_stats_2023_2024['W'] / 34
    away_win_prob_2023_2024 = away_stats_2023_2024['W'] / 34
    draw_prob_2023_2024 = (home_stats_2023_2024['D'] + away_stats_2023_2024['D']) / 34

    home_win_prob_current = home_stats_current['W'] / home_stats_current['M']
    away_win_prob_current = away_stats_current['W'] / away_stats_current['M']
    draw_prob_current = (home_stats_current['D'] + away_stats_current['D']) / (
        home_stats_current['M'] + away_stats_current['M']
    )

    # Combine probabilities using weights
    home_win_prob = (
        weight_current_season * home_win_prob_current
        + (1 - weight_current_season) * home_win_prob_2023_2024
    )
    away_win_prob = (
        weight_current_season * away_win_prob_current
        + (1 - weight_current_season) * away_win_prob_2023_2024
    )
    draw_prob = (
        weight_current_season * draw_prob_current
        + (1 - weight_current_season) * draw_prob_2023_2024
    )

    total_prob = home_win_prob + away_win_prob + draw_prob

    # Calculate odds
    odds_home = round(1 / (home_win_prob / total_prob), 2) if home_win_prob > 0 else float('inf')
    odds_away = round(1 / (away_win_prob / total_prob), 2) if away_win_prob > 0 else float('inf')
    odds_draw = round(1 / (draw_prob / total_prob), 2) if draw_prob > 0 else float('inf')

    return {
        'home_win_odds': odds_home,
        'away_win_odds': odds_away,
        'draw_odds': odds_draw
    }

def main():
    print("Welcome to the Soccer Match Prediction System!")
    print("Choose the prediction algorithm:")
    print("1. Historical Season (2023-2024)")
    print("2. Current Season (2024-2025)")
    print("3. Combined (2023-2024 and Current Season)")

    # Get user choice
    choice = input("Enter the number of your choice (1, 2, or 3): ")

    # Get user input for home and away teams
    home_team = input("Enter the home team: ")
    away_team = input("Enter the away team: ")

    try:
        if choice == "1":
            # Use historical season algorithm
            odds = generate_odds(home_team, away_team)
        elif choice == "2":
            # Use current season algorithm
            odds = generate_current_season_odds(home_team, away_team)
        elif choice == "3":
            # Use combined algorithm
            odds = generate_combined_odds(home_team, away_team)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            return

        # Display the predicted odds
        print(f"Predicted odds for {home_team} vs {away_team}: {odds}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()