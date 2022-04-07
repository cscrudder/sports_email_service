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
schedule_url = 'http://api.sportradar.us/nhl/trial/v7/en/games/' + year + '/'+ month + '/'+ day + '/schedule.json?api_key=' + api_key
schedule_r = requests.get(schedule_url)
schedule_data = schedule_r.json()
print('\n')

# Loops through days' games and prints home and away teams
for game in schedule_data['games']:
    print(' - ' + game['away']['name'] + ' at ' + game['home']['name'])
    


    broadcast_msg = '   - Broadcasts: '
    for i in range(len(game['broadcasts'])):
        broadcast_msg = broadcast_msg + (game['broadcasts'][i]['network'])
        if 'locale' in game['broadcasts'][i].keys():
            broadcast_msg = broadcast_msg + ' (' + game['broadcasts'][i]['locale'].lower() + ')'
        if i < (len(game['broadcasts'])-2):
            broadcast_msg = broadcast_msg + ', '
        if i == (len(game['broadcasts'])-2):
            broadcast_msg = broadcast_msg + ' and '
    print(broadcast_msg)
    print('')



