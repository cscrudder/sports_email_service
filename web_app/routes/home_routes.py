# web_app/routes/home_routes.py

from flask import Blueprint, request, render_template, jsonify, render_template, redirect, flash # FYI new imports


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
