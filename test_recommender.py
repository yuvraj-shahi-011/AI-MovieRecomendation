from recommendation_engine.recommender import recommend_movies
import time

imdb_id = input("IMDb ID: ")

start = time.time()

results = recommend_movies(imdb_id)

end = time.time()

print(f"\nTime Taken: {end-start:.2f} seconds\n")

if results is None:
    print("Movie not found")
else:
    print(results[
        [
            "title",
            "imdb_id",
            "vote_average",
            "release_date"
        ]
    ])