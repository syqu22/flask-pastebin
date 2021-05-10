from flask import Blueprint, render_template
from flask_login.utils import current_user
from web.models.pastebin import Pastebin


search_view = Blueprint("search_view", __name__)

@search_view.route("/search/<text>")
def search(text: str):
    #TODO
    pastebins = Pastebin.query.filter(Pastebin.paste_type.like("%" + text + "%"))
    #filter(Pastebin.title.like("%" + text + "%"))

    return render_template("search.html", user=current_user, pastebins=pastebins)
