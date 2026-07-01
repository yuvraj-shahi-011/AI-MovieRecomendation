from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash

from . import admin_bp
from admin.utils import get_db_connection
from admin.utils import admin_required


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(

            """
            SELECT username
            FROM admins
            WHERE username=%s
            AND password=%s
            """,

            (username, password)

        )

        admin = cursor.fetchone()

        cursor.close()

        conn.close()

        if admin:

            session["admin"] = admin[0]

            flash("Welcome Admin", "success")

            return redirect("/admin/dashboard")

        flash("Invalid Username or Password", "danger")

    return render_template("admin/login.html")


@admin_bp.route("/dashboard")
@admin_required
def dashboard():

    return render_template(
    "admin/dashboard.html",
    user=session.get("user")
)


@admin_bp.route("/logout")
@admin_required
def logout():

    session.pop("admin", None)

    flash("Logged out successfully", "success")

    return render_template(
    "admin/login.html",
    user=session.get("user")
)