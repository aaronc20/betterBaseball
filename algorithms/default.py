from algorithms.algorithm import Algorithm
import asyncio, httpx

P_SZN = lambda x: "https://statsapi.mlb.com/api/v1/people/" + str(x) + "/stats?stats=season"

class Default(Algorithm):
    
    def __init__(self, game):
        super().__init__(game)
    
    # get season stats for pitcher
    async def pitcher_season_stats(self, pitcher, client):
        return (await client.get(P_SZN(pitcher))).json()

    async def compute(self, client):

    
        tasks = []
        tasks.append(asyncio.ensure_future(self.pitcher_season_stats(self.away_starting_pitcher, client)))
        tasks.append(asyncio.ensure_future(self.pitcher_season_stats(self.home_starting_pitcher, client)))
        
        
        away, home = await asyncio.gather(*tasks)
        
        # as default, literally just return a shitty algo
        # TOTAL RUNS = AWAY SP ERA + HOME SP ERA
        
        away = float(away["stats"][0]["splits"][0]["stat"]["era"])
        home = float(home["stats"][0]["splits"][0]["stat"]["era"])

        return away + home
            

