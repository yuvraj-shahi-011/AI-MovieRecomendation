from flask import Flask, render_template
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

    response = requests.get(url)
    data = response.json()
    movies = data["results"]

    return render_template("index.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=True)