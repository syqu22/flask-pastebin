from flask import Blueprint

bp = Blueprint("public_pastebins", __name__)

from web.public_pastebins import routes
