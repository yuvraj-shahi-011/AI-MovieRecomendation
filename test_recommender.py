from recommendation_engine.recommender import recommend_movies

movie = input("Movie: ")

results = recommend_movies(movie)

if results is None:
    print("Movie not found")
else:
    print(
        results[
            ["title", "vote_average", "score"]
        ]
    )