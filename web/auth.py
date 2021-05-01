from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Username doesn't exist.", category="error")
    
    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        age = request.form.get("age")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if check_input(username, first_name, last_name, age, email, password1, password2):
            new_user = User(username=username, first_name=first_name, last_name=last_name, age=age, email=email, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account successfully created!", category="success")

            return redirect(url_for("views.home"))  

    return render_template("sign_up.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

def check_input(username, first_name, last_name, age, email, password1, password2):
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        flash("User already exists.", category="error")
    elif len(email) < 4:
        flash("Email must be greater than 3 characters.", category="error")
    elif len(first_name) < 2:
        flash("Username must be greater than 1 character.", category="error")
    elif len(first_name) < 2:
        flash("First name must be greater than 1 character.", category="error")
    elif len(last_name) < 2:
        flash("Last name must be greater than 1 character.", category="error")
    elif int(age) < 1:
        flash("Age needs to be greater than 0.", category="error")
    elif len(password1) < 5:
        flash("Password must be at least 5 characters long.", category="error")
    elif password1 != password2:
        flash("Passwords are not the same.", category="error")
    else:
        return True
