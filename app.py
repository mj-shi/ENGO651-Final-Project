from distutils.log import error
import os
import requests
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Default page redirects
@app.route("/")
def index():
    return redirect("/login")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        loginUsername = request.form.get("username")
        loginPassword = request.form.get("password")
        
        result = db.execute("SELECT * FROM users WHERE username = :username AND password=:password", {"username":loginUsername, "password":loginPassword}).fetchone()
        if result is None:
            return render_template("login.html", message="Invalid username or password.")
        
        session["user_id"] = result[0]
        session["user_name"] = result[1]

        return redirect("/home")
    
    if request.method == "GET":
        return render_template("login.html")

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("register.html", message="Username and Password cannot be blank.")
        registerUsername = request.form.get("username")
        registerPassword = request.form.get("password")

        userExists = db.execute("SELECT * FROM users WHERE username = :username", {"username":registerUsername}).fetchone()
        if not userExists:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username":registerUsername, "password":registerPassword})
            db.commit()
            return render_template("register.html", message="Account created successfully.")
        return render_template("register.html", message="User already exists.")
        
    if request.method == "GET":
        return render_template("register.html")

# Logout Page
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Map Home Page
@app.route("/home", methods=["GET", "POST"])
def home():
    # Checks if user is logged in
    if request.method == "GET":
        if session:
            results = db.execute("SELECT * FROM updates ORDER BY update_time DESC LIMIT 10").fetchall()
            if len(results) == 0:
                return render_template("home.html", message="No Updates", welcome=("Signed in as: "+ session["user_id"]))

            return render_template("home.html", results = results, welcome=("Signed in as: "+ session["user_id"]))
        else:
            return redirect("/login")
    
    if request.method == "POST":
        print("post request")
        if session:
            currentuser = session["user_id"]
            location = request.form.get("locdesc")
            comments = request.form.get("comments")

            if location=="" or comments=="":
                results = db.execute("SELECT * FROM updates ORDER BY update_time DESC LIMIT 10").fetchall()
                if len(results) == 0:
                    return render_template("home.html", message="No Updates", error="All fields must be filled in", welcome=("Signed in as: "+ session["user_id"]))
                return render_template("home.html", results = results, error="All fields must be filled in", welcome=("Signed in as: "+ session["user_id"]))      


            db.execute("INSERT INTO updates (update_user, comments, update_location, update_time) VALUES(:currentuser, :comments, :location, current_timestamp(0))", {"currentuser": currentuser, "comments":comments, "location": location})
            db.commit()

            results = db.execute("SELECT * FROM updates ORDER BY update_time DESC LIMIT 3").fetchall()            
            if len(results) == 0:
                return render_template("home.html", message="No Updates", welcome=("Signed in as: "+ session["user_id"]))

            return render_template("home.html", message="Update Posted", results = results, welcome=("Signed in as: "+ session["user_id"]))
        
        else:
            return redirect("/login")