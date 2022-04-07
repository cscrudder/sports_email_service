from datetime import date
import requests
from dotenv import load_dotenv
import os
import time
from pprint import pprint
import json


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
    #pprint(standings_data)
    #print(standings_data["conferences"][0].keys())
    #print(standings_data["conferences"][0]["divisions"][0].keys())
    #print(standings_data["conferences"][0]["divisions"][0]["teams"][0].keys())
    #print(len(standings_data["conferences"]))

    # printing a clean list of standings
    # Eastern conference

    eastern_teams = []
    for x in standings_data["conferences"][1]["divisions"]:
        for team in x["teams"]:
            teams = []
            teams.append(team["rank"]["conference"])
            teams.append(team["name"])
            teams.append(team["wins"])
            teams.append(team["losses"])
            teams.append(team["overtime_losses"])
            eastern_teams.append(teams)
    
    eastern_teams = sorted(eastern_teams, key = lambda x: x[0])


    #ordered_rankings = []
    #for team in range(len(eastern_teams)):
    #    if eastern_teams[team][0] == team+1:
    #        ordered_rankings.append(eastern_teams[team])
    
    print("EASTERN CONFERENCE STANDINGS")
    print(" ")
    for item in eastern_teams:
        print(str(item[0]) + ".", str(item[1]), "--", "Record:", str(item[2]) + "-" + str(item[3]) + "-" + str(item[4]))

    print(" ")
    print("-----")
    #print(eastern_teams)


    western_teams = []
    for x in standings_data["conferences"][0]["divisions"]:
        for team in x["teams"]:
            teams = []
            teams.append(team["rank"]["conference"])
            teams.append(team["name"])
            teams.append(team["wins"])
            teams.append(team["losses"])
            teams.append(team["overtime_losses"])
            western_teams.append(teams)
    
    western_teams = sorted(western_teams, key = lambda x: x[0])


    #ordered_rankings = []
    #for team in range(len(eastern_teams)):
    #    if eastern_teams[team][0] == team+1:
    #        ordered_rankings.append(eastern_teams[team])
    
    print("WESTERN CONFERENCE STANDINGS")
    print(" ")
    for item in western_teams:
        print(str(item[0]) + ".", str(item[1]), "--", "Record:", str(item[2]) + "-" + str(item[3]) + "-" + str(item[4]))

    #print(eastern_teams)













    # Makes list of lists st [team name, win #, loss #]
    standings = []
    for conference in standings_data['conferences']:
        for division in conference['divisions']:
            for team in division['teams']:
                standings.append([team['name'],team['wins'],team['losses']])

    return standings

#pprint(get_standings())

standings = get_standings()
#
#for x in range(len(standings)):
#    print(str(x+1)+".", standings[x][0])