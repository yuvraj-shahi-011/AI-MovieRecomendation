import pandas as pd

DATASET_PATH = "dataset/web_series.csv"

# Cache variable
_series = None


def load_series(force_reload=False):

    global _series

    if force_reload:
        _series = None

    if _series is None:
        print("Loading TV Series dataset...")

        _series = pd.read_csv(
            DATASET_PATH,
            low_memory=False
        )

        print(f"Loaded {len(_series)} TV Series")

        # Keep only required columns
        _series = _series[
    [
        "id",
        "name",
        "overview",
        "genres",
        "poster_path",
        "vote_average",
        "vote_count",
        "popularity",
        "origin_country",
        "first_air_date",
        "original_language",
        "number_of_seasons",
        "number_of_episodes",
    ]
]
        # Fill missing values
        feature_columns = [
            "overview",
            "genres",
        ]

        for col in feature_columns:

            _series[col] = (
                _series[col]
                .fillna("")
                .astype(str)
            )

        # Rename columns to match movie project
        _series.rename(
            columns={
                "id": "series_id",
                "name": "title",
                "first_air_date": "release_date",
            },
            inplace=True,
        )

        # Feature column for AI
        _series["features"] = (
            _series["overview"]
            + " "
            + _series["genres"]
        )

    # Keep only high-quality TV Series
    _series = _series[
        (_series["poster_path"].notna()) &
        (_series["poster_path"] != "") &
        (_series["vote_count"] >= 30) &
        (_series["vote_average"] >= 4)
]

    return _series