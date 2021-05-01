from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Pastebin
from . import db
import json

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
      pass
      #note = request.form.get("note")

      #if len(note) < 1:
      #   flash("Note is too short!", category="error")
      #else:
      #   new_note = Note(content=note, user_id=current_user.id)
      #   db.session.add(new_note)
      #   db.session.commit()
      #   flash("Note added!", category="success")
   return render_template("home.html", user=current_user)

@views.route("/pastebins")
@login_required
def pastebins():
   return render_template("pastebins.html", user=current_user)

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
