from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)
import os
from pathlib import Path
import psycopg2
import requests
import pandas as pd
from dotenv import load_dotenv
from rapidfuzz import process, fuzz

# -----------------------------
# Recommendation Engine
# -----------------------------

from recommendation_engine.recommender import recommend_movies
from recommendation_engine.series_recommender import recommend_series
from recommendation_engine.vector_store import (
    load_vector_store,
    reload_vector_store
)

from recommendation_engine.loader_series import load_series

# -----------------------------
# Admin
# -----------------------------

from admin import admin_bp


# =========================
# Helper Functions
# =========================

def get_movies():

    movies, _ = load_vector_store()

    return movies


def get_series():

    return load_series(force_reload=True)


# =========================
# LOAD ENV
# =========================

env_path = Path(__file__).parent / ".env"

load_dotenv(env_path)

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)

app.secret_key = SECRET_KEY

@app.template_filter("poster_url")
def poster_url(path):

    if not path:
        return url_for(
            "static",
            filename="images/no-poster.png"
        )

    path = str(path)

    if path.startswith("/"):

        return "https://image.tmdb.org/t/p/w500" + path

    return url_for(
        "static",
        filename="uploads/posters/" + path
    )

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
# MOVIE HOME PAGE
# =========================
@app.route("/")
@app.route("/movies")
def movie_home():

    if "user" not in session:
        return redirect("/login")

    movies = get_movies()

    def sample_df(df):

        if len(df) == 0:
            return []

        return df.sample(
            min(100, len(df))
        ).to_dict(orient="records")
    trending_movies = (
    movies
    .sort_values(
        "popularity",
        ascending=False
    )
    .head(100)
    .to_dict(orient="records")
    )   

    bollywood = sample_df(
        movies[
            movies["original_language"] == "hi"
        ]
    )

    fantasy = sample_df(
        movies[
            movies["genres"].str.contains(
                "Fantasy",
                case=False,
                na=False
            )
        ]
    )

    action = sample_df(
        movies[
            movies["genres"].str.contains(
                "Action",
                case=False,
                na=False
            )
        ]
    )

    comedy = sample_df(
        movies[
            movies["genres"].str.contains(
                "Comedy",
                case=False,
                na=False
            )
        ]
    )

    horror = sample_df(
        movies[
            movies["genres"].str.contains(
                "Horror",
                case=False,
                na=False
            )
        ]
    )

    romance = sample_df(
        movies[
            movies["genres"].str.contains(
                "Romance",
                case=False,
                na=False
            )
        ]
    )

    drama = sample_df(
        movies[
            movies["genres"].str.contains(
                "Drama",
                case=False,
                na=False
            )
        ]
    )

    thriller = sample_df(
        movies[
            movies["genres"].str.contains(
                "Thriller",
                case=False,
                na=False
            )
        ]
    )

    crime = sample_df(
        movies[
            movies["genres"].str.contains(
                "Crime",
                case=False,
                na=False
            )
        ]
    )

    family = sample_df(
        movies[
            movies["genres"].str.contains(
                "Family",
                case=False,
                na=False
            )
        ]
    )

    animation = sample_df(
        movies[
            movies["genres"].str.contains(
                "Animation",
                case=False,
                na=False
            )
        ]
    )

    adventure = sample_df(
        movies[
            movies["genres"].str.contains(
                "Adventure",
                case=False,
                na=False
            )
        ]
    )

    science_fiction = sample_df(
        movies[
            movies["genres"].str.contains(
                "Science Fiction",
                case=False,
                na=False
            )
        ]
    )

    mystery = sample_df(
        movies[
            movies["genres"].str.contains(
                "Mystery",
                case=False,
                na=False
            )
        ]
    )

    documentary = sample_df(
        movies[
            movies["genres"].str.contains(
                "Documentary",
                case=False,
                na=False
            )
        ]
    )

    tv_movie = sample_df(
        movies[
            movies["genres"].str.contains(
                "TV Movie",
                case=False,
                na=False
            )
        ]
    )

    music = sample_df(
        movies[
            movies["genres"].str.contains(
                "Music",
                case=False,
                na=False
            )
        ]
    )

    history = sample_df(
        movies[
            movies["genres"].str.contains(
                "History",
                case=False,
                na=False
            )
        ]
    )

    war = sample_df(
        movies[
            movies["genres"].str.contains(
                "War",
                case=False,
                na=False
            )
        ]
    )

    western = sample_df(
        movies[
            movies["genres"].str.contains(
                "Western",
                case=False,
                na=False
            )
        ]
    )

    return render_template(

        "index.html",
        trending_movies=trending_movies,
        bollywood=bollywood,
        fantasy=fantasy,
        action=action,
        comedy=comedy,
        horror=horror,
        romance=romance,
        drama=drama,
        thriller=thriller,
        crime=crime,
        family=family,
        animation=animation,
        adventure=adventure,
        science_fiction=science_fiction,
        mystery=mystery,
        documentary=documentary,
        tv_movie=tv_movie,
        music=music,
        history=history,
        war=war,
        western=western,

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
    print("Login route called")
    if request.method == "POST":
        print("POST request received")

        email = request.form["email"]
        password = request.form["password"]

        try:
            print("DB_HOST =", os.getenv("DB_HOST"))
            print("DB_NAME =", os.getenv("DB_NAME"))
            print("DB_USER =", os.getenv("DB_USER"))
            print("SECRET_KEY loaded =", bool(app.secret_key))

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
                print("User found:", user)
                session["user"] = user[0]
                print("Session user:", session.get("user"))
                return redirect("/")
            print("User not found")
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
# SEARCH 
# =========================
@app.route("/search")
def search():

    if "user" not in session:
        return redirect("/login")

    movies = get_movies()

    series = get_series()

    movie_titles = movies["title"].fillna("").astype(str).tolist()

    series_titles = series["title"].fillna("").astype(str).tolist()

    movie_title_to_index = {

        title: idx

        for idx, title in enumerate(movie_titles)

    }

    series_title_to_index = {

        title: idx

        for idx, title in enumerate(series_titles)

    }

    query = request.args.get("q", "").strip()

    movie_results = []

    series_results = []

    if query:

        # ---------------- Movies ----------------

        movie_df = movies[

            (

                movies["title"].str.contains(
                    query,
                    case=False,
                    na=False
                )

            )

            |

            (

                movies["genres"].str.contains(
                    query,
                    case=False,
                    na=False
                )

            )

            |

            (

                movies["cast"].str.contains(
                    query,
                    case=False,
                    na=False
                )

            )

            |

            (

                movies["director"].str.contains(
                    query,
                    case=False,
                    na=False
                )

            )

        ].head(100)

        if movie_df.empty:

            matches = process.extract(

                query,

                movie_titles,

                scorer=fuzz.WRatio,

                limit=30

            )

            indices = [

                movie_title_to_index[title]

                for title, score, _ in matches

                if score >= 70

            ]

            if indices:

                movie_df = movies.iloc[indices]

        movie_results = movie_df.to_dict("records")

        # ---------------- Series ----------------

        series_df = series[

            (

                series["title"].str.contains(
                    query,
                    case=False,
                    na=False
                )

            )

            |

            (

                series["genres"].str.contains(
                    query,
                    case=False,
                    na=False
                )

            )

            |

            (

                series["overview"].str.contains(
                    query,
                    case=False,
                    na=False
                )

            )

        ].head(100)

        if series_df.empty:

            matches = process.extract(

                query,

                series_titles,

                scorer=fuzz.WRatio,

                limit=30

            )

            indices = [

                series_title_to_index[title]

                for title, score, _ in matches

                if score >= 70

            ]

            if indices:

                series_df = series.iloc[indices]

        series_results = series_df.to_dict("records")

        for tv in series_results:

            if not isinstance(tv.get("release_date"), str):

                tv["release_date"] = "N/A"

    return render_template(

        "search.html",

        query=query,

        movies=movie_results,

        series=series_results,

        user=session.get("user")

    )

# =========================
# SERIES HOME PAGE
# =========================

@app.route("/series")
def series_home():

    if "user" not in session:
        return redirect("/login")

    series = get_series()

    filtered = series[
        (series["poster_path"].notna()) &
        (series["poster_path"] != "") &
        (series["vote_average"] >= 5.5) &
        (series["vote_count"] >= 50)
    ]

    def get_genre(genre, sort_by="vote_average"):

        df = filtered[
            filtered["genres"].str.contains(
                genre,
                case=False,
                na=False
            )
        ]

        if df.empty:
            return []

        return (
            df.sort_values(
                sort_by,
                ascending=False
            )
            .head(100)
            .to_dict(orient="records")
        )

    trending = (
        filtered
        .sort_values(
            "popularity",
            ascending=False
        )
        .head(100)
        .to_dict(orient="records")
    )

    top_rated = (
        filtered
        .sort_values(
            ["vote_average", "vote_count"],
            ascending=False
        )
        .head(100)
        .to_dict(orient="records")
    )

    popular = (
        filtered
        .sort_values(
            "vote_count",
            ascending=False
        )
        .head(100)
        .to_dict(orient="records")
    )

    indian = (
        filtered[
            filtered["origin_country"]
            .astype(str)
            .str.contains(
                "IN",
                case=False,
                na=False
            )
        ]
        .sort_values(
            "popularity",
            ascending=False
        )
        .head(100)
        .to_dict(orient="records")
    )

    return render_template(

        "series.html",

        trending=trending,
        top_rated=top_rated,
        popular=popular,
        indian=indian,

        drama=get_genre("Drama"),
        comedy=get_genre("Comedy"),
        action=get_genre("Action|Adventure", "popularity"),
        crime=get_genre("Crime"),
        fantasy=get_genre("Fantasy"),
        romance=get_genre("Romance"),
        mystery=get_genre("Mystery"),
        animation=get_genre("Animation"),
        family=get_genre("Family"),

        user=session.get("user")

    )

# =========================
# SERIES DETAIL
# =========================

@app.route("/series/<int:series_id>")
def series_detail(series_id):

    if "user" not in session:
        return redirect("/login")

    series = get_series()

    selected = series[
        series["series_id"] == series_id
    ]

    if selected.empty:
        flash("TV Series not found.", "error")
        return redirect("/series")

    selected = selected.iloc[0]

    language_map = {
        "en": "English",
        "hi": "Hindi",
        "ta": "Tamil",
        "te": "Telugu",
        "ml": "Malayalam",
        "kn": "Kannada",
        "bn": "Bengali",
        "mr": "Marathi",
        "pa": "Punjabi",
        "gu": "Gujarati",
        "ur": "Urdu",
        "fr": "French",
        "es": "Spanish",
        "de": "German",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "ru": "Russian"
    }

    language = language_map.get(
        selected["original_language"],
        str(selected["original_language"]).upper()
    )

    # ---------------- Poster ----------------

    poster_path = selected.get("poster_path")

    if (
        pd.notna(poster_path)
        and str(poster_path).strip() != ""
        and str(poster_path).lower() != "nan"
    ):

        if str(poster_path).startswith("/"):
            poster = (
                "https://image.tmdb.org/t/p/w500"
                + str(poster_path)
            )
        else:
            poster = url_for(
                "static",
                filename="uploads/posters/" + str(poster_path)
            )

    else:
        poster = url_for(
            "static",
            filename="images/no-poster.png"
        )

    release_date = selected.get("release_date")

    if pd.isna(release_date):
        release_date = "N/A"

    series_data = {
        "seriesID": selected["series_id"],
        "Title": selected["title"],
        "Plot": selected["overview"],
        "Genre": selected["genres"],
        "Released": release_date,
        "Language": language,
        "imdbRating": selected["vote_average"],
        "Seasons": selected["number_of_seasons"],
        "Episodes": selected["number_of_episodes"],
        "Poster": poster
    }

    recommendations = recommend_series(series_id)

    if recommendations is not None:

        recommendations = recommendations.to_dict(
            orient="records"
        )

        for rec in recommendations:

            poster_path = rec.get("poster_path")

            if (
                pd.notna(poster_path)
                and str(poster_path).strip() != ""
                and str(poster_path).lower() != "nan"
            ):

                if str(poster_path).startswith("/"):
                    rec["Poster"] = (
                        "https://image.tmdb.org/t/p/w500"
                        + str(poster_path)
                    )
                else:
                    rec["Poster"] = url_for(
                        "static",
                        filename="uploads/posters/" + str(poster_path)
                    )

            else:
                rec["Poster"] = url_for(
                    "static",
                    filename="images/no-poster.png"
                )

            if not isinstance(rec.get("release_date"), str):
                rec["release_date"] = "N/A"

    else:
        recommendations = []

    return render_template(
        "series_detail.html",
        series=series_data,
        recommendations=recommendations,
        user=session.get("user")
    )
# =========================
# MOVIE DETAIL
# =========================

@app.route("/movie/<imdb_id>")
def movie_detail(imdb_id):

    if "user" not in session:
        return redirect("/login")

    movies = get_movies()

    movie = movies[movies["imdb_id"] == imdb_id]

    if movie.empty:
        flash("Movie not found.", "error")
        return redirect("/")

    movie = movie.iloc[0]

    language_map = {
        "en": "English",
        "hi": "Hindi",
        "ta": "Tamil",
        "te": "Telugu",
        "ml": "Malayalam",
        "kn": "Kannada",
        "bn": "Bengali",
        "mr": "Marathi",
        "pa": "Punjabi",
        "gu": "Gujarati",
        "ur": "Urdu",
        "fr": "French",
        "es": "Spanish",
        "de": "German",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "ru": "Russian"
    }

    language = language_map.get(
        movie["original_language"],
        str(movie["original_language"]).upper()
    )

    # ---------------- Poster ----------------

    poster_path = movie.get("poster_path")

    if (
        pd.notna(poster_path)
        and str(poster_path).strip() != ""
        and str(poster_path).lower() != "nan"
    ):

        if str(poster_path).startswith("/"):
            poster = "https://image.tmdb.org/t/p/w500" + str(poster_path)
        else:
            poster = url_for(
                "static",
                filename="uploads/posters/" + str(poster_path)
            )

    else:
        poster = url_for(
            "static",
            filename="images/no-poster.png"
        )

    release_date = movie.get("release_date")

    if pd.isna(release_date):
        release_date = "N/A"

    movie_data = {
        "imdbID": movie["imdb_id"],
        "Title": movie["title"],
        "Plot": movie["overview"],
        "Genre": movie["genres"],
        "Actors": movie["cast"],
        "Director": movie["director"],
        "Released": release_date,
        "Year": str(release_date)[:4] if release_date != "N/A" else "N/A",
        "Language": language,
        "Runtime": "N/A",
        "imdbRating": movie["vote_average"],
        "Poster": poster
    }

    recommendations = recommend_movies(imdb_id)

    if recommendations is not None:

        recommendations = recommendations.to_dict(orient="records")

        for rec in recommendations:

            poster_path = rec.get("poster_path")

            if (
                pd.notna(poster_path)
                and str(poster_path).strip() != ""
                and str(poster_path).lower() != "nan"
            ):

                if str(poster_path).startswith("/"):
                    rec["Poster"] = (
                        "https://image.tmdb.org/t/p/w500"
                        + str(poster_path)
                    )
                else:
                    rec["Poster"] = url_for(
                        "static",
                        filename="uploads/posters/" + str(poster_path)
                    )

            else:
                rec["Poster"] = url_for(
                    "static",
                    filename="images/no-poster.png"
                )

            if not isinstance(rec.get("release_date"), str):
                rec["release_date"] = "N/A"

    else:
        recommendations = []

    return render_template(
        "movie.html",
        movie=movie_data,
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
    content_id = request.form["content_id"]
    content_type = request.form["content_type"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM watchlist
        WHERE username=%s
        AND content_id=%s
        AND content_type=%s
        """,
        (
            session["user"],
            content_id,
            content_type
        )
    )

    if cursor.fetchone():

        cursor.close()
        conn.close()

        flash(
            "Already in watchlist!",
            "warning"
        )

        return redirect(request.referrer)

    cursor.execute(
        """
        INSERT INTO watchlist
        (
            username,
            movie_title,
            poster,
            imdb_id,
            content_type,
            content_id
        )

        VALUES
        (
            %s,%s,%s,%s,%s,%s
        )
        """,
        (
            session["user"],
            title,
            poster,
            content_id,
            content_type,
            content_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Added to Watchlist!",
        "success"
    )

    return redirect("/watchlist")

# =========================
# REMOVE FROM WATCHLIST
# =========================

@app.route("/remove_watchlist/<content_type>/<content_id>")
def remove_watchlist(content_type, content_id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM watchlist
        WHERE username=%s
        AND content_type=%s
        AND content_id=%s
        """,
        (
            session["user"],
            content_type,
            content_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Removed from watchlist!", "success")

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

    cursor.execute(
        """
        SELECT
            movie_title,
            poster,
            content_id,
            content_type

        FROM watchlist

        WHERE username=%s

        ORDER BY created_at DESC
        """,
        (session["user"],)
    )

    watchlist_items = cursor.fetchall()
    print("=" * 60)
    print(watchlist_items)
    print("=" * 60)

    cursor.close()
    conn.close()

    return render_template(
        "watchlist.html",
        watchlist_items=watchlist_items,
        user=session.get("user")
    )

# =========================
# RUN APP
# =========================
app.register_blueprint(admin_bp)
print(app.url_map)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
    