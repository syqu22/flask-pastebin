from flask import Blueprint, render_template
from flask_login import current_user
from flask_login.utils import login_required

user_view = Blueprint("user_view", __name__)

#View user personal pastebins
@user_view.route("/user")
@login_required
def user():
   return render_template("user.html", user=current_user)
