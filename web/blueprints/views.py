from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import make_response, send_file
from flask.wrappers import Response
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from web.models import Pastebin
from web import db
from io import StringIO

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
      title = request.form.get("title")
      pastebin = request.form.get("pastebin")
      private = request.form.get("private")
      password = request.form.get("password")

      #Validate if pastebin is correct
      if check_pastebin(title, pastebin):
         new_pastebin = Pastebin(title=title, content=pastebin, user_id=None if current_user.is_anonymous else current_user.id)  
         #Add pastebin to database
         db.session.add(new_pastebin)
         db.session.commit()
         new_pastebin.link = encode_link(new_pastebin.id)
         response = make_response(redirect(url_for("views.pastebin", link=new_pastebin.link)))
         if private == "True":
            new_pastebin.password = generate_password_hash(password, method="sha256")
            #Set cookie using format k = pastebin link, v = hashed password
            response.set_cookie(new_pastebin.link, new_pastebin.password)   
            #Update the same pastebin with new link based on ID and password
         db.session.commit()

         flash("Pastebin added!", category="success")
         return response
      
         
   return render_template("home.html", user=current_user, public_pastebins=get_public_pastebins())

@views.route("/<link>", methods=["GET", "POST"])
def pastebin(link: str):
   if request.method == "GET":
      pastebin = Pastebin.query.filter_by(link=link).first()
      password_cookie = request.cookies.get(link)
      if pastebin:
         #Check if pastebin has password or if passwords are correct
         if pastebin.password == None or password_cookie == pastebin.password:
            return render_template("pastebin.html", user=current_user, pastebin=pastebin)
         else:
            #If there is no cookie with correct password return template with additional parameter password
            return render_template("pastebin.html", user=current_user, pastebin=pastebin, password=pastebin.password)
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

#Additional route just for raw format, same as normal pastebin
@views.route("/raw/<link>")
def raw_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first()
   password_cookie = request.cookies.get(link)
   if pastebin:   
      response = make_response(pastebin.content)
      response.headers.add("Content-Type", "text/plain")

      if pastebin.password == None or password_cookie == pastebin.password:
         return response
      else:
         if pastebin.user_id == current_user.get_id():
            return response
         else:
            flash("This pastebin is private.", category="error")
            return redirect(url_for("views.pastebin", link=link))
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("views.home"))

@views.route("/download/<link>")
def download_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first()
   password_cookie = request.cookies.get(link)
   if pastebin:
      response = make_response(pastebin.content)
      response.headers.add("Content-Type", "text/plain")
      response.headers.add("Content-Disposition", "attachment", filename=link+".txt")

      if pastebin.password == None or password_cookie == pastebin.password:
         return response
      else:
         if pastebin.user_id == current_user.get_id():
            return response
         else:
            flash("This pastebin is private.", category="error")
            return redirect(url_for("views.pastebin", link=link))
   else:
      flash("Can't find pastebin.", category="error")
      return redirect(url_for("views.home"))

@views.route("/user")
@login_required
def user():
   return render_template("user.html", user=current_user)

def check_pastebin(title: str, pastebin: str):
   if len(title) < 3:
      flash("Title must be at least 3 characters long.", category="error")
   elif len(title) > 150:
      flash("Title cannot exceed 150 characters limit.", category="error")
   elif len(pastebin) < 1:
      flash("Your pastebin must be at least 1 character long.", category="error")
   elif len(pastebin) > 6000000:
      flash("Your pastebin cannot exceed 6000000 characters limit.", category="error")
   else:
      return True

#Encode link using base36 encoding
def encode_link(link):
      assert link >= 0, 'Positive integer is required'
      if link == 0:
            return '0'
      base36 = []
      while link != 0:
         link, i = divmod(link, 36)
         base36.append('0123456789abcdefghijklmnopqrstuvwxyz'[i])
      return ''.join(reversed(base36))

#Get last 10 pastebins that don't have password
def get_public_pastebins():
   pastebins = Pastebin.query.filter_by(password=None).all()[-10:]

   return pastebins
