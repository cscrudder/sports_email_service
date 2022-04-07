from datetime import date
import requests
from dotenv import load_dotenv
import os
import time

def get_standings():

    load_dotenv()

    # This wait seems necessary since we're using the free API and it throws an error if we don't use it.
    time.sleep(5)
    today = date.today()
    # Sets today's date variables automatically // calls API key from .env
    season = str(today.year-1)
    api_key = os.getenv('SPORTSRADAR_NHL_API')
    # code to get API data, syntax courtesy of Plotly
    url = 'http://api.sportradar.us/nhl/trial/v7/en/seasons/' + season + '/REG/standings.json?api_key=' + api_key
    r = requests.get(url)
    standings_data = r.json()

    # Makes list of lists st [team name, win #, loss #]
    standings = []
    for conference in standings_data['conferences']:
        for division in conference['divisions']:
            for team in division['teams']:
                standings.append([team['name'],team['wins'],team['losses']])

    return standings

