from flask import render_template, request, redirect, url_for
from flask_login import current_user
from flask_login.utils import login_required,login_user, current_user
from web.models import User
from web.user import bp
from web.user.forms import EditUserForm
from web import db

@bp.route("/user")
@login_required
def user():
   return render_template("user/user.html", user=current_user)

@bp.route("/user/edit", methods=["GET", "POST"])
@login_required
def edit_user():
   form = EditUserForm()

   if request.method == "POST" and form.validate_on_submit():
      user = User.query.filter_by(username=current_user.username).first()

      if user.check_password(form.password.data):
         user.username = form.username.data
         user.email = form.email.data
         user.set_password(form.password.data)
         db.session.commit()

         login_user(user, remember=True)
         return redirect(url_for("users.user"))

   return render_template("user/user_edit.html", user=current_user, form=form)
