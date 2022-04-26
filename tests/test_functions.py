# place for testing the functions we have written

#from typing_extensions import assert_type
from app.functions import get_standings, get_schedule, get_user_data, featured_game
from pprint import pprint
import requests
from dotenv import load_dotenv
import os
import time
from datetime import date

def test_standings():
    load_dotenv()
    season = str(date.today().year-1)
    api_key = os.getenv('SPORTSRADAR_NHL_API')
    # code to get API data, syntax courtesy of Plotly
    url = 'http://api.sportradar.us/nhl/trial/v7/en/seasons/' + season + '/REG/standings.json?api_key=' + api_key
    r = requests.get(url)
    standings_data = r.json()
    assert get_standings() == standings_data
    #assert type(standings["conferences"]) == "<class 'list'>"

def test_schedule():
    load_dotenv()
    time.sleep(1.1)
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

    assert get_schedule() == schedule_data
#
#def test_featured_game():
#    user = {"name":"Jack","email":"jpf99@georgetown.edu","affiliation":"Boston Bruins","timezone":"ET"}
#    assert
#

#pprint(get_standings())