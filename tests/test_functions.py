# place for testing the functions we have written

#from typing_extensions import assert_type
from app.functions import get_standings, get_schedule, get_user_data, featured_game, time_formatter, game_formatter
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

def test_game_formatter():
    # Tests one game if formatted like we want (we put this output in a text editor to verify it is what we want)
    test_game = [{'id': '58791bfc-641e-4440-8607-6d3b3ddb40b3', 'status': 'scheduled', 'coverage': 'full', 'scheduled': '2022-04-26T23:00:00Z', 'sr_id': 'sr:match:28276586', 'reference': '21274', 'venue': {'id': 'e1e675a3-9c13-48b3-9e22-4c063dd9905d', 'name': 'Canadian Tire Centre', 'capacity': 18572, 'address': '1000 Palladium Drive', 'city': 'Ottawa', 'state': 'ON', 'country': 'CAN', 'time_zone': 'US/Eastern', 'sr_id': 'sr:venue:6066'}, 'broadcasts': [{'network': 'TSN5', 'type': 'TV', 'locale': 'International'}, {'network': 'RDS2', 'type': 'TV', 'locale': 'International'}, {'network': 'MSG+', 'type': 'TV', 'locale': 'Away', 'channel': '634-1'}], 'home': {'id': '4416f5e2-0f24-11e2-8525-18a905767e44', 'name': 'Ottawa Senators', 'alias': 'OTT', 'sr_id': 'sr:team:3700', 'reference': '9'}, 'away': {'id': '44174b0c-0f24-11e2-8525-18a905767e44', 'name': 'New Jersey Devils', 'alias': 'NJ', 'sr_id': 'sr:team:3704', 'reference': '1'}}]
    formatted_game = game_formatter(test_game)
    assert formatted_game == '<li><b>New Jersey Devils at Ottawa Senators</b> (7PM ET)<ul style="list-style-type: circle; padding-bottom: 0;"><li style="margin-left:em">Records: Devils (27W-44L) | Senators (31W-41L)</li><li style="margin-left:em">Broadcasts: TSN5 (international), RDS2 (international) and MSG+ (away)</li></ul></li></ul>'

    # Tests another game if formatted like we want (we put this output in a text editor to verify it is what we want)
    test_game2 = [{'id': '4b6dbaa5-7de3-48f4-9464-f38bb47fcc86', 'status': 'scheduled', 'coverage': 'full', 'scheduled': '2022-04-27T02:30:00Z', 'sr_id': 'sr:match:28276572', 'reference': '21285', 'venue': {'id': '1da65282-af4c-4b81-a9de-344b76bb20b0', 'name': 'SAP Center at San Jose', 'capacity': 17562, 'address': '525 W Santa Clara Street', 'city': 'San Jose', 'state': 'CA', 'zip': '95113', 'country': 'USA', 'time_zone': 'US/Pacific', 'sr_id': 'sr:venue:6046'}, 'broadcasts': [{'network': 'NBCS-CA', 'type': 'TV', 'locale': 'Home', 'channel': '698'}, {'network': 'BSSC', 'type': 'TV', 'locale': 'Away', 'channel': '693'}], 'home': {'id': '44155909-0f24-11e2-8525-18a905767e44', 'name': 'San Jose Sharks', 'alias': 'SJ', 'sr_id': 'sr:team:3696', 'reference': '28'}, 'away': {'id': '441862de-0f24-11e2-8525-18a905767e44', 'name': 'Anaheim Ducks', 'alias': 'ANA', 'sr_id': 'sr:team:3675', 'reference': '24'}}]
    formatted_game2 = game_formatter(test_game2)
    assert formatted_game2 == '<li><b>Anaheim Ducks at San Jose Sharks</b> (10:30PM ET)<ul style="list-style-type: circle; padding-bottom: 0;"><li style="margin-left:em">Records: Ducks (30W-36L) | Sharks (32W-35L)</li><li style="margin-left:em">Broadcasts: NBCS-CA (home) and BSSC (away)</li></ul></li></ul>'

def test_get_user_data():
    ## This tests if the google sheet has the headings of user data we need to run the functions
    user_data = get_user_data()
    google_sheet_keys = list(user_data[0].keys())
    assert google_sheet_keys == ['name', 'email', 'affiliation', 'time_zone']

