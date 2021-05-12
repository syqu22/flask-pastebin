from flask import jsonify, request
from web.models import User
from web.api import bp

@bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    """
    Returns user with given id
    """
    return jsonify(User.query.get_or_404(id).to_dict())
    
@bp.route("/users", methods=["GET"])
def get_users():
    """
    Returns 50 users per page
    @param page
    """
    page = request.args.get("page")
    if not page:
        start = 0
        limit = 50
    else:
        start = 50 * int(page)
        limit = 50 + 50 * int(page)

    return jsonify([user.to_dict() for user in User.query.all()[start:limit]])

@bp.route("/users/<int:id>/pastebins", methods=["GET"])
def get_user_pastebins(id):
    """
    Returns all pastebins of user with given id
    """
    user = User.query.get_or_404(id)

    return jsonify([pastebin.to_dict() for pastebin in user.pastebins])
