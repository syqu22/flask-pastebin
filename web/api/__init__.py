from flask import Blueprint

bp = Blueprint("api", __name__)

from web.api import users, pastebins
