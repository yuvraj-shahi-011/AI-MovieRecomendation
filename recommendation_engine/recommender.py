import faiss

_movies = None
_index = None
_model = None


def load_everything():

    global _movies
    global _index
    global _model

    if _movies is None:

        print("Loading AI dataset...")

        from recommendation_engine.vector_store import load_vector_store

        _movies, _ = load_vector_store()

    if _index is None:

        print("Loading FAISS index...")

        from recommendation_engine.faiss_store import load_index

        _index = load_index()

    if _model is None:

        print("Loading SentenceTransformer...")

        from recommendation_engine.embeddings import model

        _model = model

    return _movies, _index, _model


def recommend_movies(imdb_id, top_k=100):

    movies, index, model = load_everything()

    movie = movies[
        movies["imdb_id"] == imdb_id
    ]

    if movie.empty:
        return None

    movie = movie.iloc[0]

    query_embedding = model.encode(
        [movie["features"]],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(
        query_embedding,
        top_k + 1
    )

    recommendations = movies.iloc[
        indices[0]
    ].copy()

    recommendations = recommendations[
        recommendations["imdb_id"] != imdb_id
    ]

    return recommendations.head(top_k)