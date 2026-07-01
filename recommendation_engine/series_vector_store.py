import numpy as np

from recommendation_engine.loader_series import load_series

_series = None
_embeddings = None


def load_series_vector_store():

    global _series
    global _embeddings

    if _series is None:

        _series = load_series()

    if _embeddings is None:

        print("Loading TV Series embeddings...")

        _embeddings = np.load(

            "models/series_embeddings.npy"

        )

        print(

            f"TV Series embeddings loaded: {_embeddings.shape}"

        )

    return _series, _embeddings


def reload_series_vector_store():

    global _series
    global _embeddings

    _series = load_series(

        force_reload=True

    )

    _embeddings = np.load(

        "models/series_embeddings.npy"

    )

    return _series, _embeddings