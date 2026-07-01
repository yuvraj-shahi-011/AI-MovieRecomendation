import subprocess

from flask import (
    render_template,
    redirect,
    flash
)

from . import admin_bp
from admin.utils import admin_required

from admin.movie_service import reload_movies
from admin.series_service import reload_series

@admin_bp.route("/system")
@admin_required
def system():

    return render_template("admin/system.html")


@admin_bp.route("/system/reload-movies")
@admin_required
def reload_movie_dataset():

    reload_movies()
    
    flash(

        "Movie dataset reloaded successfully.",

        "success"

    )

    return redirect("/admin/system")


@admin_bp.route("/system/build-embeddings")
@admin_required
def build_embeddings():

    subprocess.run(

        ["python",
         "recommendation_engine/build_embeddings.py"]

    )

    flash(

        "Embeddings generated successfully.",

        "success"

    )

    return redirect("/admin/system")


@admin_bp.route("/system/build-faiss")
@admin_required
def build_faiss():

    subprocess.run(

        ["python",
         "recommendation_engine/build_faiss.py"]

    )

    flash(

        "FAISS index rebuilt successfully.",

        "success"

    )

    return redirect("/admin/system")


@admin_bp.route("/system/rebuild-all")
@admin_required
def rebuild_all():

    reload_movies()

    reload_series()

    subprocess.run(
        [
            "python",
            "recommendation_engine/build_embeddings.py"
        ]
    )

    subprocess.run(
        [
            "python",
            "recommendation_engine/build_faiss.py"
        ]
    )

    flash(
        "Everything rebuilt successfully.",
        "success"
    )

    return redirect("/admin/system")