import faiss

from recommendation_engine.embeddings import model
from recommendation_engine.vector_store import load_vector_store
from recommendation_engine.faiss_store import load_index

movies, embeddings = load_vector_store()
index = load_index()


def recommend_movies(imdb_id, top_k=10):

    movie = movies[
        movies["imdb_id"] == imdb_id
    ]

    if movie.empty:
        print(f"{imdb_id} not found in AI dataset")
        return None

    print(f"{imdb_id} found in AI dataset")

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