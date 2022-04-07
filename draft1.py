from datetime import date
import requests
from dotenv import load_dotenv
import os

load_dotenv()

today = date.today()

# Sets today's date variables automatically // calls API key from .env
day = str(today.day)
month = str(today.month)
year = str(today.year)
api_key = os.getenv('SPORTSRADAR_NHL_API')

# code to get API data, syntax courtesy of Plotly
url = 'http://api.sportradar.us/nhl/trial/v7/en/games/' + year + '/'+ month + '/'+ day + '/schedule.json?api_key=' + api_key
r = requests.get(url)
data = r.json()
print('\n')

# Loops through days' games and prints home and away teams
for game in data['games']:
    print(' - ' + game['away']['name'] + ' at ' + game['home']['name'])
