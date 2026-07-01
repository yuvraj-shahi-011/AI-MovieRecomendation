from narwhals import new_series
import pandas as pd

SERIES_DATASET = "dataset/web_series.csv"

SERIES_PER_PAGE = 50

_series = None


def load_series():

    global _series

    if _series is None:

        print("Loading Series Dataset...")

        _series = pd.read_csv(
            SERIES_DATASET,
            low_memory=False
        )

        _series = _series.fillna("")

        print(f"{len(_series)} Series Loaded")

    return _series


def reload_series():

    global _series

    _series = None

    return load_series()


def get_series(

    page=1,

    search=""

):

    df = load_series().copy()

    if search:

        df = df[

            df["name"].str.contains(

                search,

                case=False,

                na=False

            )

        ]

    df = df.sort_values(

        by="vote_average",

        ascending=False

    )

    total_series = len(df)

    total_pages = max(

        1,

        (total_series + SERIES_PER_PAGE - 1)

        // SERIES_PER_PAGE

    )

    start = (page - 1) * SERIES_PER_PAGE

    end = start + SERIES_PER_PAGE

    series = df.iloc[start:end]

    return (

        series.to_dict("records"),

        total_pages,

        total_series

    )


def get_series_by_id(series_id):

    df = load_series()

    row = df[df["id"] == int(series_id)]

    if row.empty:

        return None

    return row.iloc[0].to_dict()


def add_series(data):

    global _series

    df = load_series().copy()

    next_id = 1

    if len(df):

        next_id = int(df["id"].max()) + 1

    new_series = {}

    # Fill every column in dataset
    for column in df.columns:

        new_series[column] = ""

    # Auto ID
    new_series["id"] = next_id

    # Copy submitted values
    for key, value in data.items():

        new_series[key] = value

        # -------- Defaults --------

    # Make sure every new series passes the loader filters
    new_series["vote_count"] = 100

    if not new_series.get("vote_average"):
        new_series["vote_average"] = 7.5

    if not new_series.get("popularity"):
        new_series["popularity"] = 100

    new_series.setdefault("adult", False)

    new_series.setdefault("backdrop_path", "")

    new_series.setdefault("homepage", "")

    new_series.setdefault("in_production", False)

    new_series.setdefault("original_name", new_series["name"])

    new_series.setdefault("type", "Scripted")

    new_series.setdefault("tagline", "")

    new_series.setdefault(
        "languages",
        new_series["original_language"]
    )

    new_series.setdefault("networks", "Netflix")

    new_series.setdefault("origin_country", "US")

    new_series.setdefault(
        "spoken_languages",
        "English"
    )

    new_series.setdefault(
        "production_companies",
        ""
    )

    new_series.setdefault(
        "production_countries",
        "United States of America"
    )

    new_series.setdefault(
        "episode_run_time",
        45
    )

    df = pd.concat(

        [

            df,

            pd.DataFrame([new_series])

        ],

        ignore_index=True

    )

    df.to_csv(

        SERIES_DATASET,

        index=False

    )

    reload_series()


def update_series(series_id, data):

    global _series

    df = load_series().copy()

    index = df[df["id"] == int(series_id)].index

    if len(index) == 0:
        return

    i = index[0]

    for k, v in data.items():

        if k not in df.columns:
            continue

        dtype = df[k].dtype

        try:
            if str(dtype).startswith("float"):
                v = float(v) if v not in ("", None) else 0.0
            elif str(dtype).startswith("int"):
                v = int(float(v)) if v not in ("", None) else 0
        except (ValueError, TypeError):
            pass

        df.at[i, k] = v

    df.to_csv(
        SERIES_DATASET,
        index=False
    )

    reload_series()


def delete_series(series_id):

    global _series

    df = load_series().copy()

    df = df[df["id"] != int(series_id)]

    df.to_csv(

        SERIES_DATASET,

        index=False

    )

    reload_series()