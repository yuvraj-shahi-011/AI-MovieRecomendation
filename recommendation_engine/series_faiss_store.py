import faiss

_index = None


def load_series_index():

    global _index

    if _index is None:

        print("Loading TV Series FAISS index...")

        _index = faiss.read_index(
            "models/series_index.faiss"
        )

        print("TV Series FAISS index loaded!")

    return _index