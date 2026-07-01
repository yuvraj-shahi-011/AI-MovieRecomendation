import pandas as pd

DATASET = "dataset/ai_movies.csv"

df = pd.read_csv(DATASET)

new_columns = {
    "backdrop_path": "",
    "runtime": "",
    "status": "Released",
    "trailer_url": "",
    "featured": False,
    "trending": False,
    "created_at": ""
}

for col, default in new_columns.items():

    if col not in df.columns:

        df[col] = default

df.to_csv(DATASET, index=False)

print("✅ Dataset Updated Successfully!")
print(df.columns.tolist())