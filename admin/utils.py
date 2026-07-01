import os
import psycopg2

from functools import wraps
from flask import session, redirect


def get_db_connection():

    return psycopg2.connect(

        host=os.getenv("DB_HOST"),

        database=os.getenv("DB_NAME"),

        user=os.getenv("DB_USER"),

        password=os.getenv("DB_PASSWORD"),

        port=os.getenv("DB_PORT")

    )


def admin_required(f):

    @wraps(f)

    def wrapper(*args, **kwargs):

        if "admin" not in session:

            return redirect("/admin/login")

        return f(*args, **kwargs)

    return wrapper