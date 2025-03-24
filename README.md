# Soccer Prediction Project

This project is designed to predict match odds for Ligue 1 football matches based on historical data from the 2023-2024 season. The predictions are generated using a custom algorithm that analyzes team performance statistics.

## Project Structure

```
soccer-prediction
├── data
│   └── ligue1-2023-2024.csv
├── src
│   ├── main.py
│   ├── algorithms
│   │   └── prediction.py
│   └── utils
│       └── data_loader.py
├── requirements.txt
└── README.md
```

## Files Description

- **data/ligue1-2023-2024.csv**: Contains match results and statistics for the Ligue 1 2023-2024 season, including team names, wins, draws, losses, goals scored, goals against, and points.

- **src/main.py**: The entry point of the application. It handles user input for home and away teams and calls the prediction algorithm to generate match odds.

- **src/algorithms/prediction.py**: Contains the `PredictionAlgorithm` class with a method `generate_odds(home_team, away_team)` that calculates and returns the predicted odds based on the historical data from the CSV file.

- **src/utils/data_loader.py**: Exports a function `load_data(filepath)` that reads the CSV file and returns the data in a structured format for use in the prediction algorithm.

- **requirements.txt**: Lists the dependencies required for the project, such as pandas for data manipulation.

## Setup Instructions

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:

   ```
   python src/main.py
   ```

5. Follow the prompts to input the home and away teams for which you want to generate match prediction odds.

## Usage

After running the application, you will be prompted to enter the names of the home and away teams. The application will then use the historical data to generate and display the predicted odds for the match.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or additional features.