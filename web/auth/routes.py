from flask import render_template, request, flash, redirect, url_for
from web.models import User
from web import db
from flask_login import login_user, login_required, logout_user, current_user
from web.auth import bp
from web.auth.forms import LoginForm, SignupForm

#Login view
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", category="error")
        return redirect(url_for("pastebins.home"))

    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash("Logged in successfully!", category="success")
            return redirect(url_for("pastebins.home"))

    return render_template("auth/login.html", user=current_user, form=form)

#Sign up view
@bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = SignupForm()

    if request.method == "POST" and form.validate_on_submit():
        new_user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash("Account successfully created!", category="success")
        return redirect(url_for("pastebins.home"))
            
    return render_template("auth/sign_up.html", user=current_user, form=form)

#Log out view
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
