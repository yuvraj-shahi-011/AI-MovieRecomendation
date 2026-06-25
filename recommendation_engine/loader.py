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

    return _movies