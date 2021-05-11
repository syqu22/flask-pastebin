from flask import Blueprint

bp = Blueprint("search", __name__)

from web.search import routes
