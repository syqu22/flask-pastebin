from flask import Blueprint

bp = Blueprint("pastebins", __name__)

from web.pastebin import routes
