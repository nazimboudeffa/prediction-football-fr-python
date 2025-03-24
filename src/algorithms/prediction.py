import pandas as pd

class PredictionAlgorithm:
    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("The data provided must be a pandas DataFrame.")
        self.data = data

    def get_team_stats(self, team_name, season_data):
        # Normalize team names and handle missing data
        team_stats = season_data[season_data['Team'].str.strip().str.lower() == team_name.strip().lower()]
        if team_stats.empty:
            raise ValueError(f"Team '{team_name}' not found in the dataset.")
        return team_stats.iloc[0]

    def generate_odds(self, home_team, away_team):
        home_stats = self.get_team_stats(home_team, self.data)
        away_stats = self.get_team_stats(away_team, self.data)

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
    
    def generate_current_season_odds(self, home_team, away_team):
        # Filter data for the current season
        current_season_data = self.data[self.data['Season'] == '2023-2024']

        home_stats = current_season_data[current_season_data['Team'] == home_team].iloc[0]
        away_stats = current_season_data[current_season_data['Team'] == away_team].iloc[0]

        home_win_prob = home_stats['W'] / home_stats['Matches_Played']
        away_win_prob = away_stats['W'] / away_stats['Matches_Played']
        draw_prob = (home_stats['D'] + away_stats['D']) / (home_stats['Matches_Played'] + away_stats['Matches_Played'])

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
    
    def generate_combined_odds(self, home_team, away_team, weight_current_season=0.6):
        # Filter data for the 2023-2024 season and the current season
        season_2023_2024_data = self.data[self.data['Season'] == '2023-2024']
        current_season_data = self.data[self.data['Season'] == '2024-2025']

        # Get stats for both seasons
        home_stats_2023_2024 = season_2023_2024_data[season_2023_2024_data['Team'] == home_team].iloc[0]
        away_stats_2023_2024 = season_2023_2024_data[season_2023_2024_data['Team'] == away_team].iloc[0]

        home_stats_current = current_season_data[current_season_data['Team'] == home_team].iloc[0]
        away_stats_current = current_season_data[current_season_data['Team'] == away_team].iloc[0]

        # Calculate probabilities for both seasons
        home_win_prob_2023_2024 = home_stats_2023_2024['W'] / 34
        away_win_prob_2023_2024 = away_stats_2023_2024['W'] / 34
        draw_prob_2023_2024 = (home_stats_2023_2024['D'] + away_stats_2023_2024['D']) / 34

        home_win_prob_current = home_stats_current['W'] / home_stats_current['Matches_Played']
        away_win_prob_current = away_stats_current['W'] / away_stats_current['Matches_Played']
        draw_prob_current = (home_stats_current['D'] + away_stats_current['D']) / (
            home_stats_current['Matches_Played'] + away_stats_current['Matches_Played']
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