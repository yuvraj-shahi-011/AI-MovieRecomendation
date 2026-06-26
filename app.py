from flask import Flask, render_template, request, redirect, session, flash, url_for
from recommendation_engine.recommender import recommend_movies
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import requests
import os

# =========================
# LOAD ENV VARIABLES
# =========================

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    return conn


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

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
            print(data)
            if data.get("Response") == "True":

                popular.append({
                    "title": data["Title"],
                    "poster": data["Poster"],
                    "imdb_id": data["imdbID"]
                })

        except Exception as e:
            print("Movie Error:", e)
    print("HOME SESSION USER:", session.get("user"))        

    return render_template(
        "index.html",
        popular=popular,
        user=session.get("user")
    )


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
                """,
                (username, email, password)
            )

            conn.commit()

            cursor.close()
            conn.close()
            flash("Registration successful!", "success")
            return redirect("/login")

        except Exception as e:
            flash(f"Registration Error: {e}", "error")

    return render_template(
        "register.html",
        user=session.get("user")
    )


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE email=%s AND password=%s
                """,
                (email, password)
            )

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                session["user"] = user[0]
                return redirect("/")
            flash("Invalid Email or Password", "error")
        except Exception as e:
            flash(f"Login Error: {e}", "error")

    return render_template(
        "login.html",
        user=session.get("user")
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


# =========================
# SEARCH MOVIES
# =========================

@app.route("/search")
def search():

    if "user" not in session:
        return redirect("/login")

    movie_name = request.args.get("movie")

    if not movie_name:
        return redirect("/")

    try:

        url = (
            f"https://www.omdbapi.com/"
            f"?apikey={OMDB_API_KEY}"
            f"&t={movie_name}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        movie = response.json()

        if movie.get("Response") == "True":

            return redirect(
                url_for(
                    "movie_detail",
                    imdb_id=movie["imdbID"]
                )
            )

        return render_template(
            "search.html",
            movie=None,
            error="Movie not found.",
            user=session.get("user")
        )

    except Exception as e:

        print("Search Error:", e)

        return render_template(
            "search.html",
            movie=None,
            error="Something went wrong.",
            user=session.get("user")
        )

# =========================
# MOVIE DETAIL
# =========================

@app.route("/movie/<imdb_id>")
def movie_detail(imdb_id):

    if "user" not in session:
        return redirect("/login")

    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"

    recommendations = []

    try:
        response = requests.get(url, timeout=10)
        movie = response.json()

        if movie.get("Response") == "True":
            recommendations = recommend_movies(imdb_id)
            if recommendations is not None:
                recommendations = recommendations.to_dict(orient="records")
            else:
                recommendations = []
    except Exception as e:
        print("Movie Detail Error:", e)
        movie = None

    return render_template(
        "movie.html",
        movie=movie,
        recommendations=recommendations,
        user=session.get("user")
    )

# =========================
# ADD_TO_WATCHLIST
# =========================

@app.route("/add_watchlist", methods=["POST"])
def add_watchlist():

    if "user" not in session:
        return redirect("/login")

    title = request.form["title"]
    poster = request.form["poster"]
    imdb_id = request.form["imdb_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if movie already exists
    cursor.execute(
        """
        SELECT id
        FROM watchlist
        WHERE username=%s
        AND imdb_id=%s
        """,
        (session["user"], imdb_id)
    )

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        conn.close()
        flash("Movie already in watchlist!", "error")
        return redirect("/search?movie=" + title)

    # Insert movie
    cursor.execute(
        """
        INSERT INTO watchlist
        (username, movie_title, poster, imdb_id)
        VALUES (%s, %s, %s, %s)
        """,
        (session["user"], title, poster, imdb_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Movie added to watchlist!", "success")
    return redirect("/watchlist")

# =========================
# REMOVE FROM WATCHLIST
# =========================

@app.route("/remove_watchlist/<imdb_id>")
def remove_watchlist(imdb_id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM watchlist
        WHERE username=%s
        AND imdb_id=%s
        """,
        (session["user"], imdb_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Movie removed from watchlist!", "danger")
    return redirect("/watchlist")

# =========================
# WATCHLIST
# =========================

@app.route("/watchlist")
def watchlist():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT movie_title, poster, imdb_id
        FROM watchlist
        WHERE username=%s
        ORDER BY created_at DESC
        """, (session["user"],))

    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "watchlist.html",
        movies=movies,
        user=session.get("user")
    )

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)