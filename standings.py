from datetime import date
import requests
from dotenv import load_dotenv
import os



def get_standings():

    load_dotenv()

    today = date.today()
    # Sets today's date variables automatically // calls API key from .env
    season = str(today.year-1)
    api_key = os.getenv('SPORTSRADAR_NHL_API')
    # code to get API data, syntax courtesy of Plotly
    url = 'http://api.sportradar.us/nhl/trial/v7/en/seasons/' + season + '/REG/standings.json?api_key=' + api_key
    r = requests.get(url)
    data = r.json()
    print('\n')

    # print(data)

    # Makes list of dictionaries st {team : win #}
    standings = []
    for conference in data['conferences']:
        for division in conference['divisions']:
            for team in division['teams']:
                standings.append({team['name']:{'wins':team['wins'],'losses':team['losses']}})

    print(standings)
    return standings

