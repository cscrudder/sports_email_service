# function to recommend games

from app.users import users
from app.api_pulls import get_schedule, get_standings
from pprint import pprint
from app.dailygames import rivalries
from app.utilities import time_formatter


def featured_game(user, schedule_data):

    """
    Requires user data from the users.py file and schedule data from the Sportradar API

    Invoke like:

    featured_game(user, schedule_data)

    Function will return a featured game based on user's team affiliations
    
    """

    featured_game = None

    # Loops through days' games and prints home and away teams
    
    
    if user['affiliation'] != "League":

        done = False

        for game in schedule_data['games']:
            # prints teams playing
            #print(' - ' + game['away']['name'] + ' at ' + game['home']['name'] + ' (' + time_formatter(game['scheduled'], timezone) + ')')
            if game['away']['name'] == user['affiliation'] or game['home']['name'] == user['affiliation']:
                featured_game = game
                done = True
        if done == False:
            rivalry_games = []
            featured_game = None

            for game in schedule_data["games"]:
                teams = []
                teams.append(game['away']['name'])
                teams.append(game['home']['name'])
                for matchup in rivalries:
                    if (teams[0] in matchup) and (teams[1] in matchup):
                        rivalry_games.append(game)
            
            print(rivalry_games)

            if len(rivalry_games) == 1:
                featured_game = game
            elif len(rivalry_games) > 1:
                primetime_games = []
                for match in rivalry_games:
                    gametime = time_formatter(match["scheduled"])
                    #print(gametime[0])
                    if int(gametime[0]) == 7 or int(gametime[0]) == 8 or int(gametime[0]) == 9:
                        primetime_games.append(match)
                    
                if len(primetime_games) == 0:
                    featured_game = rivalry_games[0]
                else:
                    featured_game = primetime_games[0]
            
            elif len(rivalry_games) == 0:
                primetime_games = []
                for match in schedule_data["games"]:
                    gametime = time_formatter(match["scheduled"])
                    #print(gametime[0])
                    if int(gametime[0]) == 7 or int(gametime[0]) == 8 or int(gametime[0]) == 9:
                        primetime_games.append(match)
                    
                if len(primetime_games) == 0:
                    featured_game = None
                else:
                    featured_game = primetime_games[0]


    elif user['affiliation'] == "League":

        
        rivalry_games = []
        featured_game = None

        for game in schedule_data["games"]:
            teams = []
            teams.append(game['away']['name'])
            teams.append(game['home']['name'])
            for matchup in rivalries:
                if (teams[0] in matchup) and (teams[1] in matchup):
                    rivalry_games.append(game)
        
        print(rivalry_games)

        if len(rivalry_games) == 1:
            featured_game = game
        elif len(rivalry_games) > 1:
            primetime_games = []
            for match in rivalry_games:
                gametime = time_formatter(match["scheduled"])
                #print(gametime[0])
                if int(gametime[0]) == 7 or int(gametime[0]) == 8 or int(gametime[0]) == 9:
                    primetime_games.append(match)
                
            if len(primetime_games) == 0:
                featured_game = rivalry_games[0]
            else:
                featured_game = primetime_games[0]
        
        elif len(rivalry_games) == 0:
            primetime_games = []
            for match in schedule_data["games"]:
                gametime = time_formatter(match["scheduled"])
                #print(gametime[0])
                if int(gametime[0]) == 7 or int(gametime[0]) == 8 or int(gametime[0]) == 9:
                    primetime_games.append(match)
                
            if len(primetime_games) == 0:
                featured_game = None
            else:
                featured_game = primetime_games[0]

   
    return featured_game
















#sched = get_schedule()
#
#times = []
#
#for game in sched["games"]:
#
#    times.append(time_formatter(game["scheduled"]))
#
#print(times[0][0])


for user in users:

    pprint(featured_game(user,get_schedule()))


