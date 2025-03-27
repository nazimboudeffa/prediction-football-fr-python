import pandas as pd

def get_team_stats(team_name, season_data):
    # Normalize team names and handle missing data
    team_stats = season_data[season_data['Team'].str.strip().str.lower() == team_name.strip().lower()]
    if team_stats.empty:
        raise ValueError(f"Team '{team_name}' not found in the dataset.")
    return team_stats.iloc[0]

def adjust_team_stats_for_transfer(team_stats, player_impact, is_player_joining):
    # Determine the adjustment factor based on whether the player is joining or leaving
    adjustment_factor = 1 + player_impact if is_player_joining else 1 - player_impact

    # Adjust the team's statistics
    team_stats['W'] = max(0, team_stats['W'] * adjustment_factor)  # Wins
    team_stats['D'] = max(0, team_stats['D'] * adjustment_factor)  # Draws
    team_stats['M'] = max(1, team_stats['M'])  # Matches played (ensure it's at least 1)

    return team_stats

def generate_odds_with_transfert(home_team, away_team):
    # Filter data for the current season
    current_season_data = pd.read_csv('data/france/ligue1-2023-2024.csv')

    home_stats = get_team_stats(home_team, current_season_data)
    away_stats = get_team_stats(away_team, current_season_data)

    # Adjust team statistics for transfer impact
    # TODO: Implement the transfer impact logic with a CSV file for all the teams
    home_stats = adjust_team_stats_for_transfer(home_stats, 0.3, True)  # Player joining with 30% impact
    away_stats = adjust_team_stats_for_transfer(away_stats, 0.2, False)  # Player leaving with 20% impact

    home_win_prob = home_stats['W'] / home_stats['M']
    away_win_prob = away_stats['W'] / away_stats['M']
    draw_prob = (home_stats['D'] + away_stats['D']) / (home_stats['M'] + away_stats['M'])

    total_prob = home_win_prob + away_win_prob + draw_prob

    odds_home = round(1 / (home_win_prob / total_prob), 2) if home_win_prob > 0 else float('inf')
    odds_away = round(1 / (away_win_prob / total_prob), 2) if away_win_prob > 0 else float('inf')
    odds_draw = round(1 / (draw_prob / total_prob), 2) if draw_prob > 0 else float('inf')

    return {
        'home_win_odds': odds_home,
        'draw_odds': odds_draw,
        'away_win_odds': odds_away
    }

def main():   
    print("Welcome to the Soccer Match Prediction System!")

    # Get user input for home and away teams
    home_team = input("Enter the home team: ")
    away_team = input("Enter the away team: ")

    odds = generate_odds_transfert(home_team, away_team)

    # Display the predicted odds
    print(f"Predicted odds for {home_team} vs {away_team}: {odds}")

if __name__ == "__main__":
    main()