def test_featured_game():
    ## This part tests if the users' favorite team will be returned.
    test_schedule = {'date': '2022-04-26', 'league': {'id': 'fd560107-a85b-4388-ab0d-655ad022aff7', 'name': 'NHL', 'alias': 'NHL'}, \
        'games': [{'home': {'id': '441781b9-0f24-11e2-8525-18a905767e44', 'name': 'New York Rangers', 'alias': 'NYR', 'sr_id': 'sr:team:3701', 'reference': '3'}, 'away': {'id': '44182a9d-0f24-11e2-8525-18a905767e44', 'name': 'Carolina Hurricanes', 'alias': 'CAR', 'sr_id': 'sr:team:3680', 'reference': '12'}}, \
            {'home': {'id': '441730a9-0f24-11e2-8525-18a905767e44', 'name': 'Toronto Maple Leafs', 'alias': 'TOR', 'sr_id': 'sr:team:3693', 'reference': '10'}, 'away': {'id': '44169bb9-0f24-11e2-8525-18a905767e44', 'name': 'Detroit Red Wings', 'alias': 'DET', 'sr_id': 'sr:team:3685', 'reference': '17'}}]}
    user = {"name":"Jack","email":"jpf99@georgetown.edu","affiliation":"Toronto Maple Leafs","timezone":"ET"}
    selected_game = featured_game(user,test_schedule)
    assert selected_game[0]['home']['name'] == 'Toronto Maple Leafs'

    ## This part tests if the users' favorite team will be returned.
    test_schedule = {'date': '2022-04-26', 'league': {'id': 'fd560107-a85b-4388-ab0d-655ad022aff7', 'name': 'NHL', 'alias': 'NHL'}, \
        'games': [{'home': {'id': '441781b9-0f24-11e2-8525-18a905767e44', 'name': 'New York Rangers', 'alias': 'NYR', 'sr_id': 'sr:team:3701', 'reference': '3'}, 'away': {'id': '44182a9d-0f24-11e2-8525-18a905767e44', 'name': 'Carolina Hurricanes', 'alias': 'CAR', 'sr_id': 'sr:team:3680', 'reference': '12'}}, \
            {'home': {'id': '441730a9-0f24-11e2-8525-18a905767e44', 'name': 'Toronto Maple Leafs', 'alias': 'TOR', 'sr_id': 'sr:team:3693', 'reference': '10'}, 'away': {'id': '44169bb9-0f24-11e2-8525-18a905767e44', 'name': 'Detroit Red Wings', 'alias': 'DET', 'sr_id': 'sr:team:3685', 'reference': '17'}}]}
    user = {"name":"Jack","email":"jpf99@georgetown.edu","affiliation":"New York Rangers","timezone":"ET"}
    selected_game = featured_game(user,test_schedule)
    assert selected_game[0]['home']['name'] == 'New York Rangers'

    ## This part tests if the users' affilition is league that a rivalry game will team will be returned.
    test_schedule = {'date': '2022-04-26', 'league': {'id': 'fd560107-a85b-4388-ab0d-655ad022aff7', 'name': 'NHL', 'alias': 'NHL'}, \
        'games': [{'scheduled': '2022-04-26T23:00:00Z','home': {'id': '441781b9-0f24-11e2-8525-18a905767e44', 'name': 'Montreal Canadiens', 'alias': 'NYR', 'sr_id': 'sr:team:3701', 'reference': '3'}, 'away': {'id': '44182a9d-0f24-11e2-8525-18a905767e44', 'name':'Boston Bruins', 'alias': 'CAR', 'sr_id': 'sr:team:3680', 'reference': '12'}}, \
            {'scheduled': '2022-04-26T23:00:00Z','home': {'id': '441730a9-0f24-11e2-8525-18a905767e44', 'name': 'Toronto Maple Leafs', 'alias': 'TOR', 'sr_id': 'sr:team:3693', 'reference': '10'}, 'away': {'id': '44169bb9-0f24-11e2-8525-18a905767e44', 'name': 'Detroit Red Wings', 'alias': 'DET', 'sr_id': 'sr:team:3685', 'reference': '17'}}]}
    user = {"name":"Jack","email":"jpf99@georgetown.edu","affiliation":"League","timezone":"ET"}
    selected_game = featured_game(user,test_schedule)
    assert selected_game[0]['home']['name'] == 'Montreal Canadiens'

def test_time_formatter():
    ## These test time zone
    assert time_formatter('2022-04-08T23:00:00Z','ET') == '7PM ET'
    assert time_formatter('2022-04-08T23:00:00Z','CT') == '6PM CT'
    assert time_formatter('2022-04-08T23:00:00Z','MT') == '5PM MT'
    assert time_formatter('2022-04-08T23:00:00Z','PT') == '4PM PT'
    assert time_formatter('2022-04-08T23:00:00Z','AKT') == '3PM AKT'

    ## This one tests the ':30' functionality
    assert time_formatter('2022-04-08T23:30:00Z','ET') == '7:30PM ET'

    ## This tests different hours
    assert time_formatter('2022-04-08T00:00:00Z','ET') == '8PM ET'
    assert time_formatter('2022-04-08T01:00:00Z','ET') == '9PM ET'