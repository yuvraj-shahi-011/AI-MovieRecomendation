import pandas as pd

DATASET_PATH = "dataset/ai_movies.csv"

_movies = None


def load_movies(force_reload=False):

    global _movies

    if force_reload:

        _movies = None

    if _movies is None:

        print("Loading AI dataset...")

        _movies = pd.read_csv(

            DATASET_PATH,

            low_memory=False

        )

        print(f"Loaded {len(_movies)} movies")

        feature_columns = [

            "overview",

            "genres",

            "cast",

            "director"

        ]

        for col in feature_columns:

            _movies[col] = (

                _movies[col]

                .fillna("")

                .astype(str)

            )

        _movies["features"] = (

            _movies["overview"]

            + " "

            + _movies["genres"]

            + " "

            + _movies["cast"]

            + " "

            + _movies["director"]

        )

    return _movies