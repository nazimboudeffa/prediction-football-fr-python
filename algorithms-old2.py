def calc_forces(stats):
    """
    stats : dict { equipe: { 'buts_pour': int, 'buts_contre': int, 'matchs': int } }
    Retourne attaque et défense moyennes normalisées
    """
    forces = {}
    # Moyennes de la ligue
    avg_attack = sum([s['buts_pour']/s['matchs'] for s in stats.values()]) / len(stats)
    avg_defense = sum([s['buts_contre']/s['matchs'] for s in stats.values()]) / len(stats)

    for team, s in stats.items():
        attaque = (s['buts_pour']/s['matchs']) / avg_attack
        defense = (s['buts_contre']/s['matchs']) / avg_defense
        forces[team] = {'attaque': attaque, 'defense': defense}
    return forces

def calc_prob(team_home, team_away, forces):
    """
    Compare deux équipes et retourne probabilités & cotes
    """
    att_home, def_home = forces[team_home]['attaque'], forces[team_home]['defense']
    att_away, def_away = forces[team_away]['attaque'], forces[team_away]['defense']

    # Score relatif (plus haut = meilleure chance de gagner)
    score_home = att_home / def_away
    score_away = att_away / def_home

    # Bonus domicile (classique en foot)
    score_home *= 1.2

    total = score_home + score_away
    p_home = score_home / total
    p_away = score_away / total

    # probabilité du nul comme moyenne pondérée
    p_draw = 0.25 * (p_home + p_away)
    # ajustement pour que somme = 1
    norm = p_home + p_draw + p_away
    p_home, p_draw, p_away = p_home/norm, p_draw/norm, p_away/norm

    return {
        "prob_home": round(p_home, 3),
        "prob_draw": round(p_draw, 3),
        "prob_away": round(p_away, 3),
        "odds_home": round(1/p_home, 2),
        "odds_draw": round(1/p_draw, 2),
        "odds_away": round(1/p_away, 2),
    }

# ---- Exemple fictif ----
stats = {
    "PSG": {"buts_pour": 92, "buts_contre": 35, "matchs": 34},
    "Marseille": {"buts_pour": 74, "buts_contre": 47, "matchs": 34}
}

forces = calc_forces(stats)
cotes = calc_prob("PSG", "Marseille", forces)
print(cotes)

def calc_prob_from_ranking(home, away, classement, bonus_home=1.1):
    """
    home, away : noms des équipes
    classement : dict {equipe: points}
    bonus_home : multiplicateur pour l’avantage domicile
    """
    points_home = classement[home]
    points_away = classement[away]

    # Force basée sur les points
    score_home = points_home * bonus_home
    score_away = points_away

    # Probabilités brutes (sans nul)
    p_home = score_home / (score_home + score_away)
    p_away = 1 - p_home

    # Probabilité du nul (fixe, ex: 25% du total)
    p_draw = 0.25
    # On réduit home/away proportionnellement pour faire de la place
    p_home *= (1 - p_draw)
    p_away *= (1 - p_draw)

    # Cotes = inverse probabilité
    return {
        "prob_home": round(p_home, 3),
        "prob_draw": round(p_draw, 3),
        "prob_away": round(p_away, 3),
        "odds_home": round(1/p_home, 2),
        "odds_draw": round(1/p_draw, 2),
        "odds_away": round(1/p_away, 2)
    }

# ---- Exemple fictif avec le classement final 2024-2025 ----
classement = {
    "PSG": 84,
    "Marseille": 65,
    "Monaco": 61,
    "Nice": 60,
    "Lille": 60,
    "Lyon": 57
}

cotes = calc_prob_from_ranking("PSG", "Marseille", classement)
print(cotes)