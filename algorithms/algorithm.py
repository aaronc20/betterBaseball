import httpx, asyncio

# https://statsapi.mlb.com/api/v1.1/game/{gamePk}/feed/live
URL = lambda x: "https://statsapi.mlb.com/api/v1.1/game/" + str(x) + "/feed/live"

class Algorithm:
    
    def __init__(self, game):
        self.game = game
        self.game_data = httpx.get(URL(game)).json()

        self.away_team = self.game_data["gameData"]["teams"]["away"]["id"]
        self.away_batting_order = self.game_data["liveData"]["boxscore"]["teams"]["away"]["batters"]
        self.away_starting_pitcher = self.away_batting_order.pop()

        self.home_team = self.game_data["gameData"]["teams"]["home"]["id"]
        self.home_batting_order = self.game_data["liveData"]["boxscore"]["teams"]["home"]["batters"]
        self.home_starting_pitcher = self.home_batting_order.pop()

        self.display_array = []
        self.display_array.append(self.display("away"))
        self.display_array.append(self.display("home"))

    def display(self, loc):
        away = self.game_data["gameData"]["teams"][loc]["name"] + "\n"
        away = away + self.game_data["gameData"]["probablePitchers"][loc]["fullName"]
        return away

    async def pretty_print(self, client):
        
        return self.display_array + [str(round(await self.compute(client), 2))]
        # return an array, in the form
        # [awayteam \n awaySP, hometeam \n homeSP, predicted line]


    def retrieve_splits():
        pass

    def compute(self, client):
        pass

