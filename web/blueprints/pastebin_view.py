from dateutil.relativedelta import relativedelta
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import make_response
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.security import generate_password_hash
from web.models.pastebin import Pastebin
from web import db

pastebin_view = Blueprint("pastebin_view", __name__)

#Create pastebin
@pastebin_view.route("/", methods=["GET", "POST"])
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
         new_pastebin.encode_link()
         response = make_response(redirect(url_for("pastebin_view.pastebin", link=new_pastebin.link)))
         if private == "True":
            if password != "".strip():
               new_pastebin.password = generate_password_hash(password, method="sha256")
               #Set cookie using format k = pastebin link, v = hashed password
               response.set_cookie(new_pastebin.link, new_pastebin.password)
            else:
               flash("Please input password else uncheck Private.", category="error")
               return render_template("home.html", user=current_user, public_pastebins=get_public_pastebins())
         #Set expiration date and add the date to pastebin model if checkbox is checked
         if expire == "True" and expiration_date != "never":
            if expiration_date == "1min":
               new_pastebin.expire_date = new_pastebin.date + relativedelta(minutes=+1)
            elif expiration_date == "15min":
               new_pastebin.expire_date = new_pastebin.date + relativedelta(minutes=+15)
            elif expiration_date == "hour":
               new_pastebin.expire_date = new_pastebin.date + relativedelta(hours=+1)
            elif expiration_date == "day":
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
@pastebin_view.route("/<link>", methods=["GET", "POST"])
def pastebin(link: str):
   if request.method == "GET":
      pastebin = Pastebin.query.filter_by(link=link).first()
      password_cookie = request.cookies.get(link)
      
      if pastebin and not pastebin.is_expired():
         if not pastebin.password or password_cookie == pastebin.password:
            return render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.utcnow().replace(microsecond=0))
         else:
            if pastebin.user_id is not None and str(pastebin.user_id) == current_user.get_id():
               return render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.utcnow().replace(microsecond=0))
            else:
               flash("This pastebin is private.", category="error")
               return render_template("pastebin.html", user=current_user, link=link, password=pastebin.password, time=datetime.utcnow().replace(microsecond=0))
      else:
         flash("Can't find pastebin.", category="error")
         return redirect(url_for("pastebin_view.home"))
   
   if request.method == "POST":
      pastebin = Pastebin.query.filter_by(link=link).first()
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
   pastebin = Pastebin.query.filter_by(link=link).first()
   password_cookie = request.cookies.get(link)

   if pastebin and not pastebin.is_expired():   
      response = make_response(pastebin.content)
      response.headers.add("Content-Type", "text/plain")

      if not pastebin.password or password_cookie == pastebin.password:
         return response
      else:
         if pastebin.user_id is not None and str(pastebin.user_id) == current_user.get_id():
            return response
         else:
            flash("This pastebin is private.", category="error")
            return redirect(url_for("pastebin_view.pastebin", link=link))
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("pastebin_view.home"))

#Download pastebin
@pastebin_view.route("/download/<link>")
def download_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first()
   password_cookie = request.cookies.get(link)

   if pastebin and not pastebin.is_expired():
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
            return redirect(url_for("pastebin_view.pastebin", link=link))
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("pastebin_view.home"))

#Delete pastebin (Only user can remove his own pastebin)
@login_required
@pastebin_view.route("/delete/<link>")
def delete_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first()

   if pastebin and not pastebin.is_expired():
      if pastebin.user_id is not None and str(pastebin.user_id) == current_user.get_id():
         db.session.delete(pastebin)
         db.session.commit()
         flash("Sucessfully removed pastebin.", category="success")
         return redirect(url_for("user_view.user"))
      else:
         flash("You don't have permission to do that.", category="error")
         return redirect(url_for("pastebin_view.home"))
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("pastebin_view.home"))

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


#Get last 10 pastebins that are not private
def get_public_pastebins():
   pastebins = Pastebin.query.filter_by(password=None).all()[-10:]
   for pastebin in pastebins:
      pastebin.is_expired()
   return pastebins
