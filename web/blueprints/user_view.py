from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from flask_login.utils import login_required,login_user, current_user
from web.models.user import User

from web import db

user_view = Blueprint("user_view", __name__)

@user_view.route("/user")
@login_required
def user():
   return render_template("user.html", user=current_user)

@user_view.route("/user/edit", methods=["GET", "POST"])
@login_required
def edit_user():
   if request.method == "POST":
      username = request.form.get("username")
      email = request.form.get("email")
      new_password = request.form.get("new_password")
      password1 = request.form.get("password1")
      password2 = request.form.get("password2")
      user = current_user
      new_user = User(username, email, new_password)

      if new_user.is_valid(password1, password2):
         user.username = new_user.username
         user.email = new_user.email
         user.password = new_user.password
         db.session.commit()

         login_user(user, remember=True)
         return redirect(url_for("user_view.user"))
      return render_template("user_edit.html", user=current_user, username=username, email=email)

   return render_template("user_edit.html", user=current_user)
