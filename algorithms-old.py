import pandas as pd

def get_season_data(season_file):
    """
    Load season data from a CSV file.

    Parameters:
    - season_file (str): Path to the season data file.

    Returns:
    - pd.DataFrame: The loaded season data.
    """
    try:
        season_data = pd.read_csv(season_file)
        return season_data
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{season_file}' not found.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"File '{season_file}' is empty or invalid.")
    except Exception as e:
        raise ValueError(f"An error occurred while loading the file: {e}")

def get_team_stats(team_name, season_data):
    team_stats = season_data[season_data['Team'].str.strip().str.lower() == team_name.strip().lower()]
    if team_stats.empty:
        raise ValueError(f"Team '{team_name}' not found in the dataset.")
    return team_stats.iloc[0]

def calculate_probabilities(home_stats, away_stats):
    """
    Calculate probabilities for home win, away win, and draw.

    Parameters:
    - home_stats (pd.Series): Stats for the home team.
    - away_stats (pd.Series): Stats for the away team.

    Returns:
    - tuple: (home_win_prob, draw_prob, away_win_prob)
    """
    home_win_prob = home_stats['W'] / home_stats['M']
    away_win_prob = away_stats['W'] / away_stats['M']
    draw_prob = (home_stats['D'] + away_stats['D']) / (home_stats['M'] + away_stats['M'])

    return home_win_prob, draw_prob, away_win_prob

def calculate_odds(home_win_prob, draw_prob, away_win_prob):
    """
    Calculate odds from probabilities.

    Parameters:
    - home_win_prob (float): Probability of a home win.
    - draw_prob (float): Probability of a draw.
    - away_win_prob (float): Probability of an away win.

    Returns:
    - dict: A dictionary containing the calculated odds.
    """
    total_prob = home_win_prob + draw_prob + away_win_prob

    odds_home = round(1 / (home_win_prob / total_prob), 2) if home_win_prob > 0 else float('inf')
    odds_draw = round(1 / (draw_prob / total_prob), 2) if draw_prob > 0 else float('inf')
    odds_away = round(1 / (away_win_prob / total_prob), 2) if away_win_prob > 0 else float('inf')

    return {
        'home_win_odds': odds_home,
        'draw_odds': odds_draw,
        'away_win_odds': odds_away
    }

def adjust_probs_for_home_away(home_win_prob, draw_prob, away_win_prob, home_advantage=0.1, away_advantage=-0.05):
    """
    Adjust the odds based on whether a team is playing at home or away.

    Parameters:
    - home_win_prob (float): Probability of a home win.
    - draw_prob (float): Probability of a draw.
    - away_win_prob (float): Probability of an away win.
    - home_advantage (float): Multiplier for home advantage (default is 0.1).
    - away_advantage (float): Multiplier for away advantage (default is -0.05).

    Returns:
    - tuple: Adjusted probabilities (home_win_prob, draw_prob, away_win_prob).
    """
    # Apply home advantage multiplier
    adjusted_home_win_prob = home_win_prob + home_advantage
    adjusted_away_win_prob = away_win_prob + away_advantage

    return adjusted_home_win_prob, draw_prob, adjusted_away_win_prob

def calculate_odds2(home_win_prob, draw_prob, away_win_prob, epsilon=1e-6):
    """
    Calculate odds from probabilities with safety for zero probabilities.
    Always ensures finite odds.
    """

    # Convert to float and apply epsilon
    home_win_prob = float(home_win_prob) if home_win_prob else 0.0
    draw_prob = float(draw_prob) if draw_prob else 0.0
    away_win_prob = float(away_win_prob) if away_win_prob else 0.0

    # Replace zeros with epsilon
    if home_win_prob <= 0: home_win_prob = epsilon
    if draw_prob <= 0: draw_prob = epsilon
    if away_win_prob <= 0: away_win_prob = epsilon

    # Normalize so total = 1
    total = home_win_prob + draw_prob + away_win_prob
    home_win_prob /= total
    draw_prob /= total
    away_win_prob /= total

    # Calculate odds
    odds_home = round(1 / home_win_prob, 2)
    odds_draw = round(1 / draw_prob, 2)
    odds_away = round(1 / away_win_prob, 2)

    return {
        "home_win_odds": odds_home,
        "draw_odds": odds_draw,
        "away_win_odds": odds_away,
    }

