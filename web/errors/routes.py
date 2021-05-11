from flask import render_template
from flask_login import current_user
from web.errors import bp

@bp.app_errorhandler(400)
def page_not_found_error(e):
    return render_template("errors/400.html", user=current_user), 400

@bp.app_errorhandler(401)
def page_not_found_error(e):
    return render_template("errors/401.html", user=current_user), 401

@bp.app_errorhandler(403)
def page_not_found_error(e):
    return render_template("errors/403.html", user=current_user), 403

@bp.app_errorhandler(404)
def page_not_found_error(e):
    return render_template("errors/404.html", user=current_user), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html", user=current_user), 500
