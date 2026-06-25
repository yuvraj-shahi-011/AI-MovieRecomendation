from recommendation_engine.loader import load_movies

movies = load_movies()


def filter_candidates(movie_title):
    """
    Filter movies that are similar based on language and genre.
    """

    # Find the searched movie
    movie = movies[
        movies["title"].str.lower() == movie_title.lower()
    ]

    if movie.empty:
        return None

    movie = movie.iloc[0]

    language = movie["original_language"]
    genre = movie["genres"]

    # Filter by language
    candidates = movies[
        movies["original_language"] == language
    ]

    # Filter by genre (only if genre exists)
    if genre:
        candidates = candidates[
            candidates["genres"].str.contains(
                genre,
                case=False,
                na=False
            )
        ]

    return candidates