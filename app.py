from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from pathlib import Path
import sqlite3
import requests
import os

# Load .env from same folder as app.py
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

print("ENV FILE:", env_path)
print("OMDB_API_KEY =", OMDB_API_KEY)
print("SECRET_KEY =", SECRET_KEY)

app = Flask(__name__)
app.secret_key = SECRET_KEY


# HOME PAGE
@app.route("/")
def home():

    movie_names = [
        "The Dark Knight",
        "Interstellar",
        "Joker",
        "Avengers: Endgame"
    ]

    popular = []

    for name in movie_names:
        try:
            url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={name}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get("Response") == "True":
                popular.append({
                    "title": data.get("Title"),
                    "poster": data.get("Poster")
                })

        except Exception as e:
            print("Error:", e)

    return render_template(
        "index.html",
        popular=popular,
        user=session.get("user")
    )
# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """,
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/")

        return "Invalid Email or Password"

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


# SEARCH
@app.route("/search")
def search():

    movie = None

    movie_name = request.args.get("movie")

    if movie_name:

        try:
            url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_name}"

            response = requests.get(url, timeout=10)

            movie = response.json()

            if movie.get("Response") == "False":
                movie = None

        except Exception as e:
            print("Search Error:", e)
            movie = None

    return render_template(
        "search.html",
        movie=movie
    )
if __name__ == "__main__":
    app.run(debug=True)