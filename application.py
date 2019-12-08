import os
import requests
from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

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



#Funciones extra
def average(reviews):
    if len(reviews) > 0:
        rating = 0
        for review in reviews :
            rating += review.rating
        rating = rating / len(reviews)
        return rating
    else:
        return 0
   

#Querys Base de datos 

def search_books(str):
      data = db.execute("SELECT * FROM books WHERE title LIKE '%"+str+"%' or  author LIKE '%"+str+"%' or  isbn LIKE '%"+str+"%';").fetchall()
      return data

def search_book(str):
      book = db.execute("SELECT * FROM books WHERE isbn = '"+str+"';").fetchall()
      reviews = db.execute("SELECT * FROM reviews WHERE isbn = '"+str+"';").fetchall()
      return book, reviews



#Navegacion


@app.route("/")
def index():
    return  render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if (request.method ==  "GET"):  
        return render_template("register_form.html")

    elif (request.method ==  "POST"):  

        # Get form information.
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Make sure flight exists.
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
            return render_template("no_success.html")
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username": username, "password": password})
        db.commit()
        return render_template("success.html")

@app.route("/login", methods=["POST"])
def login():
    """Register new user"""

    # Get form information.
    username = request.form.get("username")
    password = request.form.get("password")
      
    # Make sure flight exists.
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount > 0:
        db.execute("UPDATE users SET logged = '1' WHERE username = :username AND password = :password", {"username": username, "password": password})
        db.commit()
        session["up"] = []
        session["up"].append(username)
        session["up"].append(password)
        return redirect(url_for('search'))

    return render_template("error_pass.html")

@app.route("/logout")
def logout():
    """Register new user"""

    # Get form information.
    username = session["up"][0]
    password = session["up"][1]
      
    # Make sure flight exists.
    db.execute("UPDATE users SET logged = '0' WHERE username = :username AND password = :password", {"username": username, "password": password})
    db.commit()


    return render_template("index.html")


@app.route("/search", methods = ["GET","POST"])
def search():
    results = 0
    if request.method ==  "POST":     
        search_data = request.form.get("search_data")
        results = search_books(search_data)

    return render_template("search.html", results = results)


@app.route("/search/<string:isbn>", methods = ["GET"])
def search_book2(isbn):
    book, reviews = search_book(isbn)
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "BMMuRMuhdcBuBOgYl3kwQ", "isbns": isbn})
    if len(book) == 0:
        return render_template('404.html'), 404
    return render_template("books.html", book = book[0], reviews = reviews, isbn = isbn, res = res.json()['books'][0])


@app.route("/review_sub/<string:ISBN>", methods=["POST"])
def reviews(ISBN):
    """Register new user"""

    # Get form information.
    username = session["up"][0]
    isbn = ISBN
    
    rating = request.form.get("rating")
    review = request.form.get("review")
    # Make sure flight exists.
    if db.execute("SELECT * FROM reviews WHERE username = :username AND isbn = :isbn", {"username": username, "isbn": isbn}).rowcount == 0:
        db.execute("INSERT INTO reviews (isbn, username, rating, review) VALUES (:isbn, :username, :rating, :review)",
            {"username": username, "isbn": isbn, "rating": rating, "review":review})
        db.commit()
        return render_template("review-new.html")
    else:
        db.execute("UPDATE reviews SET rating = :rating, review = :review WHERE username = :username AND isbn = :isbn", {"username": username, "isbn": isbn, "rating": rating, "review":review})
        db.commit()
        return render_template("review-update.html")



@app.route("/review/<string:ISBN>", methods = ["GET"])
def review(ISBN):
    isbn = ISBN
    return render_template("review.html", isbn = isbn)




@app.route("/api/<string:isbn>", methods = ["GET"])
def api(isbn):

    book, reviews = search_book(isbn)

    if len(book) == 0:
        return render_template('404.html', title = '404'), 404
    else :
        book = book[0]
        json_res = {
        "title": book.title,
        "author": book.author,
        "year": int(book.year),
        "isbn": book.isbn,
        "review_count": len(reviews),
        "average_score": average(reviews)
        }
        return json_res, 200





#set FLASK_APP=application.py

#set DATABASE_URL=postgres://trgzqcnracvcxr:95c3dc26df8688c7e8f94401454c25dce83a94a5c19c0f3bba4694b7643c0db0@ec2-54-235-104-136.compute-1.amazonaws.com:5432/d40b302ipd1hj5