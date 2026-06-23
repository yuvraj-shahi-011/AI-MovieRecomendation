from flask import Flask, render_template
import requests

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"

@app.route("/")
def home():

    trending_url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
    popular_url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
    top_url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}"
    upcoming_url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}"

    trending = requests.get(trending_url).json()["results"]
    popular = requests.get(popular_url).json()["results"]
    top_rated = requests.get(top_url).json()["results"]
    upcoming = requests.get(upcoming_url).json()["results"]

    return render_template(
        "index.html",
        trending=trending,
        popular=popular,
        top_rated=top_rated,
        upcoming=upcoming
    )

if __name__ == "__main__":
    app.run(debug=True)