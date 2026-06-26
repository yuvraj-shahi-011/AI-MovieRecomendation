import faiss

_index = None


def load_index():
    global _index

    if _index is None:
        print("Loading FAISS index...")

        _index = faiss.read_index(
            "models/movie_index.faiss"
        )

        print("FAISS index loaded!")

    return _index