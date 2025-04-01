import pandas as pd
from algorithms import get_season_data, generate_odds_with_home_away_adjustment, generate_combined_odds_with_home_away_adjustment

def main():
    file_1_path = "data/france/ligue1-2023-2024.csv"
    file_2_path = "data/france/ligue1-2024-2025.csv"
    # Load the historical season data
    # season_file_1 = "historical_season_2023_2024.csv"
    # season_file_2 = "current_season_2024_2025.csv"
    season_data_1 = get_season_data(file_1_path)
    season_data_2 = get_season_data(file_2_path)  

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
            odds = generate_odds_with_home_away_adjustment(home_team, away_team, season_data_1)
        elif choice == "2":
            # Use current season algorithm
            odds = generate_odds_with_home_away_adjustment(home_team, away_team, season_data_2)
        elif choice == "3":
            # Use combined algorithm
            odds = generate_combined_odds_with_home_away_adjustment(home_team, away_team, season_data_1, season_data_2)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            return

        # Display the predicted odds
        print(f"Predicted odds for {home_team} vs {away_team}: {odds}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()