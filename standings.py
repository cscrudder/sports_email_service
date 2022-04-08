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
    #pprint(standings_data["conferences"][0].keys())
    #print(standings_data["conferences"][0]["divisions"][0].keys())
    #print(standings_data["conferences"][0]["divisions"][0]["teams"][0].keys())
    #print(len(standings_data["conferences"]))

    return standings_data



def nhl_conference_standings(standings_data):

    """
    This function requires input of a dictionary from the Sportsradar API with NHL league standings data.
    The API can be accessed with the following URL (see below in python syntax):

    'http://api.sportradar.us/nhl/trial/v7/en/seasons/' + season + '/REG/standings.json?api_key=' + api_key

    In the above, the season part should be a year and the API key should be obtained by each developer.

    When the data is returned from the API, store it in a variable as a dictionary and pass it into this function.
    """

    print(" ")
    # conference standings
    for conference in range(len(standings_data["conferences"])):

        conf_teams = []
        for x in standings_data["conferences"][conference]["divisions"]:
            for team in x["teams"]:
                teams = []
                teams.append(team["rank"]["conference"])
                teams.append(team["market"])
                teams.append(team["name"])
                teams.append(team["wins"])
                teams.append(team["losses"])
                teams.append(team["overtime_losses"])
                teams.append(team["points"])
                conf_teams.append(teams)
        
        conf_teams = sorted(conf_teams, key = lambda x: x[0])

        
        print(standings_data["conferences"][conference]["alias"], "CONFERENCE STANDINGS")
        print(" ")
        for item in conf_teams:
            print(str(item[0]) + ".", str(item[1]), str(item[2]), "|", "Record:", str(item[3]) + "-" 
            + str(item[4]) + "-" + str(item[5]), "|", "Points:", str(item[6]))

        print(" ")

def nhl_division_standings(standings_data):

    """
    This function requires input of a dictionary from the Sportsradar API with NHL league standings data.
    The API can be accessed with the following URL (see below in python syntax):

    'http://api.sportradar.us/nhl/trial/v7/en/seasons/' + season + '/REG/standings.json?api_key=' + api_key

    In the above, the season part should be a year and the API key should be obtained by each developer.

    When the data is returned from the API, store it in a variable as a dictionary and pass it into this function.
    """

    # division standings

    for conference in range(len(standings_data["conferences"])):

        
        for division in range(len(standings_data["conferences"][conference]["divisions"])):
            div_teams = []
            for team in standings_data["conferences"][conference]["divisions"][division]["teams"]:
                teams = []
                teams.append(team["rank"]["division"])
                teams.append(team["market"])
                teams.append(team["name"])
                teams.append(team["wins"])
                teams.append(team["losses"])
                teams.append(team["overtime_losses"])
                teams.append(team["points"])
                div_teams.append(teams)
        
            div_teams = sorted(div_teams, key = lambda x: x[0])

        
            print(standings_data["conferences"][conference]["divisions"][division]["alias"], "DIVISION STANDINGS")
            print(" ")
            for item in div_teams:
                print(str(item[0]) + ".", str(item[1]), str(item[2]), "|", "Record:", str(item[3]) + "-" 
                + str(item[4]) + "-" + str(item[5]), "|", "Points:", str(item[6]))

            print(" ")


if __name__ == "__main__":

    standings = get_standings()

    nhl_conference_standings(standings)
    nhl_division_standings(standings)

