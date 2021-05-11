from flask import render_template
from flask_login.utils import current_user
from web.models import Pastebin
from web.search import bp

@bp.route("/search/<text>")
def search(text: str):
    #TODO
    pastebins = Pastebin.query.filter(Pastebin.paste_type.like("%" + text + "%"))
    #filter(Pastebin.title.like("%" + text + "%"))

    return render_template("search.html", user=current_user, pastebins=pastebins)
