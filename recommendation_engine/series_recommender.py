import faiss

_series = None
_index = None
_model = None


def load_everything():

    global _series
    global _index
    global _model

    if _series is None:

        print("Loading TV Series dataset...")

        from recommendation_engine.series_vector_store import (
            load_series_vector_store
        )

        _series, _ = load_series_vector_store()

    if _index is None:

        print("Loading TV Series FAISS index...")

        from recommendation_engine.series_faiss_store import load_series_index

        _index = load_series_index()

    if _model is None:

        print("Loading SentenceTransformer...")

        from recommendation_engine.embeddings import model

        _model = model

    return _series, _index, _model


def recommend_series(series_id, top_k=100):

    series, index, model = load_everything()

    selected = series[
        series["series_id"] == series_id
    ]

    if selected.empty:
        return None

    selected = selected.iloc[0]

    query_embedding = model.encode(
        [selected["features"]],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(
        query_embedding,
        top_k + 1
    )

    recommendations = series.iloc[
        indices[0]
    ].copy()

    recommendations = recommendations[
        recommendations["series_id"] != series_id
    ]

    return recommendations.head(top_k)