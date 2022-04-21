# web_app/routes/home_routes.py

from flask import Blueprint, request, render_template, jsonify, render_template, redirect, flash # FYI new imports
import os

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
@home_routes.route("/home")
def home():
    return render_template("home.html")



@home_routes.route("/sample")
def sample():
    return render_template("sample.html")


@home_routes.route("/register", methods=["GET","POST"])
def register():
    
    if request.method == "POST": # the form will send a POST
        print("FORM DATA:", dict(request.form))

        request_data = dict(request.form)

        if '@' in request_data['email'] and '.' in request_data['email'] and request_data['name'] != '':
            
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials


            # use creds to create a client to interact with the Google Drive API
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

            client = gspread.authorize(creds)

            # # Find a workbook by name and open the first sheet
            # # Make sure you use the right name here.
            sheet = client.open("nhl_daily_email_data").sheet1

            row = [request_data['name'],request_data['email'],request_data['affiliation'],request_data['time_zone']]
            index = 2
            sheet.insert_row(row, index)
            
            
            
            
            
            
            flash("You have been signed up for the NHL Daily Briefing!", "success")
        else:
            flash("Invalid input. Try again.", "danger")

    return render_template("register.html")
