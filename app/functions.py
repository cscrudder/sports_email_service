from datetime import date
import sched
import google_auth_oauthlib
import requests
from dotenv import load_dotenv
import os
import time
import pytz, dateutil.parser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS")
RECIPIENT_EMAIL_ADDRESS = os.getenv("RECIPIENT_EMAIL_ADDRESS")


# Sportradar API REQUESTS
def get_standings():
    """
    This function returns a dictionary from the Sportsradar API with NHL league standings data.
    The API is accessed with the following URL (see below in python syntax):

    'http://api.sportradar.us/nhl/trial/v7/en/seasons/' + season + '/REG/standings.json?api_key=' + api_key

    In the above, the season part should be a year and the API key should be obtained by each developer.

    When the data is returned from the API, it is stored in the return variable.
    """

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
    return standings_data

def get_schedule():
    """
    This function returns the daily NHL game schedule from the Sportradar API.
    The API can be accessed with the following URL (see below in python syntax):

    'http://api.sportradar.us/nhl/trial/v7/en/games/' + year + '/'+ month + '/'+ day + '/schedule.json?api_key=' + api_key

    When the data is returned from the API, it is stored in the return variable.
    """

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

# FUNCTION THAT PULLS USER DATA FROM GOOGLE SHEET
def get_user_data(): 
    """
    This function gets user data from a google sheet called 'nhl_daily_email_data'. It does not require any inputs and returns a list of dictionaries.
    """    

    # syntax courtesy of: https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials


    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)


    client = gspread.authorize(creds)

    # # Find a workbook by name and open the first sheet
    # # Make sure you use the right name here.
    sheet = client.open("nhl_daily_email_data").sheet1

    # # Extract and print all of the values
    users = sheet.get_all_records()
    return users

# FUNCTION THAT DETERMINES THE FEATURED GAME
def featured_game(user, schedule_data):
    
    """
    Requires user data from the users.py file and schedule data from the Sportradar API

    Invoke like:

    featured_game(user, schedule_data)

    Function will return a featured game based on user's team affiliations
    
    """

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
        # Rivalry daya came from Wikipedia list: https://en.wikipedia.org/wiki/National_Hockey_League_rivalries
        # Significant rivalries were cross-referenced with this list: https://www.rookieroad.com/ice-hockey/top-10-nhl-rivalries-of-all-time/
        # Rivalries were assigned a score of 1 (mild), 2 (moderate to significant), or 3 (extreme)

    featured_game = None

    # Loops through days' games and prints home and away teams
    


    if user['affiliation'] != "League":

        done = False

        # loop to test if the user's team is playing that day

        for game in schedule_data['games']:
            # prints teams playing
            if game['away']['name'].strip() == user['affiliation'].strip() or game['home']['name'].strip() == user['affiliation'].strip():
                featured_game = game
                done = True
        
        # if not, look for other games that could be of interest
        if done == False:
            rivalry_games = []
            featured_game = None

            #looking for rivalry games
            for game in schedule_data["games"]:
                teams = []
                teams.append(game['away']['name'])
                teams.append(game['home']['name'])
                for matchup in rivalries:
                    if (teams[0] in matchup) and (teams[1] in matchup):
                        rivalry_games.append(game)
            
            #print(rivalry_games)

            if len(rivalry_games) == 1:
                featured_game = game
            
            # if there is more than one rivalry game, look for if any of them are in primetime
            elif len(rivalry_games) > 1:
                primetime_games = []
                for match in rivalry_games:
                    gametime = time_formatter(match["scheduled"])
                    #print(gametime[0])
                    if int(gametime[0]) == 7 or int(gametime[0]) == 8 or int(gametime[0]) == 9:
                        primetime_games.append(match)
                
                # if none are, choose the first rivalry game.  If one is, choose that
                if len(primetime_games) == 0:
                    featured_game = rivalry_games[0]
                else:
                    featured_game = primetime_games[0]
            
            # if there are no rivalry games, look for primetime games
            elif len(rivalry_games) == 0:
                primetime_games = []
                for match in schedule_data["games"]:
                    gametime = time_formatter(match["scheduled"])
                    #print(gametime[0])
                    if int(gametime[0]) == 7 or int(gametime[0]) == 8 or int(gametime[0]) == 9:
                        primetime_games.append(match)

                # in the absence of primetime games, there are no featured games that day   
                if len(primetime_games) == 0:
                    featured_game = None
                else:
                    featured_game = primetime_games[0]


    # same exact logic as above, but it skips the part where it looks for the user's team
    elif user['affiliation'] == "League":

        rivalry_score = 1

        rivalry_games = []
        featured_game = None

        for game in schedule_data["games"]:
            teams = []
            teams.append(game['away']['name'])
            teams.append(game['home']['name'])
            for matchup in rivalries:
                if (teams[0] in matchup) and (teams[1] in matchup):

                    rivalry_games.append(game)
        
        #print(rivalry_games)

                    if matchup[2] > rivalry_score:
                        rivalry_games.append(game)
        
        # print(rivalry_games)


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

    return_list = []
    return_list.append(featured_game)
    return return_list

