from sentence_transformers import SentenceTransformer

print("Loading AI model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("AI model loaded successfully!")


def create_embeddings(texts):
    """
    Generate embeddings for a list of text strings.
    """
    return model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )