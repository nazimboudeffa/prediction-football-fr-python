import pandas as pd
from algorithms.prediction import PredictionAlgorithm

def load_data(file_path):
    try:
        # Load the CSV file into a pandas DataFrame
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file at {file_path} is empty or invalid.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the data: {e}")

def main():
    # Load the data
    data = load_data('data/france/ligue1-2023-2024.csv')
    print(type(data))  # Debugging: Check the type of the loaded data
    
    # Initialize the prediction algorithm
    predictor = PredictionAlgorithm(data)
    
    # Get user input for home and away teams
    home_team = input("Enter the home team: ")
    away_team = input("Enter the away team: ")
    
    # Generate match prediction odds
    odds = predictor.generate_odds(home_team, away_team)
    
    # Display the predicted odds
    print(f"Predicted odds for {home_team} vs {away_team}: {odds}")

if __name__ == "__main__":
    main()