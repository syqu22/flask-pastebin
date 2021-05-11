from flask import Blueprint

bp = Blueprint("errors", __name__)

from web.errors import routes
