import requests, json
import time

from prediction_algorithms import default_algorithm

BASE_URL = "https://statsapi.mlb.com/api/v1/"
BASE_URL_ALT = "https://statsapi.mlb.com/api/v1.1/"

def predictScore(pitcherID, teamID):

    # load player stats, team stats
        # player stats
        # https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=season&group=all
        # 
        # team stats
        # https://statsapi.mlb.com/api/v1/teams/{teamId}/stats?stats=season&group=pitching

    player_stats = json.loads(requests.get(BASE_URL + "/people/" + str(pitcherID)\
                                     + "/stats?stats=season&group=pitching").text)["stats"][0]["splits"][0]["stat"]
    team_stats = json.loads(requests.get(BASE_URL + "/teams/" + str(teamID)\
                                  + "/stats?stats=season&group=pitching").text)["stats"][0]["splits"][0]["stat"]
    
    return default_algorithm(player_stats, team_stats)

# predict the score of a game, given a gamePk.
def process_game(gamePk):

    result = ""

    # https://statsapi.mlb.com/api/v1.1/game/{gamePk}/feed/live
    game_url = BASE_URL_ALT + "/game/" + str(gamePk) + "/feed/live"
    game_data = json.loads(requests.get(game_url).text)
    
    game_teams = game_data["gameData"]["teams"]
    game_pitchers = json.loads(requests.get(game_url).text)["gameData"]["probablePitchers"]

    if "away" in game_pitchers and "home" in game_pitchers:
        result = result + game_teams["away"]["teamName"] + " (" + (game_pitchers["away"]["fullName"] if "away" in game_pitchers else "None")  + ") @ "
        result = result + game_teams["home"]["teamName"] + " (" + (game_pitchers["home"]["fullName"] if "home" in game_pitchers else "None") + ")."
        

        result = result + " Predicted score: " + \
            str(round(predictScore(game_pitchers["away"]["id"], game_teams["away"]["id"])+ \
                              predictScore(game_pitchers["home"]["id"], game_teams["home"]["id"]), 2))
    
    else:
        result = result + game_teams["away"]["teamName"] + " @ " + game_teams["home"]["teamName"] + ", one or more SP not announced."
    return result


def todays_slate(date):

    s_time = time.time()
    result = ""
    slate_url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=" + date

    # grabs and parses so we have a list of games
    slate = json.loads(requests.get(slate_url).text)["dates"][0]["games"]

    for game in slate:
        result = result + process_game(game["gamePk"]) + "\n"

    result = result + "Time Taken: " + str(round(time.time()-s_time, 2)) + " seconds."
    return result

date = "2024-06-03"
print(todays_slate(date))