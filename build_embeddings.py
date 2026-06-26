import os
import pickle
import numpy as np

from recommendation_engine.loader import load_movies
from recommendation_engine.embeddings import create_embeddings

print("Loading AI dataset...")

movies = load_movies()

print(f"Movies: {len(movies)}")

print("Generating embeddings...")

embeddings = create_embeddings(
    movies["features"].tolist()
)

os.makedirs("models", exist_ok=True)

print("Saving embeddings...")

np.save(
    "models/embeddings.npy",
    embeddings
)

print("Saving movie dataset...")

with open("models/ai_movies.pkl", "wb") as f:
    pickle.dump(movies, f)

print("Done!")

print("Embedding Shape:", embeddings.shape)