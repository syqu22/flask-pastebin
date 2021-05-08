from flask import Blueprint, render_template, request, flash, redirect, url_for
from web.models.user import User
from web import db
from flask_login import login_user, login_required, logout_user, current_user

auth_view = Blueprint("auth_view", __name__)

#Login view
@auth_view.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            #If user with given username exists and passwords are correct Log him In
            if user.check_password(password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("pastebin_view.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Username doesn't exist.", category="error")
    
    return render_template("login.html", user=current_user)

#Sign up view
@auth_view.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #If user is valid add it to database
        if is_user_valid(username, email, password1, password2):
            new_user = User(username, email, password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account successfully created!", category="success")

            return redirect(url_for("pastebin_view.home"))  

    return render_template("sign_up.html", user=current_user)

#Log out view
@auth_view.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_view.login"))

#Validate user
def is_user_valid(username: str, email: str, password1: str, password2: str):
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        flash("User already exists.", category="error")
    elif len(email) < 4:
        flash("Email must be greater than 3 characters.", category="error")
    elif len(password1) < 5:
        flash("Password must be at least 5 characters long.", category="error")
    elif len(password1) > 20:
        flash("Password cannot be longer than 20 characters.", category="error")
    elif password1 != password2:
        flash("Passwords are not the same.", category="error")
    else:
        return True