# FUNCTIONS THAT RETURN CONFERENCE AND DIVISION STANDINGS
def nhl_conference_standings(standings_data):
    
    """
    This function requires input of a dictionary from the Sportsradar API with NHL league standings data.
    The API can be accessed with the following URL (see below in python syntax):

    'http://api.sportradar.us/nhl/trial/v7/en/seasons/' + season + '/REG/standings.json?api_key=' + api_key

    In the above, the season part should be a year and the API key should be obtained by each developer.

    When the data is returned from the API, store it in a variable as a dictionary and pass it into this function.
    """

    conf_html = ''

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

        ## HTML formatting
        conf_html += '<h3>' + standings_data["conferences"][conference]["alias"].title() + " Conference Standings</h3>"
        conf_html += '<table><tr><th>Rank</th><th>Team</th><th>Wins</th><th>Losses</th><th>OT Losses</th><th>Points</th></tr>'
        for item in conf_teams:
            conf_html += '<tr><td>' + str(item[0]) + '</td>' + '<td>' + str(item[1]) + ' ' + str(item[2]) + '</td>' + '<td>' + str(item[3]) + '</td>' + '<td>' + str(item[4]) + '</td>' + '<td>' + str(item[5]) + '</td>' + '<td>' + str(item[6]) + '</td></tr>'
        conf_html += '</table>'

    return conf_html        

def nhl_division_standings(standings_data):

    """
    This function requires input of a dictionary from the Sportsradar API with NHL league standings data.
    The API can be accessed with the following URL (see below in python syntax):

    'http://api.sportradar.us/nhl/trial/v7/en/seasons/' + season + '/REG/standings.json?api_key=' + api_key

    In the above, the season part should be a year and the API key should be obtained by each developer.

    When the data is returned from the API, store it in a variable as a dictionary and pass it into this function.
    """

    # division standings

    div_html = ''

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

            # HTML formatting
            div_html += '<h3>' + standings_data["conferences"][conference]["divisions"][division]["alias"].title() + ' Division Standings</h3>'
            div_html += '<table><tr><th>Rank</th><th>Team</th><th>Wins</th><th>Losses</th><th>OT Losses</th><th>Points</th></tr>'
            for item in div_teams:
                div_html += '<tr><td>' + str(item[0]) + '</td>' + '<td>' + str(item[1]) + ' ' + str(item[2]) + '</td>' + '<td>' + str(item[3]) + '</td>' + '<td>' + str(item[4]) + '</td>' + '<td>' + str(item[5]) + '</td>' + '<td>' + str(item[6]) + '</td></tr>'
            div_html += '</table>'

    return div_html

# FORMATS ISO TIME
def time_formatter(time, timezone="ET"):
    """
    This function takes times only in the format ISO 8601 format (2022-04-08T23:00:00Z) and converts them to a readable time.
    The function does not return minuites if they are '00'. The return includes AM/PM and the timezone.
    Users may choose from ET, CT, MT, PT, or AKT timezones. ET is set as the default.    
    """

    # dictionary to convert timezone abbreviations to the needed inputs for pytz
    abbreviations = {'ET':'America/New_York','CT':'America/North_Dakota/Center','MT':'America/Denver','PT':'America/Los_Angeles','AKT':'America/Juneau'}

    # utc to ET time conversion syntax from xster, a medium user: 
    # https://medium.com/xster-tech/python-convert-iso8601-utc-to-local-time-a386652b0306

    utc_time = dateutil.parser.parse(time)
    local_time = utc_time.astimezone(pytz.timezone(abbreviations[timezone]))

    local_time = str(local_time)
    hour = int(local_time[11:][:2])
    minutes = int(local_time[14:][:2])

    # Formats AM/PM and on-the-hour/not-on-the-hour starts nicely
    if minutes == 0:
        if hour > 12:
            return (str(hour - 12) + 'PM' + ' ' + timezone)
        else:
            return (str(hour) + 'AM' + ' ' + timezone)
    else:
        if hour > 12:
            return (str(hour - 12) + ':' + str(minutes) + 'PM' + ' ' + timezone)
        else:
            return (str(hour) + ':' + str(minutes) + 'AM' + ' ' + timezone) 

