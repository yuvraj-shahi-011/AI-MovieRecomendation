from recommendation_engine.vector_store import load_vector_store

movies, _ = load_vector_store()

for i in range(10):
    print("=" * 60)
    print("Title:", movies.iloc[i]["title"])
    print("Poster:", movies.iloc[i]["poster_path"])
    print("IMDb:", movies.iloc[i]["imdb_id"])