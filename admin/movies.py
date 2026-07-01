from flask import (
    render_template,
    request,
    redirect,
    flash
)

import os
from werkzeug.utils import secure_filename

from . import admin_bp
from admin.utils import admin_required

from recommendation_engine.vector_store import reload_vector_store

from admin.movie_service import (
    get_movies,
    get_all_genres,
    get_all_languages,
    add_movie,
    get_movie,
    update_movie,
    delete_movie
)

from werkzeug.utils import secure_filename

from flask import (
    render_template,
    request,
    redirect,
    flash
)

from . import admin_bp
from admin.utils import admin_required

from admin.movie_service import (
    get_movies,
    get_all_genres,
    get_all_languages,
    add_movie
)

@admin_bp.route("/movies")
@admin_required
def movies():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    )

    genre = request.args.get(
        "genre",
        ""
    )

    language = request.args.get(
        "language",
        ""
    )

    sort = request.args.get(
        "sort",
        "rating"
    )

    movies, total_pages, total_movies = get_movies(

        page,

        search,

        genre,

        language,

        sort

    )

    return render_template(

        "admin/movies.html",

        movies=movies,

        page=page,

        total_pages=total_pages,

        total_movies=total_movies,

        search=search,

        genre=genre,

        language=language,

        sort=sort,

        genres=get_all_genres(),

        languages=get_all_languages()

    )
# ==========================================
# ADD MOVIE
# ==========================================

@admin_bp.route("/movie/add", methods=["GET", "POST"])
@admin_required
def add_movie_page():

    if request.method == "POST":

        poster = request.files.get("poster")
        backdrop = request.files.get("backdrop")

        poster_filename = ""
        backdrop_filename = ""

        # -----------------------------
        # Poster Upload
        # -----------------------------

        if poster and poster.filename:

            os.makedirs(
                "static/uploads/posters",
                exist_ok=True
            )

            poster_filename = secure_filename(
                poster.filename
            )

            poster.save(
                os.path.join(
                    "static",
                    "uploads",
                    "posters",
                    poster_filename
                )
            )

        # -----------------------------
        # Backdrop Upload
        # -----------------------------

        if backdrop and backdrop.filename != "":

            backdrop_filename = secure_filename(

                backdrop.filename

            )

            backdrop.save(

                os.path.join(

                    "static",

                    "uploads",

                    "backdrops",

                    backdrop_filename

                )

            )

        movie = {

            "imdb_id": request.form["imdb_id"],

            "title": request.form["title"],

            "overview": request.form["overview"],

            "genres": ",".join(request.form.getlist("genres")),

            "cast": request.form["cast"],

            "director": request.form["director"],

            "poster_path": poster_filename,

            "backdrop_path": backdrop_filename,

            "release_date": request.form["release_date"],

            "vote_average": float(
    request.form.get("vote_average") or 7.5
),

"vote_count": 100,

"popularity": float(
    request.form.get("popularity") or 100
),

"original_language": request.form["original_language"],

"runtime": request.form.get("runtime") or 120,

"status": request.form["status"],

"adult": False,

            "trailer_url": request.form["trailer_url"],

            "featured":

                "featured" in request.form,

            "trending":

                "trending" in request.form

        }

        add_movie(movie)
        reload_vector_store()

        flash(

            "Movie Added Successfully!",

            "success"

        )

        return redirect(

            "/admin/movies"

        )

    return render_template(

        "admin/add_movie.html"

    )
@admin_bp.route("/movie/edit/<imdb_id>", methods=["GET", "POST"])
@admin_required
def edit_movie(imdb_id):

    movie = get_movie(imdb_id)

    if movie is None:

        flash("Movie not found", "danger")

        return redirect("/admin/movies")

    if request.method == "POST":

        updated = {

            "title": request.form["title"],

            "overview": request.form["overview"],

            "genres": ",".join(request.form.getlist("genres")),

            "cast": request.form["cast"],

            "director": request.form["director"],

            "release_date": request.form["release_date"],

            "vote_average": float(
    request.form.get("vote_average") or 7.5
),

"vote_count": 100,

"popularity": float(
    request.form.get("popularity") or 100
),

"original_language": request.form["original_language"],

"runtime": request.form.get("runtime") or 120,

"status": request.form["status"],

"adult": False,

        }

        update_movie(imdb_id, updated)
        reload_vector_store()
        flash("Movie Updated Successfully!", "success")

        return redirect("/admin/movies")

    return render_template(

    "admin/add_movie.html",

    genres=get_all_genres(),

    edit=False

)
@admin_bp.route("/movie/delete/<imdb_id>", methods=["GET","POST"])
@admin_required
def delete_movie_page(imdb_id):

    movie = get_movie(imdb_id)

    if movie is None:

        flash(

            "Movie Not Found",

            "danger"

        )

        return redirect("/admin/movies")

    if request.method == "POST":

        delete_movie(imdb_id)
        reload_vector_store()

        flash(

            "Movie Deleted Successfully",

            "success"

        )

        return redirect("/admin/movies")

    return render_template(

        "admin/delete_movie.html",

        movie=movie

    )