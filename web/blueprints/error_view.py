from flask import render_template, Blueprint
from flask_login import current_user

error_view = Blueprint("error_view", __name__)

@error_view.app_errorhandler(400)
def page_not_found_error(e):
    return render_template("errors/404.html", user=current_user), 400

@error_view.app_errorhandler(401)
def page_not_found_error(e):
    return render_template("errors/404.html", user=current_user), 401

@error_view.app_errorhandler(403)
def page_not_found_error(e):
    return render_template("errors/404.html", user=current_user), 403

@error_view.app_errorhandler(404)
def page_not_found_error(e):
    return render_template("errors/404.html", user=current_user), 404

@error_view.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html", user=current_user), 500
