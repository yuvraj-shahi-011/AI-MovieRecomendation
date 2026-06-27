from flask import Flask, render_template, request, redirect, session, flash, url_for
from recommendation_engine.recommender import recommend_movies, movies
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from movie_categories import *
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
print("Movies available:", len(movies))


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

    # Bollywood
    bollywood = movies[
        movies["original_language"] == "hi"
    ].sample(12)

    # Action
    action = movies[
        movies["genres"].str.contains("Action", case=False, na=False)
    ].sample(12)

    # Comedy
    comedy = movies[
        movies["genres"].str.contains("Comedy", case=False, na=False)
    ].sample(12)

    # Horror
    horror = movies[
        movies["genres"].str.contains("Horror", case=False, na=False)
    ].sample(12)

    # Romance
    romance = movies[
        movies["genres"].str.contains("Romance", case=False, na=False)
    ].sample(12)

    return render_template(
        "index.html",
        bollywood=bollywood.to_dict(orient="records"),
        action=action.to_dict(orient="records"),
        comedy=comedy.to_dict(orient="records"),
        horror=horror.to_dict(orient="records"),
        romance=romance.to_dict(orient="records"),
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

    movie_name = request.args.get("movie", "").strip()

    if not movie_name:
        return redirect("/")

    try:

        # Search movie in AI dataset
        movie = movies[
            movies["title"].str.lower() == movie_name.lower()
        ]

        if not movie.empty:

            movie = movie.iloc[0]

            return redirect(
                url_for(
                    "movie_detail",
                    imdb_id=movie["imdb_id"]
                )
            )

        # Partial search if exact title is not found
        movie = movies[
            movies["title"].str.lower().str.contains(
                movie_name.lower(),
                na=False
            )
        ]

        if not movie.empty:

            movie = movie.iloc[0]

            return redirect(
                url_for(
                    "movie_detail",
                    imdb_id=movie["imdb_id"]
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

    # Search movie in AI dataset
    movie = movies[
        movies["imdb_id"] == imdb_id
    ]

    if movie.empty:
        flash("Movie not found.", "error")
        return redirect("/")

    movie = movie.iloc[0]

    # Convert Pandas row into dictionary
    movie = {
    "imdbID": movie["imdb_id"],
    "Title": movie["title"],
    "Plot": movie["overview"],
    "Genre": movie["genres"],
    "Actors": movie["cast"],
    "Director": movie["director"],
    "Released": movie["release_date"],
    "Year": movie["release_date"][:4] if movie["release_date"] else "N/A",
    "Language": movie["original_language"],
    "Runtime": "N/A",
    "imdbRating": movie["vote_average"],
    "Poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
}

    # AI Recommendations
    recommendations = recommend_movies(imdb_id)

    if recommendations is not None:

        recommendations = recommendations.to_dict(orient="records")

        for rec in recommendations:

            rec["Poster"] = (
                f"https://image.tmdb.org/t/p/w500{rec['poster_path']}"
            )

    else:
        recommendations = []

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