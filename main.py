import httpx, asyncio, json
import time

from games.game import Game
from algorithms.default import Default

from rich.console import Console
from rich.table import Table

# LAMBDAS
PAD = lambda x: "0" + str(x) if len(str(x)) == 1 else str(x)

# CONSTS
TODAY_SCHEDULE_LINK = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date="

def date():
    today = time.localtime()
    return str(today.tm_year) + "-" + PAD(today.tm_mon) + "-" + PAD(today.tm_mday)

algorithms_mapping = {
    1: "default",
}

def tableize():
    table = Table(title="Algorithms")
    table.add_column("algorithm")
    table.add_column("num")
    for key in algorithms_mapping.keys():
        table.add_row(algorithms_mapping[key], str(key))
    return table

def get_tasks(slate, client):
    console = Console()
    console.print(tableize())
    algo = input("pick an algorithm by selecting the number associated w/ it: ")

    tasks = []
    if algo == "1":
        tasks = [asyncio.ensure_future(Default(game["gamePk"]).pretty_print(client)) for game in slate["dates"][0]["games"]]

    return tasks

async def run():
    

    slate = httpx.get(TODAY_SCHEDULE_LINK + date()).json()
    async with httpx.AsyncClient() as client:

        tasks = get_tasks(slate, client)
        results = await asyncio.gather(*tasks)
    
        table = Table(title=f"Slate for {date()}", show_lines=True)
        table.add_column("Away Team")
        table.add_column("Home Team")
        table.add_column("Predicted Runs")

        for s in results:
            table.add_row(s[0], s[1], s[2])

        console = Console()
        console.print(table)


    
asyncio.run(run())
