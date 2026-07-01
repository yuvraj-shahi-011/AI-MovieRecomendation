import numpy as np

from recommendation_engine.loader import load_movies

_movies = None
_embeddings = None


def load_vector_store():

    global _movies
    global _embeddings

    if _movies is None:

        _movies = load_movies()

    if _embeddings is None:

        print("Loading embeddings...")

        _embeddings = np.load(

            "models/embeddings.npy"

        )

        print(

            f"Embeddings loaded: {_embeddings.shape}"

        )

    return _movies, _embeddings


def reload_vector_store():

    global _movies

    _movies = load_movies(force_reload=True)

    return _movies