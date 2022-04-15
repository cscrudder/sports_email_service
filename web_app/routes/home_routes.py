# web_app/routes/home_routes.py

from flask import Blueprint, request, render_template

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
@home_routes.route("/home")
def home():
    return render_template("home.html")

@home_routes.route("/sample")
def sample():
    return render_template("sample.html")

@home_routes.route("/register")
def register():
    return render_template("register.html")