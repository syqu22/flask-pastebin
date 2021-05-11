from flask import render_template, request, flash, redirect, url_for
from web.models import User
from web import db
from flask_login import login_user, login_required, logout_user, current_user
from web.auth import bp

#Login view
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", category="error")
        return redirect(url_for("pastebins.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            #If user with given username exists and passwords are correct Log him In
            if user.check_password(password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("pastebins.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("User with this name does not exist.", category="error")
        return render_template("auth/login.html", user=current_user, username=username)
    
    return render_template("auth/login.html", user=current_user)

#Sign up view
@bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash("User already exists.", category="error")
        else:
            new_user = User(username, email, password1)
            if new_user.is_valid(password1, password2):
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("Account successfully created!", category="success")
                return redirect(url_for("pastebins.home"))
            
            return render_template("auth/sign_up.html", user=current_user, username=username, email=email)

    return render_template("auth/sign_up.html", user=current_user)

#Log out view
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
