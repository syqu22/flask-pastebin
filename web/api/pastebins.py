from flask import jsonify, request
from web.models import Pastebin
from web.api import bp

@bp.route("/pastebins/<int:id>", methods=["GET"])
def get_pastebin(id):
    """
    Returns pastebin with given id
    """
    return jsonify(Pastebin.query.get_or_404(id).to_dict())
    
@bp.route("/pastebins", methods=["GET"])
def get_pastebins():
    """
    Returns 50 pastebins per page
    @param page
    """
    page = request.args.get("page")
    if not page:
        start = 0
        limit = 50
    else:
        start = 50 * int(page)
        limit = 50 + 50 * int(page)

    return jsonify([pastebin.to_dict() for pastebin in Pastebin.query.all()[start:limit]])