# CONVERTS GAME DATA TO HTML
def game_formatter(schedule_data, standings_data, timezone='ET'):
    """
    This function formats games in the following way in HTML:
        - Away Team at Home Team (TIME)
            - Records
            - Broadcast Info
    It requires daily schedule data (in a list), stanings data (in the API SportsRadar API format), and optionally the time zone you want displayed (ET,CT,MT,PT, or AKT only)
    """

    schedule_html = ''

    # Loops through days' games and prints home and away teams
    
    for game in schedule_data:
        # prints teams playing
        schedule_html += '<li><b>' + game['away']['name'] + ' at ' + game['home']['name'] + '</b> (' + time_formatter(game['scheduled'], timezone) + ')'

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
                schedule_html += '<ul style="list-style-type: circle; padding-bottom: 0;">'
                schedule_html += '<li style="margin-left:em">' + 'Records: ' + standings[i][0] + ' (' + str(standings[i][1]) + 'W-' + str(standings[i][2]) + 'L) | ' 

        for i in range(len(standings)):
            if standings[i][0] in game['home']['name']: #home team
                # each team has this [team name, win #, loss #] in standings
                # adds home team to away team standings
                # record_msg = record_msg + standings[i][0] + ' (' + str(standings[i][1]) + 'W-' + str(standings[i][2]) + 'L)'
                schedule_html += standings[i][0] + ' (' + str(standings[i][1]) + 'W-' + str(standings[i][2]) + 'L)' + '</li>'
        # print(record_msg)   
    
        # prints info about the boradcast
        broadcast_msg = 'Broadcasts: '
        for i in range(len(game['broadcasts'])):
            broadcast_msg = broadcast_msg + (game['broadcasts'][i]['network'])
            # if statements make sure to format the list correctly
            if 'locale' in game['broadcasts'][i].keys():
                broadcast_msg = broadcast_msg + ' (' + game['broadcasts'][i]['locale'].lower() + ')'
            if i < (len(game['broadcasts'])-2):
                broadcast_msg = broadcast_msg + ', '
            if i == (len(game['broadcasts'])-2):
                broadcast_msg = broadcast_msg + ' and ' 
        schedule_html += '<li style="margin-left:em">' + broadcast_msg + '</li></ul></li>'
    schedule_html += '</ul>'
    return schedule_html
# schedule['games'] to print the day's schedule
# game_formatter(featured_game(user, schedule))) to get the recommended game

# FUNCTION THAT COMBINES ALL PREVIOUS FUNCTIONS TO PRODUCE 1 HTML MESSAGE
def html_message(user_data,standings_data,schedule_data):
    """
    This function aggregates all the HTML messages to form a cohesive email. It requires user_data (list of dictionaires with keys name, email, affiliation, time_zone), NHL standings data (in the Sportradar API output format), and schedule data (in the Sportradar API output format)
    The function callls all HTML formatting functions then appenends those strings.
    It returns the HTML code for the email
    """
    # Starts with a blank string
    html_message = ''
    # Adds the user name and salutation
    html_message += '<h3>Hey ' + user_data['name'] + ',</h3><p>Here is your daily update!</b>'
    # Adds recommended game info
    html_message += "<h1>Today's Recommended Game:</h1>" + game_formatter(featured_game(user_data, schedule_data),standings_data, user_data['time_zone'])
    # Adds the daily schedule
    html_message += "<h1>Today's Schedule:</h1>" + game_formatter(schedule_data['games'], standings_data, user_data['time_zone'])
    # Adds league stadnings
    html_message += "<h1>League Standings:</h1>" + nhl_division_standings(standings_data) + nhl_conference_standings(standings_data)
    # Returns HTML
    return html_message

# FUNCTION THAT SENDS EMAILS
def send_email(subject="Daily Hockey Report", html="<p>Hello World</p>", recipient_address=RECIPIENT_EMAIL_ADDRESS):
    """
    Sends an email with the specified subject and html contents to the specified recipient,

    If recipient is not specified, sends to the admin's sender address by default.
    """
        
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    print("SUBJECT:", subject)
    #print("HTML:", html)

    message = Mail(from_email=SENDER_EMAIL_ADDRESS, to_emails=recipient_address, subject=subject, html_content=html)
    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", type(e), e)
        return None




if __name__ == "__main__":
    standings = get_standings()
    schedule = get_schedule()
    users = get_user_data()
    # print(game_formatter(featured_game(user, schedule)))
    # print(nhl_conference_standings(standings))
    # print(nhl_division_standings(standings))
    # print(game_formatter(schedule['games']))
    # print(html_message(user,standings,schedule))

    # print(schedule)
    # print(standings)

    from datetime import date
    today = date.today().strftime("%b %d %Y")
    email_subject = "NHL Daily Briefing: " + today
    
    for user in users:
        send_email(subject=email_subject, html=html_message(user,standings,schedule), recipient_address=user['email'])


