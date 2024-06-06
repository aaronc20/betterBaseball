def default_algorithm(player_stats, team_stats):
    
    starter_avg_innings_pitched = float(player_stats["inningsPitched"])/float(player_stats["gamesPitched"])
    
    starter_portion = starter_avg_innings_pitched*float(player_stats["era"])/9
    team_portion = (9-starter_avg_innings_pitched)*float(team_stats["era"])/9
    return starter_portion + team_portion
    