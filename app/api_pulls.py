from datetime import date
import requests
from dotenv import load_dotenv
import os
import time

def get_standings():

    load_dotenv()

    # This wait seems necessary since we're using the free API and it throws an error if we don't use it.
    time.sleep(1.1)
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





def get_schedule():
    load_dotenv()
    time.sleep(1.1)
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

    return schedule_data


