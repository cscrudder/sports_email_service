# Tests for the API calls
# These are in a different folder to exempt them from GitHub Actions Tests

from app.functions import get_standings, get_schedule, get_user_data
from datetime import date

def test_get_standings():
    # This tests that 1) the API makes the pull and 2) the league is correct (Sportradar offers APIs for many leagues, so this is good to check)
    standings_data = get_standings()
    assert standings_data['league']['name'] == 'NHL'

def test_get_schedule():
    schedule_data = get_schedule()
    # This tests that 1) the API makes the pull and 2) API is sending data from the correct day:
    today = date.today().strftime("%Y-%m-%d")
    assert schedule_data['date'] == today
    # This tests that the league is correct
    assert schedule_data['league']['name'] == 'NHL'


def test_get_user_data():
    ## This tests if the google sheet has the headings of user data we need to run the functions
    user_data = get_user_data()
    google_sheet_keys = list(user_data[0].keys())
    assert google_sheet_keys == ['name', 'email', 'affiliation', 'time_zone']
