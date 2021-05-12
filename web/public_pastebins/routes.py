from sqlalchemy import desc
from flask import render_template, request
from flask_login.utils import current_user
from web.models import Pastebin
from web.public_pastebins import bp

@bp.route("/public")
def public():
    page = request.args.get("page", 1, type=int)
    tags = dict()

    #Get last 50 pastebins
    pastebins = Pastebin.query.order_by(desc(Pastebin.date)).filter_by(password=None).limit(50).from_self()

    for pastebin in pastebins:
        pastebin.is_expired()  
        if pastebin.syntax in tags:
            tags[pastebin.syntax] += 1
        else:
            tags[pastebin.syntax] = 1

    tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)

    return render_template("public_pastebins.html", user=current_user, pastebins=pastebins.paginate(page, 15, False), tags=tags)
