import os
import pickle
import numpy as np

from recommendation_engine.loader_series import load_series
from recommendation_engine.embeddings import create_embeddings

print("Loading TV Series dataset...")

series = load_series()

print(f"TV Series: {len(series)}")

print("Generating embeddings...")

embeddings = create_embeddings(
    series["features"].tolist()
)

os.makedirs("models", exist_ok=True)

print("Saving embeddings...")

np.save(
    "models/series_embeddings.npy",
    embeddings
)

print("Saving TV Series dataset...")

with open("models/web_series.pkl", "wb") as f:
    pickle.dump(series, f)

print("Done!")

print("Embedding Shape:", embeddings.shape)