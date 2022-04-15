from datetime import date
<<<<<<< HEAD
from pytz import timezone
import requests
from dotenv import load_dotenv
import os
<<<<<<<< HEAD:app/dailygames.py
from app.standings import get_standings
from app.utilities import time_formatter
========
from standings import get_standings
from utilities import time_formatter
>>>>>>>> main:dailygames.py
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

# Rivalry daya came from Wikipedia list: https://en.wikipedia.org/wiki/National_Hockey_League_rivalries
# Significant rivalries were cross-referenced with this list: https://www.rookieroad.com/ice-hockey/top-10-nhl-rivalries-of-all-time/
# Rivalries were assigned a score of 1 (mild), 2 (moderate to significant), or 3 (extreme)
rivalries = [['Ottawa Senators','Toronto Maple Leafs',2],['Buffalo Sabres','Toronto Maple Leafs',1],['Boston Bruins','Buffalo Sabres',2],\
    ['Boston Bruins','Montreal Canadiens',3],['Boston Bruins','Tampa Bay Lightning',1],['Boston Bruins','Toronto Maple Leafs',2],\
    ['Florida Panthers','Tampa Bay Lightning',2],['Montreal Canadiens','Ottawa Senators',2], ['Montreal Canadiens','Toronto Maple Leafs',3], \
    ['Montreal Canadiens','Toronto Maple Leafs',3],['New York Islanders','New York Rangers',2],['Philadelphia Flyers','Pittsburgh Penguins',1], \
    ['New Jersey Devils','New York Rangers',2],['New Jersey Devils','Philadelphia Flyers',2],['Columbus Blue Jackets','Pittsburgh Penguins',2], \
    ['New York Islanders','Philadelphia Flyers',2],['New York Islanders','Pittsburgh Penguins',2],['New York Islanders','Washington Capitals',1], \
    ['New York Rangers','Philadelphia Flyers',1],['New York Rangers','Pittsburgh Penguins',1],['New York Rangers','Washington Capitals',1], \
    ['Philadelphia Flyers','Washington Capitals',1],['Pittsburgh Penguins','Washington Capitals',3],['Boston Bruins','New York Rangers',1], \
    ['Boston Bruins','Philadelphia Flyers',2],['Boston Bruins','Pittsburgh Penguins',1],['Boston Bruins','Washington Capitals',1],\
    ['New York Islanders','Toronto Maple Leafs',1],['Chicago Blackhawks','Minnesota Wild',1],['Chicago Blackhawks','St. Louis Blues',2], \
    ['Colorado Avalanche','Dallas Stars',1],['Dallas Stars','St. Louis Blues',1],['Anaheim Ducks','San Jose Sharks',1], \
    ['Calgary Flames','Edmonton Oilers',2],['Calgary Flames','Vancouver Canucks',1],['Anaheim Ducks','Los Angeles Kings',1], \
    ['Los Angeles Kings','San Jose Sharks',1],['San Jose Sharks','Vegas Golden Knights',1],['Calgary Flames','Winnipeg Jets',2],\
    ['Edmonton Oilers','Winnipeg Jets',1],['Chicago Blackhawks','Detroit Red Wings',2],['Colorado Avalanche','Detroit Red Wings',2], \
    ['Detroit Red Wings','Toronto Maple Leafs',3]]
=======
import requests
from dotenv import load_dotenv
import os
from app.standings import get_standings
from pprint import pprint



def load_schedule():

    load_dotenv()

    # sets today's date
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
    #print(len(schedule_data["games"]))
    return schedule_data


# still need to resolve how to show the time of the game, looks wonky af in the data
def show_schedule(schedule_data):

    print(schedule_data["date"], "SCHEDULE:")
    for game in schedule_data["games"]:
        print(game["home"]["name"], "host the", game["away"]["name"])
        print(game["away"]["alias"], "@", game["home"]["alias"])
        print("Scheduled for:", game["scheduled"])
        broadcasts = []
        for broadcast in game["broadcasts"]:
            broadcasts.append(broadcast["network"])
        
        #there is a weird comma that shows up after "Watch on:" but I don't know how to get rid of it and still print the networks on the same line
        print("Watch on:", *broadcasts, sep = ", ")
        print(" ")
        print("-----")
        print(" ")



if __name__ == "__main__":

    schedule_data = load_schedule()

    # imports standings
    standings = get_standings()

    # Loops through days' games and prints home and away teams
    for game in schedule_data['games']:
        # prints teams playing
        print(' - ' + game['away']['name'] + ' at ' + game['home']['name'])

        
        
        # prints the teams' records
        for i in range(len(standings)):
            if standings[i][0] in game['away']['name']: #away team
                # each team has this [team name, win #, loss #] in standings
                record_msg = '   - Record: ' + standings[i][0] + ' (' + str(standings[i][1]) + 'W-' + str(standings[i][2]) + 'L) // '
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
>>>>>>> main

