# Daily Hockey Briefings App (Python)
This app sends a daily email every morning to hockey fans with a recommended game, schedule of games, the previous days' scores, and conference standings. The recommended game considers expected competitiveness and suspense, as well as games relavent to the user's favorite team.

The app has a web app user interface where fans can enter their name, email, timezone, and favorite team.

## Developer Instructions
Here's the developer page link: https://developer.sportradar.com/docs/read/Home#getting-started

The 'API Sandbox' is particularly helpful. You just tell the website what data you want and it generates the URL you need.

## Installation

Create a copy of this [template repo](https://github.com/cscrudder/sports_email_service), then clone or download your new repo onto your local computer (for example to the Desktop), and navigate there from the command-line:

```sh
cd ~/Desktop/daily-briefings-py/
```

Use Anaconda to create and activate a new virtual environment, perhaps called "briefings-env":

```sh
conda create -n hockey_briefings-env python=3.8
conda activate hockey_briefings-env
```

Then, within an active virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

### Sendgrid

Follow these [SendGrid setup instructions](https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/sendgrid.md#setup) to sign up for a SendGrid account, configure your account's email address (i.e. `SENDER_EMAIL_ADDRESS`), and obtain an API key (i.e. `SENDGRID_API_KEY`).

### Sportradar

To configure the sportradar API, go to [sportradar API Registration](https://developer.sportradar.com/member/register). Register for a "NHL Trial: Trail" API Key.

Create a new file called ".env" in the root directory of this repo, and paste the following contents inside, using your own values as appropriate:

### Google

To be able to send webpage user submissions to a Google Sheet then pull them to send daily emails, create a file called 'client_secret.json' in the root directory, following the instructions [here](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html).

You will need to make a Google Sheet called "nhl_daily_email_data" from your Google Account for send and recieve user data from.

```sh
# these are example contents for the ".env" file:

# required vars:
SPORTSRADAR_NHL_API='________________'
SENDGRID_API_KEY='________________'
SENDER_EMAIL_ADDRESS='________________'

# optional vars:
TIMEZONE='ET'
```

## Usage
To send all registered users a briefing:
```sh
python -m app.functions
```

## Run Flask
```sh
export FLASK_APP=web_app
flask run
```