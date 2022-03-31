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

# Login 
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        loginUsername = request.form.get("username")
        loginPassword = request.form.get("password")
        
        result = db.execute("SELECT * FROM users WHERE username = :username AND password=:password", {"username":loginUsername, "password":loginPassword}).fetchone()
        if result is None:
            return render_template("index.html", message="Invalid username or password.")
        
        session["user_id"] = result[0]
        session["user_name"] = result[1]

        return redirect("/home")
    
    if request.method == "GET":
        return render_template("index.html")

# Register
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

# Logout 
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

""" # Homepage 
@app.route("/home", methods=["GET", "POST"])
def home():
    # Search book logic
    if request.method == "POST":
        search = request.form.get("search")
        if not search:
            return render_template("home.html", message="ERROR: You must provide information of the book (Title/Author/ISBN)", welcome=("Welcome "+ session["user_id"]))
        query = "%"+search+"%"
        results = db.execute("SELECT * FROM books WHERE title ILIKE :query OR author ILIKE :query OR isbn ILIKE :query", {"query": query}).fetchall()

        if len(results) == 0:
            return render_template("home.html", message="No Results Found.", welcome=("Welcome "+ session["user_id"]))
        
        return render_template("home.html", results=results, welcome=("Welcome "+ session["user_id"]))
    
    # Checks if user is logged in
    if request.method == "GET":
        if session:
            return render_template("home.html", welcome=("Welcome "+ session["user_id"]))
        else:
            return redirect("/login")

# Book Details
@app.route("/details/<int:id>", methods=["GET", "POST"])
def details(id):
    if session:
        #Get book and reviews
        book = db.execute("SELECT * FROM books WHERE id = :id", {"id": id}).fetchone()

        reviews = []
        results = db.execute("SELECT * FROM reviews WHERE book_id = :id", {"id":id}).fetchall()
        for review in results:
            reviewUser = db.execute("SELECT * FROM users WHERE id = :id", {"id": review.user_id}).fetchone()
            reviews.append((reviewUser.username, review.rating, review.comments))
        
        # Access Google Books API
        reviewData = []
        paramString = "isbn:"+ book.isbn
        res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": paramString})
        if res.status_code != 200:
            reviewData = ("","")
        else:
            data = res.json()
            averageRating = data['items'][0]['volumeInfo']['averageRating']
            ratingsCount = data['items'][0]['volumeInfo']['ratingsCount']
            reviewData = [averageRating, ratingsCount] 

        #Post review logic
        if request.method == "POST":
            currentuser = session["user_id"]
            userResult = db.execute("SELECT * FROM users WHERE username = :currentuser", {"currentuser": currentuser}).fetchone()
            userid = userResult.id

            reviewExists = db.execute("SELECT * FROM reviews WHERE user_id = :userid AND book_id = :id", {"userid": userid, "id": id}).fetchall()
            if reviewExists:
                return render_template("details.html", message="You have already reviewed this book.", book = book, reviews = reviews, reviewData = reviewData)
            
            rating = request.form.get("rating")
            comments = request.form.get("comments")

            db.execute("INSERT INTO reviews (user_id, book_id, rating, comments) VALUES(:userid, :id, :rating, :comments)", {"userid": userid, "id": id, "rating": rating, "comments": comments})
            db.commit()
            reviews.append((currentuser, rating, comments))
            return render_template("details.html", message="Review submitted.", book = book, reviews = reviews, reviewData = reviewData)
        return render_template("details.html", book = book, reviews = reviews, reviewData = reviewData)
    else:
        return redirect("/login")        

# API call to website
@app.route("/api/<isbn>", methods=["GET"])
def api_call(isbn):
    # Check db for book
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if not book:
        return jsonify({"error": "Book not found"}), 404

    paramString = "isbn:"+isbn
    # Access Google Books API
    res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": paramString})
    if res.status_code != 200:
        averageRating = 0
        ratingsCount = 0
        isbnTen = ""
        isbnThirteen = ""
    else:
        data = res.json()
        averageRating = data['items'][0]['volumeInfo']['averageRating']
        ratingsCount = data['items'][0]['volumeInfo']['ratingsCount']
        isbnTen = data['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier']
        isbnThirteen = data['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
    
    # Get database review data
    results = db.execute("SELECT * FROM reviews WHERE book_id = :id", {"id": book.id}).fetchall()
    ratingsTotal = 0
    reviewsCount = len(results)
    for row in results:
        ratingsTotal += row.rating
    
    # Calculate combined rating and count of reviews
    ratingsTotal += (ratingsCount * averageRating)
    reviewsCount += ratingsCount
    totalAverage = ratingsTotal / reviewsCount
    totalAverage = float('%.2f'%totalAverage)

    # Return json 
    return jsonify({
        "title": book.title,
        "author": book.author,
        "publishedDate": book.year,
        "ISBN_10": isbnTen,
        "ISBN_13": isbnThirteen,
        "reviewCount": reviewsCount,
        "averageRating": totalAverage
    })

 """