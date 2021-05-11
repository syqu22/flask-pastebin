from flask import Blueprint

bp = Blueprint("users", __name__)

from web.user import routes
