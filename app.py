from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# Secret Key for Session
app.secret_key = "moviehub_secret_key"


# HOME PAGE
@app.route("/")
def home():

    popular = [
        {
            "title": "The Dark Knight",
            "vote_average": 9.0,
            "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
        },
        {
            "title": "Avengers: Endgame",
            "vote_average": 8.8,
            "poster_path": "/or06FN3Dka5tukK1e9sl16pB3iy.jpg"
        },
        {
            "title": "Joker",
            "vote_average": 8.4,
            "poster_path": "/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg"
        },
        {
            "title": "Batman Begins",
            "vote_average": 8.2,
            "poster_path": "/4MpN4kIEqUjW8OPtOQJXlTdHiJV.jpg"
        }
    ]

    return render_template(
        "index.html",
        popular=popular,
        user=session.get("user")
    )


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """,
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user"] = user[1]

            return redirect("/")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)