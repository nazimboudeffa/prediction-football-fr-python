import random
import pandas as pd

def generate_odds(teamA_name, teamB_name, data):
    """
    Génère les cotes 1X2 pour un match entre teamA et teamB.
    
    teamA_name, teamB_name : noms des équipes (chaînes)
    data : DataFrame du classement (doit contenir 'Team', 'PTS', 'Diff')
    """
    # Extraction des infos depuis le DataFrame
    teamA = data[data["Team"] == teamA_name].iloc[0]
    teamB = data[data["Team"] == teamB_name].iloc[0]

    # Score de force basé sur les points et la différence de buts
    strengthA = int(teamA["PTS"]) + int(teamA["Diff"]) * 0.3
    strengthB = int(teamB["PTS"]) + int(teamB["Diff"]) * 0.3

    # Probabilités brutes
    pA = strengthA / (strengthA + strengthB)
    pB = strengthB / (strengthA + strengthB)
    pDraw = 0.15 + 0.1 * (1 - abs(pA - pB))  # nul plus probable si forces proches

    # Normalisation
    total = pA + pB + pDraw
    pA /= total
    pB /= total
    pDraw /= total

    # Conversion en cotes décimales (1/probabilité) + marge bookmaker
    margin = 1.05
    oddsA = round((1 / pA) * margin, 2)
    oddsDraw = round((1 / pDraw) * margin, 2)
    oddsB = round((1 / pB) * margin, 2)

    return {
        "Match": f"{teamA_name} vs {teamB_name}",
        "1": oddsA,
        "X": oddsDraw,
        "2": oddsB
    }