import os

from flask import (
    render_template,
    request,
    redirect,
    flash
)

from werkzeug.utils import secure_filename
from recommendation_engine.loader_series import load_series
from . import admin_bp
from admin.utils import admin_required

from admin.series_service import (
    get_series,
    get_series_by_id,
    add_series,
    update_series,
    delete_series
)


# ==========================================
# SERIES HOME
# ==========================================

@admin_bp.route("/series")
@admin_required
def series():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    )

    series_list, total_pages, total_series = get_series(
        page,
        search
    )

    return render_template(

        "admin/series.html",

        series=series_list,

        page=page,

        total_pages=total_pages,

        total_series=total_series,

        search=search

    )


# ==========================================
# ADD SERIES
# ==========================================

@admin_bp.route("/series/add", methods=["GET", "POST"])
@admin_required
def add_series_page():

    if request.method == "POST":

        poster = request.files.get("poster")

        poster_filename = ""

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

        data = {

            "name": request.form["name"],

            "overview": request.form["overview"],

            "genres": request.form["genres"],

            "created_by": request.form["created_by"],

                "poster_path": poster_filename,

            "first_air_date": request.form["first_air_date"],

            "last_air_date": request.form["last_air_date"],

            "vote_average": float(

                request.form.get("vote_average") or 7.5

            ),

            "vote_count": 100,

            "popularity": float(

                request.form.get("popularity") or 100

            ) if "trending" not in request.form else 999999,

            "original_language": request.form["original_language"],

            "number_of_seasons": int(

                request.form.get("number_of_seasons") or 1

            ),

            "number_of_episodes": int(

                request.form.get("number_of_episodes") or 1

            ),

            "status": request.form["status"],
            "featured": "featured" in request.form,
            "trending": "trending" in request.form

        }

        add_series(data)

        load_series(force_reload=True)

        flash(

            "Series Added Successfully!",

            "success"

        )

        return redirect("/admin/series")

    return render_template(

        "admin/add_series.html",

        edit=False

    )


# ==========================================
# EDIT SERIES
# ==========================================

@admin_bp.route("/series/edit/<int:series_id>", methods=["GET", "POST"])
@admin_required
def edit_series(series_id):

    tv = get_series_by_id(series_id)

    if tv is None:

        flash("Series Not Found", "danger")

        return redirect("/admin/series")

    if request.method == "POST":

        # ---------------- Poster Upload ----------------

        poster = request.files["poster"]

        poster_filename = tv["poster_path"]

        if poster and poster.filename != "":

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

        # ---------------- Update Data ----------------

        updated = {

            "name": request.form["name"],

            "overview": request.form["overview"],

            "genres": request.form["genres"],

            "created_by": request.form["created_by"],

            "poster_path": poster_filename,

            "first_air_date": request.form["first_air_date"],

            "last_air_date": request.form["last_air_date"],

            "vote_average": request.form["vote_average"],

            "popularity": 999999 if "trending" in request.form else float(request.form.get("popularity") or 100),

            "original_language": request.form["original_language"],

            "number_of_seasons": request.form["number_of_seasons"],

            "number_of_episodes": request.form["number_of_episodes"],

            "status": request.form["status"]

        }

        update_series(
            series_id,
            updated
        )

        load_series(force_reload=True)

        flash(

            "Series Updated Successfully!",

            "success"

        )

        return redirect("/admin/series")

    return render_template(

        "admin/add_series.html",

        tv=tv,

        edit=True

    )

# ==========================================
# DELETE SERIES
# ==========================================

@admin_bp.route("/series/delete/<int:series_id>", methods=["GET", "POST"])
@admin_required
def delete_series_page(series_id):

    tv = get_series_by_id(series_id)

    if tv is None:

        flash(

            "Series Not Found",

            "danger"

        )

        return redirect("/admin/series")

    if request.method == "POST":

        delete_series(series_id)
        load_series(force_reload=True)

        flash(

            "Series Deleted Successfully",

            "success"

        )

        return redirect("/admin/series")

    return render_template(

        "admin/delete_series.html",

        tv=tv

    )