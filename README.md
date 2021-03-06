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

To be able to send webpage user submissions to a Google Sheet then pull them to send daily emails, create a file called 'google-credentials.json' in the root directory, following the instructions [here](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html).

You will need to make a Google Sheet called "nhl_daily_email_data" from your Google Account for send and recieve user data from.

```sh
# these are example contents for the ".env" file:
SPORTSRADAR_NHL_API='________________'
SENDGRID_API_KEY='________________'
SENDER_EMAIL_ADDRESS='________________'
```

## Local Usage
### Usage
To send all registered users a briefing:
```sh
python -m app.functions
```

### Run Flask
To run the web application locally, run the following code in your terminal: 
```sh
export FLASK_APP=web_app
flask run
```

### Testing
Our program is equipped with tests to ensure that the APIs work, the proper game is always recommended, and that our formatting functions work. To run the tests, run the following line of code in your terminal:
```sh
python -m pytest
```
This project is enabled with GitHub Actions to automatically run Pytests. However, the API tests have been exempted from GitHub testing since they require secret credentials in the .env file. However, they can be tested locally.

## Heroku Usage
This program is designed to run once daily at 5am ET on the Heroku server. To do this, you must create a Heroku app. Then you can push the app to Heroku through the terminal:
```sh
git push heroku main
```
Next, you must go to Heroku and set up enivornmental variables. Go to the 'Settings' tab of your app. Click 'Reveal Config Vars'. Enter "GOOGLE_CREDENTIALS" and paste the contents of your google-credentials.json file inside. Then, add the variables from the .env file.

You can then enable and configure 'Heroku Scheduler' to send the email daily. You need to tell the scheduler to run the following code:
```sh
python -m app.functions
```