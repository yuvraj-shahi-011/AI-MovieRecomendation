import faiss
import numpy as np
import os

print("Loading TV Series embeddings...")

embeddings = np.load("models/series_embeddings.npy")

print("Embeddings:", embeddings.shape)

embeddings = embeddings.astype("float32")

faiss.normalize_L2(embeddings)

print("Building TV Series FAISS index...")

index = faiss.IndexFlatIP(
    embeddings.shape[1]
)

index.add(embeddings)

os.makedirs("models", exist_ok=True)

faiss.write_index(
    index,
    "models/series_index.faiss"
)

print("TV Series FAISS index created successfully!")

print("Total vectors:", index.ntotal)