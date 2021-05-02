from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from flask_login.utils import login_required
from .models import Pastebin
from .util.pastebin_util import PastebinUtil
from . import db

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
      pastebin = request.form.get("pastebin")

      if len(pastebin) < 1:
         flash("Your pastebin must be at least 1 character long.", category="error")
      elif len(pastebin) > 6000000:
         flash("Your pastebin cannot exceed 6000000 characters limit.", category="error")
      else:
         if current_user.is_anonymous:
            new_pastebin = Pastebin(content=pastebin)
         else:
            new_pastebin = Pastebin(content=pastebin, user_id=current_user.id)      
         db.session.add(new_pastebin)
         db.session.commit()
         new_pastebin.link = PastebinUtil.base36_encode(new_pastebin.id)
         db.session.commit()
         flash("Pastebin added!", category="success")
         return redirect(url_for("views.pastebins", link=new_pastebin.link))
   return render_template("home.html", user=current_user)

@views.route("/<link>")
def pastebins(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first()
   if pastebin:
      return render_template("pastebin.html", user=current_user, pastebin=pastebin)
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("views.home"))

@views.route("/user")
@login_required
def user():
   return render_template("user.html", user=current_user)
