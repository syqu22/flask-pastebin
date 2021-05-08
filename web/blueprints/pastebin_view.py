from dateutil.relativedelta import relativedelta
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
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
      paste_type = request.form.get("type_select")
      private = request.form.get("private")
      password = request.form.get("password")
      expire_select = request.form.get("expire")
      expiration_date = request.form.get("expire_select")

      if ispastebin_valid(title, pastebin, paste_type):
         new_pastebin = Pastebin(title=title if title != "" else None, content=pastebin, paste_type=paste_type, user_id=current_user.get_id())  
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

         validate_expiration_date(new_pastebin, expire_select, expiration_date)

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
         #Check if pastebin is private or if there is password alread saved in cookie
         if not pastebin.password or password_cookie == pastebin.password:
            return render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.utcnow().replace(microsecond=0))
         else:
            #If there is a password but pastebin is owned by current user, render page
            if pastebin.user_id is not None and str(pastebin.user_id) == current_user.get_id():
               return render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.utcnow().replace(microsecond=0))
            else:
               #Render page with password attribute
               flash("This pastebin is private.", category="error")
               return render_template("pastebin.html", user=current_user, link=link, password=pastebin.password, time=datetime.utcnow().replace(microsecond=0))
      else:
         abort(404)
   
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
      abort(404)

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
      abort(404)

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
      abort(404)

#Validate pastebin
def ispastebin_valid(title: str, pastebin: str, paste_type: str):
   types = [
      "text", "bash", "c", "c#", "c++", "css", "go", "html", "http", "ini", "java", "js","json", "kotlin", 
      "lua", "markdown", "objectivec", "perl", "php", "python", "r", "ruby", "rust", "sql", "swift", "typescript"]

   if len(title) > 150:
      flash("Title cannot exceed 150 characters limit.", category="error")
   elif len(pastebin) < 1:
      flash("Your pastebin must be at least 1 character long.", category="error")
   elif len(pastebin) > 6000000:
      flash("Your pastebin cannot exceed 6000000 characters limit.", category="error")
   elif paste_type not in types:
      flash("The syntax type you have choosed does not exist.", category="error")
   else:
      return True

#Set expiration date and add the date to pastebin model if checkbox is checked and time choosed
def validate_expiration_date(pastebin: Pastebin, expire_select: str, date: str):
   if expire_select == "True" and date != "never":
      if date == "1min":
         pastebin.expire_date = pastebin.date + relativedelta(minutes=+1)
      elif date == "15min":
         pastebin.expire_date = pastebin.date + relativedelta(minutes=+15)
      elif date == "hour":
         pastebin.expire_date = pastebin.date + relativedelta(hours=+1)
      elif date == "day":
         pastebin.expire_date = pastebin.date + relativedelta(days=+1)
      elif date == "week":
         pastebin.expire_date = pastebin.date + relativedelta(weeks=+1)
      elif date == "month":
         pastebin.expire_date = pastebin.date + relativedelta(months=+1)
      elif date == "year":
         pastebin.expire_date = pastebin.date + relativedelta(years=+1)

#Get last 10 pastebins that are not private
def get_public_pastebins():
   pastebins = Pastebin.query.filter_by(password=None).all()[-10:]
   for pastebin in pastebins:
      pastebin.is_expired()
   return pastebins
