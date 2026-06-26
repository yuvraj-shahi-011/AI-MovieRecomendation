import faiss
import numpy as np
import os

print("Loading embeddings...")

embeddings = np.load("models/embeddings.npy")

print("Embeddings:", embeddings.shape)

# FAISS requires float32
embeddings = embeddings.astype("float32")

# Normalize vectors for cosine similarity
faiss.normalize_L2(embeddings)

print("Building FAISS index...")

index = faiss.IndexFlatIP(embeddings.shape[1])

index.add(embeddings)

os.makedirs("models", exist_ok=True)

faiss.write_index(
    index,
    "models/movie_index.faiss"
)

print("FAISS index created successfully!")

print("Total vectors:", index.ntotal)