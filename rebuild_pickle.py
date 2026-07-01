import pandas as pd
import pickle

print("Loading ai_movies.csv...")

movies = pd.read_csv(
    "dataset/ai_movies.csv",
    low_memory=False
)

print("Movies:", movies.shape)

with open("models/ai_movies.pkl", "wb") as f:
    pickle.dump(movies, f, protocol=4)

print("New ai_movies.pkl created successfully!")