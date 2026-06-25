import pandas as pd

DATASET_PATH = "dataset/processed_movies.csv"

# Cache variable
_movies = None


def load_movies():
    global _movies

    if _movies is None:
        print("Loading processed dataset...")

        _movies = pd.read_csv(
            DATASET_PATH,
            low_memory=False
        )

        print(f"Loaded {len(_movies)} movies")

        # Fill missing values
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

        # Create feature column
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