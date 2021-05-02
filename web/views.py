from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Pastebin
from . import db

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
      pastebin = request.form.get("pastebin")

      if len(pastebin) < 1:
         flash("Your pastebin have to be at least 1 word long.", category="error")
      elif len(pastebin) > 6000000:
         flash("Your pastebin cannot exceed 6000000 symbols limit.", category="error")
      else:
         if current_user.is_anonymous:
            new_pastebin = Pastebin(content=pastebin)
         else:
            new_pastebin = Pastebin(content=pastebin, user_id=current_user.id)
         db.session.add(new_pastebin)
         db.session.commit()
         flash("Pastebin added!", category="success")
   return render_template("home.html", user=current_user)

@views.route("/<link>")
def pastebins(link: str):
   if Pastebin.query.filter_by(link=link).first():
      return render_template("todo.html", user=current_user)
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("views.home"))

#@views.route("/delete-note", methods=["POST"])
#@login_required
#def delete_note():
#    note = json.loads(request.data)
#    noteId = note["noteId"]
#    note = Note.query.get(noteId)
#
#    if note:
#        if note.user_id == current_user.id:
#            db.session.delete(note)
#            db.session.commit()
#            return jsonify({})
