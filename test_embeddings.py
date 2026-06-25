from recommendation_engine.embeddings import create_embeddings

movies = [
    "Inception is a science fiction thriller.",
    "Interstellar is a space exploration movie.",
    "3 Idiots is a comedy drama."
]

vectors = create_embeddings(movies)

print("Embedding Shape:", vectors.shape)
print(vectors)