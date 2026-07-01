from flask import Blueprint

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

# Import routes AFTER blueprint creation
import admin.auth
import admin.movies
import admin.series
import admin.system