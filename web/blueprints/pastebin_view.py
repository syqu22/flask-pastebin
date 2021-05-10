from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask.helpers import make_response
from flask_login import current_user
from flask_login.utils import login_required
from web.models.pastebin import Pastebin
from web import db

pastebin_view = Blueprint("pastebin_view", __name__)

@pastebin_view.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
      title = request.form.get("title") or None
      content = request.form.get("content")
      paste_type = request.form.get("paste_type")
      password = request.form.get("password") or None
      expire_date = request.form.get("expire_date") or None

      new_pastebin = Pastebin(title, content, paste_type, current_user.get_id(), expire_date, password)
      if new_pastebin.is_valid():
         response = make_response(redirect(url_for("pastebin_view.pastebin", link=new_pastebin.link)))
         if password:
            response.set_cookie(new_pastebin.link, new_pastebin.password)
         db.session.add(new_pastebin)
         db.session.commit()

         flash("Pastebin added!", category="success")
         return response
         
   return render_template("home.html", user=current_user, public_pastebins=get_public_pastebins())

@pastebin_view.route("/<link>", methods=["GET", "POST"])
def pastebin(link: str):
   if request.method == "GET":
      pastebin = Pastebin.query.filter_by(link=link).first_or_404()
      password_cookie = request.cookies.get(link)
      
      if not pastebin.is_expired():
         #Check if pastebin is private or if there is password alread saved in cookie
         if not pastebin.password or password_cookie == pastebin.password:
            return render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.utcnow().replace(microsecond=0))
         else:
            #If there is a password but pastebin is owned by current user, render page
            if pastebin.user_id and str(pastebin.user_id) == current_user.get_id():
               return render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.utcnow().replace(microsecond=0))
            else:
               #Else render page with password attribute
               flash("This pastebin is private.", category="error")
               return render_template("pastebin.html", user=current_user, link=link, password=pastebin.password, time=datetime.utcnow().replace(microsecond=0))
      else:
         abort(404)
   
   if request.method == "POST":
      pastebin = Pastebin.query.filter_by(link=link).first_or_404()
      password = request.form.get("password")
      response = make_response(render_template("pastebin.html", user=current_user, pastebin=pastebin))

      #If password is correct save it as a cookie for later use
      if pastebin.check_password(password):
         response.set_cookie(link, pastebin.password)
         return response
      else:
         flash("Password is incorrect!", category="error")
         return redirect(url_for("pastebin_view.pastebin", link=link))

#View raw pastebin
@pastebin_view.route("/raw/<link>")
def raw_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first_or_404()
   password_cookie = request.cookies.get(link)

   if not pastebin.is_expired():   
      response = make_response(pastebin.content)
      response.headers.add("Content-Type", "text/plain")

      if not pastebin.password or password_cookie == pastebin.password:
         return response
      else:
         if pastebin.user_id and str(pastebin.user_id) == current_user.get_id():
            return response
         else:
            abort(403)
   else:
      abort(404)

#Download pastebin
@pastebin_view.route("/download/<link>")
def download_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first_or_404()
   password_cookie = request.cookies.get(link)

   if not pastebin.is_expired():
      response = make_response(pastebin.content)
      response.headers.add("Content-Type", "text/plain")
      response.headers.add("Content-Disposition", "attachment", filename=link+".txt")

      if not pastebin.password or password_cookie == pastebin.password:
         return response
      else:
         if pastebin.user_id and str(pastebin.user_id) == current_user.get_id():
            return response
         else:
            abort(403)
   else:
      abort(404)

#Delete pastebin (Only user can remove his own pastebin)
@login_required
@pastebin_view.route("/delete/<link>")
def delete_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first_or_404()

   if not pastebin.is_expired():
      if pastebin.user_id and str(pastebin.user_id) == current_user.get_id():
         db.session.delete(pastebin)
         db.session.commit()
         flash("Sucessfully removed pastebin.", category="success")
         return redirect(url_for("user_view.user"))
      else:
         abort(403)
   else:
      abort(404)

def get_public_pastebins():
   """
   Get last 10 pastebins that are not private
   """
   pastebins = Pastebin.query.filter_by(password=None).all()[-10:]
   for pastebin in pastebins:
      pastebin.is_expired()
   return pastebins
