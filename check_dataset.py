from recommendation_engine.vector_store import load_vector_store

movies, embeddings = load_vector_store()

print(movies.columns.tolist())
print(movies.head())
