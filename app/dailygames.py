from datetime import date
from pytz import timezone
import requests
from dotenv import load_dotenv
import os
from app.standings import get_standings
from app.utilities import time_formatter
load_dotenv()

# sets today's date
today = date.today()

# Sets today's date variables automatically // calls API key from .env
day = str(today.day)
month = str(today.month)
year = str(today.year)
api_key = os.getenv('SPORTSRADAR_NHL_API')

# checks if timezone env is set, if not, defaults to ET
if os.getenv('TIMEZONE') is not None:
    timezone = os.getenv('TIMEZONE')
else:
    timezone = 'ET'

# code to get API data, syntax courtesy of Plotly
schedule_url = 'http://api.sportradar.us/nhl/trial/v7/en/games/' + year + '/'+ month + '/'+ day + '/schedule.json?api_key=' + api_key
schedule_r = requests.get(schedule_url)
schedule_data = schedule_r.json()
print('\n')

# imports standings
standings_data = get_standings()

# Loops through days' games and prints home and away teams
for game in schedule_data['games']:
    # prints teams playing
    print(' - ' + game['away']['name'] + ' at ' + game['home']['name'] + ' (' + time_formatter(game['scheduled'], timezone) + ')')

    # Makes list of lists st [team name, win #, loss #]
    standings = []
    for conference in standings_data['conferences']:
       for division in conference['divisions']:
           for team in division['teams']:
               standings.append([team['name'],team['wins'],team['losses']])
    
    # prints the teams' records
    for i in range(len(standings)):
        if standings[i][0] in game['away']['name']: #away team
            # each team has this [team name, win #, loss #] in standings
            record_msg = '   - Records: ' + standings[i][0] + ' (' + str(standings[i][1]) + 'W-' + str(standings[i][2]) + 'L) | '
    for i in range(len(standings)):
        if standings[i][0] in game['home']['name']: #home team
            # each team has this [team name, win #, loss #] in standings
            # adds home team to away team standings
            record_msg = record_msg + standings[i][0] + ' (' + str(standings[i][1]) + 'W-' + str(standings[i][2]) + 'L)'
    print(record_msg)   
 
    # prints info about the boradcast
    broadcast_msg = '   - Broadcasts: '
    for i in range(len(game['broadcasts'])):
        broadcast_msg = broadcast_msg + (game['broadcasts'][i]['network'])
        # if statements make sure to format the list correctly
        if 'locale' in game['broadcasts'][i].keys():
            broadcast_msg = broadcast_msg + ' (' + game['broadcasts'][i]['locale'].lower() + ')'
        if i < (len(game['broadcasts'])-2):
            broadcast_msg = broadcast_msg + ', '
        if i == (len(game['broadcasts'])-2):
            broadcast_msg = broadcast_msg + ' and ' 
    print(broadcast_msg)
    
    print('')

