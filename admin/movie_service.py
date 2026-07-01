import pandas as pd
from datetime import datetime

MOVIE_DATASET = "dataset/ai_movies.csv"

MOVIES_PER_PAGE = 50

_movies = None


def load_movies():

    global _movies

    if _movies is None:

        print("Loading Movies Dataset...")

        _movies = pd.read_csv(
            MOVIE_DATASET,
            low_memory=False
        )

        _movies = _movies.fillna("")

        print(f"{len(_movies)} Movies Loaded")

    return _movies


def reload_movies():

    global _movies

    _movies = None

    return load_movies()


def get_movies(

    page=1,

    search="",

    genre="",

    language="",

    sort="rating"

):

    df = load_movies().copy()

    # ---------------- SEARCH ----------------

    if search:

        df = df[
            df["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # ---------------- GENRE ----------------

    if genre:

        df = df[
            df["genres"].str.contains(
                genre,
                case=False,
                na=False
            )
        ]

    # ---------------- LANGUAGE ----------------

    if language:

        df = df[
            df["original_language"] == language
        ]

    # ---------------- SORT ----------------

    if sort == "rating":

        df = df.sort_values(
            "vote_average",
            ascending=False
        )

    elif sort == "year":

        df = df.sort_values(
            "release_date",
            ascending=False
        )

    elif sort == "title":

        df = df.sort_values(
            "title"
        )

    total_movies = len(df)

    total_pages = max(
        1,
        (total_movies + MOVIES_PER_PAGE - 1)
        // MOVIES_PER_PAGE
    )

    start = (page - 1) * MOVIES_PER_PAGE

    end = start + MOVIES_PER_PAGE

    movies = df.iloc[start:end]

    return (

        movies.to_dict("records"),

        total_pages,

        total_movies

    )


def get_all_languages():

    df = load_movies()

    return sorted(

        df["original_language"]

        .dropna()

        .unique()

    )


def get_all_genres():

    df = load_movies()

    genres = set()

    for value in df["genres"]:

        if pd.isna(value):

            continue

        for genre in str(value).split(","):

            genre = genre.strip()

            if genre:

                genres.add(genre)

    return sorted(genres)
def add_movie(data):

    global _movies

    df = load_movies().copy()

    next_id = 1

    if len(df) > 0:

        next_id = int(df["id"].max()) + 1

    new_movie = {

    "id": next_id,

    "imdb_id": data["imdb_id"],

    "title": data["title"],

    "overview": data["overview"],

    "genres": data["genres"],

    "cast": data["cast"],

    "director": data["director"],

    "poster_path": data["poster_path"],

    "release_date": data["release_date"],

    "vote_average": float(data["vote_average"]),

    "popularity": float(data["popularity"]),

    "original_language": data["original_language"]

}

    df = pd.concat(

        [

            df,

            pd.DataFrame([new_movie])

        ],

        ignore_index=True

    )

    df.to_csv(

        MOVIE_DATASET,

        index=False

    )

    reload_movies()
def get_movie(imdb_id):

    df = load_movies()

    movie = df[df["imdb_id"] == imdb_id]

    if movie.empty:
        return None

    return movie.iloc[0].to_dict()
def update_movie(imdb_id, data):

    global _movies

    df = load_movies().copy()

    index = df[df["imdb_id"] == imdb_id].index

    if len(index) == 0:
        return False

    i = index[0]

    for key, value in data.items():

        if key in df.columns:

            df.at[i, key] = value

    df.to_csv(
        MOVIE_DATASET,
        index=False
    )

    reload_movies()

    return True
def delete_movie(imdb_id):

    global _movies

    df = load_movies().copy()

    movie = df[df["imdb_id"] == imdb_id]

    if movie.empty:
        return False

    poster = movie.iloc[0]["poster_path"]

    backdrop = ""

    if "backdrop_path" in movie.columns:

        backdrop = movie.iloc[0]["backdrop_path"]

    df = df[df["imdb_id"] != imdb_id]

    df.to_csv(

        MOVIE_DATASET,

        index=False

    )

    reload_movies()

    return {

        "poster": poster,

        "backdrop": backdrop

    }