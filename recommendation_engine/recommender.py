from sentence_transformers import util

from recommendation_engine.loader import load_movies
from recommendation_engine.embeddings import create_embeddings
from recommendation_engine.candidate_filter import filter_candidates


movies = load_movies()


def recommend_movies(movie_title, top_k=10):
    """
    Recommend movies similar to the given movie.
    """

    candidates = filter_candidates(movie_title)

    if candidates is None or candidates.empty:
        return None

    # Find the searched movie
    selected = candidates[
        candidates["title"].str.lower() == movie_title.lower()
    ]

    if selected.empty:
        return None

    # Create embeddings
    texts = candidates["features"].fillna("").tolist()

    embeddings = create_embeddings(texts)

    query_embedding = create_embeddings(
        [selected.iloc[0]["features"]]
    )

    scores = util.cos_sim(
        query_embedding,
        embeddings
    )[0]

    candidates = candidates.copy()

    candidates["score"] = scores.numpy()

    candidates = candidates.sort_values(
        by="score",
        ascending=False
    )

    return candidates.head(top_k + 1)