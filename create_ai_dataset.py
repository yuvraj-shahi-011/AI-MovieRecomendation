import pandas as pd

print("Loading processed dataset...")

movies = pd.read_csv(
    "dataset/processed_movies.csv",
    low_memory=False
)

print("Original:", movies.shape)

# Remove movies with missing overview
movies = movies[
    movies["overview"].notna()
]

# Remove movies with missing genres
movies = movies[
    movies["genres"].notna()
]

# Remove movies with missing director
movies = movies[
    movies["director"].notna()
]

# Keep only movies with some popularity
movies = movies[
    movies["popularity"] >= 1
]

print("Filtered:", movies.shape)
# Remove duplicate IMDb IDs
movies = movies.drop_duplicates(
    subset="imdb_id",
    keep="first"
)

# Remove duplicate titles
movies = movies.drop_duplicates(
    subset="title",
    keep="first"
)

print("After removing duplicates:", movies.shape)

movies.to_csv(
    "dataset/ai_movies.csv",
    index=False
)

print("ai_movies.csv created successfully!")