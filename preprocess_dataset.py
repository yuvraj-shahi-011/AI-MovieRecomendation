import pandas as pd

print("Loading dataset...")

df = pd.read_csv(
    "dataset/TMDB_all_movies.csv",
    low_memory=False
)

print("Original Shape:", df.shape)

# Keep only the columns needed for recommendations
columns = [
    "id",
    "title",
    "overview",
    "genres",
    "cast",
    "director",
    "poster_path",
    "release_date",
    "vote_average",
    "popularity",
    "original_language"
]

df = df[columns]

print("Selected Columns:", df.shape)

# Remove rows without a title
df = df.dropna(subset=["title"])

# Fill missing values
df["overview"] = df["overview"].fillna("")
df["genres"] = df["genres"].fillna("")
df["cast"] = df["cast"].fillna("")
df["director"] = df["director"].fillna("")
df["poster_path"] = df["poster_path"].fillna("")
df["release_date"] = df["release_date"].fillna("Unknown")
df["original_language"] = df["original_language"].fillna("Unknown")

print("Cleaned Shape:", df.shape)

df.to_csv(
    "dataset/processed_movies.csv",
    index=False
)

print("processed_movies.csv created successfully!")