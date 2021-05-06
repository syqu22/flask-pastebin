from dateutil.relativedelta import relativedelta
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import make_response
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from web.models import Pastebin
from web import db

views = Blueprint("views", __name__)

#Create pastebin
@views.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
      title = request.form.get("title")
      pastebin = request.form.get("pastebin")
      private = request.form.get("private")
      password = request.form.get("password")
      expire = request.form.get("expire")
      expiration_date = request.form.get("expire_select")

      if is_pastebin_valid(title, pastebin):
         new_pastebin = Pastebin(title=title if title != "" else None, content=pastebin, user_id=current_user.get_id())  
         db.session.add(new_pastebin)
         db.session.commit()
         new_pastebin.link = encode_link(new_pastebin.id)
         response = make_response(redirect(url_for("views.pastebin", link=new_pastebin.link)))
         if private == "True":
            if password != "".strip():
               new_pastebin.password = generate_password_hash(password, method="sha256")
               #Set cookie using format k = pastebin link, v = hashed password
               response.set_cookie(new_pastebin.link, new_pastebin.password)
            else:
               flash("Please input password else uncheck Private.", category="error")
               return render_template("home.html", user=current_user, public_pastebins=get_public_pastebins())
         if expire == "True" and expiration_date != "never":
            if expiration_date == "day":
               new_pastebin.expire_date = new_pastebin.date + relativedelta(days=+1)
            elif expiration_date == "week":
               new_pastebin.expire_date = new_pastebin.date + relativedelta(weeks=+1)
            elif expiration_date == "month":
               new_pastebin.expire_date = new_pastebin.date + relativedelta(months=+1)
            elif expiration_date == "year":
               new_pastebin.expire_date = new_pastebin.date + relativedelta(years=+1)

         #Update the same pastebin with new link based on ID and optionally password and/or expiration date
         db.session.commit()

         flash("Pastebin added!", category="success")
         return response
          
   return render_template("home.html", user=current_user, public_pastebins=get_public_pastebins())

#View pastebin
@views.route("/<link>", methods=["GET", "POST"])
def pastebin(link: str):
   if request.method == "GET":
      pastebin = Pastebin.query.filter_by(link=link).first()
      password_cookie = request.cookies.get(link)

      if pastebin:
         if not pastebin.password or password_cookie == pastebin.password:
            return render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.now().replace(microsecond=0))
         else:
            if pastebin.user_id is not None and str(pastebin.user_id) == current_user.get_id():
               return render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.now().replace(microsecond=0))
            else:
               flash("This pastebin is private.", category="error")
               return render_template("pastebin.html", user=current_user, link=link, password=pastebin.password, time=datetime.now().replace(microsecond=0))
      else:
         flash("Can't find pastebin.", category="error")
         return redirect(url_for("views.home"))
   
   if request.method == "POST":
      pastebin = Pastebin.query.filter_by(link=link).first()
      password = request.form.get("password")
      response = make_response(render_template("pastebin.html", user=current_user, pastebin=pastebin))

      #If password is correct save it as a cookie for later use
      if check_password_hash(pastebin.password, password):
         response.set_cookie(link, pastebin.password)
         return response
      else:
         flash("Password is incorrect!", category="error")
         return redirect(url_for("views.pastebin", link=link))

#View raw pastebin
@views.route("/raw/<link>")
def raw_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first()
   password_cookie = request.cookies.get(link)

   if pastebin:   
      response = make_response(pastebin.content)
      response.headers.add("Content-Type", "text/plain")

      if not pastebin.password or password_cookie == pastebin.password:
         return response
      else:
         if pastebin.user_id is not None and str(pastebin.user_id) == current_user.get_id():
            return response
         else:
            flash("This pastebin is private.", category="error")
            return redirect(url_for("views.pastebin", link=link))
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("views.home"))

#Download pastebin
@views.route("/download/<link>")
def download_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first()
   password_cookie = request.cookies.get(link)

   if pastebin:
      response = make_response(pastebin.content)
      response.headers.add("Content-Type", "text/plain")
      response.headers.add("Content-Disposition", "attachment", filename=link+".txt")

      if not pastebin.password or password_cookie == pastebin.password:
         return response
      else:
         if pastebin.user_id is not None and str(pastebin.user_id) == current_user.get_id():
            return response
         else:
            flash("This pastebin is private.", category="error")
            return redirect(url_for("views.pastebin", link=link))
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("views.home"))

#Delete pastebin (Only user can remove his own pastebin)
@login_required
@views.route("/delete/<link>")
def delete_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first()

   if pastebin:
      if pastebin.user_id is not None and str(pastebin.user_id) == current_user.get_id():
         db.session.delete(pastebin)
         db.session.commit()
         flash("Sucessfully removed pastebin.", category="success")
         return redirect(url_for("user_view.user"))
      else:
         flash("You don't have permission to do that.", category="error")
         return redirect(url_for("views.home"))
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("views.home"))

#Validate pastebin
def is_pastebin_valid(title: str, pastebin: str):
   if len(title) > 150:
      flash("Title cannot exceed 150 characters limit.", category="error")
   elif len(pastebin) < 1:
      flash("Your pastebin must be at least 1 character long.", category="error")
   elif len(pastebin) > 6000000:
      flash("Your pastebin cannot exceed 6000000 characters limit.", category="error")
   else:
      return True

#Encode link using base36
def encode_link(link):
      assert link >= 0, 'Positive integer is required'
      if link == 0:
            return '0'
      base36 = []
      while link != 0:
         link, i = divmod(link, 36)
         base36.append('0123456789abcdefghijklmnopqrstuvwxyz'[i])
      return ''.join(reversed(base36))

#Get last 10 pastebins that are not private
def get_public_pastebins():
   pastebins = Pastebin.query.filter_by(password=None).all()[-10:]

   return pastebins