def generate_odds(home_team, away_team, season_data):
    home_stats = get_team_stats(home_team, season_data)
    away_stats = get_team_stats(away_team, season_data)

    home_win_prob, draw_prob, away_win_prob = calculate_probabilities(home_stats, away_stats)
    return calculate_odds(home_win_prob, draw_prob, away_win_prob)

def generate_odds_with_home_away_adjustment(home_team, away_team, season_data, home_advantage=0.1, away_advantage=-0.05):
    """
    Generate odds for a match between two teams with home and away adjustments.

    Parameters:
    - home_team (str): Name of the home team.
    - away_team (str): Name of the away team.
    - season_data (pd.DataFrame): DataFrame containing the season data.
    - home_advantage (float): Multiplier for home advantage (default is 0.1).
    - away_advantage (float): Multiplier for away advantage (default is -0.05).
    Returns:
    - dict: A dictionary containing the adjusted odds.
    """
    home_stats = get_team_stats(home_team, season_data)
    away_stats = get_team_stats(away_team, season_data)

    home_win_prob, draw_prob, away_win_prob = calculate_probabilities(home_stats, away_stats)
    
    # Adjust odds based on home and away advantages
    adjusted_home_win_prob, adjusted_draw_prob, adjusted_away_win_prob = adjust_probs_for_home_away(
        home_win_prob, draw_prob, away_win_prob, home_advantage, away_advantage
    )

    return calculate_odds(adjusted_home_win_prob, adjusted_draw_prob, adjusted_away_win_prob)


def generate_combined_odds(home_team, away_team, season_file_1, season_file_2, weight_current_season=0.6):
    season_1_data = pd.read_csv(season_file_1)
    season_2_data = pd.read_csv(season_file_2)

    home_stats_1 = get_team_stats(home_team, season_1_data)
    away_stats_1 = get_team_stats(away_team, season_1_data)

    home_stats_2 = get_team_stats(home_team, season_2_data)
    away_stats_2 = get_team_stats(away_team, season_2_data)

    home_win_prob_1, draw_prob_1, away_win_prob_1 = calculate_probabilities(home_stats_1, away_stats_1)
    home_win_prob_2, draw_prob_2, away_win_prob_2 = calculate_probabilities(home_stats_2, away_stats_2)

    home_win_prob = weight_current_season * home_win_prob_2 + (1 - weight_current_season) * home_win_prob_1
    draw_prob = weight_current_season * draw_prob_2 + (1 - weight_current_season) * draw_prob_1
    away_win_prob = weight_current_season * away_win_prob_2 + (1 - weight_current_season) * away_win_prob_1

    return calculate_odds(home_win_prob, draw_prob, away_win_prob)

def generate_combined_odds_with_home_away_adjustment(home_team, away_team, season_file_1, season_file_2, weight_current_season=0.6, home_advantage=1.1):
    season_1_data = get_season_data(season_file_1)
    season_2_data = get_season_data(season_file_2)

    home_stats_1 = get_team_stats(home_team, season_1_data)
    away_stats_1 = get_team_stats(away_team, season_1_data)

    home_stats_2 = get_team_stats(home_team, season_2_data)
    away_stats_2 = get_team_stats(away_team, season_2_data)

    home_win_prob_1, draw_prob_1, away_win_prob_1 = calculate_probabilities(home_stats_1, away_stats_1)
    home_win_prob_2, draw_prob_2, away_win_prob_2 = calculate_probabilities(home_stats_2, away_stats_2)

    home_win_prob = weight_current_season * home_win_prob_2 + (1 - weight_current_season) * home_win_prob_1
    draw_prob = weight_current_season * draw_prob_2 + (1 - weight_current_season) * draw_prob_1
    away_win_prob = weight_current_season * away_win_prob_2 + (1 - weight_current_season) * away_win_prob_1

    home_win_prob, draw_prob, away_win_prob = adjust_odds_for_home_away(
        home_win_prob, draw_prob, away_win_prob, home_advantage
    )
    return calculate_odds(home_win_prob, draw_prob, away_win_prob)