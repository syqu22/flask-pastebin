from flask import render_template, request, url_for
from flask_login.utils import current_user
from web.models import Pastebin
from web.public_pastebins import bp

@bp.route("/public")
def public():
    page = request.args.get("page", 1, type=int)
    pastebins = Pastebin.query.filter_by(password=None).paginate(page, 15, False)
    
    return render_template("public_pastebins.html", user=current_user, pastebins=pastebins)
