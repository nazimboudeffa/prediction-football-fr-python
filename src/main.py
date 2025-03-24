import pandas as pd
from utils.data_loader import load_data
from algorithms.prediction import PredictionAlgorithm

def main():
    # Load the data
    data = load_data('data/france/ligue1-2023-2024.csv')
    
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