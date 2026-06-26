import pickle
import numpy as np

_movies = None
_embeddings = None


def load_vector_store():
    global _movies, _embeddings

    if _movies is None:
        print("Loading AI dataset...")

        with open("models/ai_movies.pkl", "rb") as f:
            _movies = pickle.load(f)

        print(f"Movies loaded: {len(_movies)}")

    if _embeddings is None:
        print("Loading embeddings...")

        _embeddings = np.load("models/embeddings.npy")

        print(f"Embeddings loaded: {_embeddings.shape}")

    return _movies, _embeddings