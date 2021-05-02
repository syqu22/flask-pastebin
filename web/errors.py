from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user

errors = Blueprint("errors", __name__)

@errors.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404