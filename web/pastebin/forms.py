from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired, Length, ValidationError
from web.models import Pastebin
from flask import request

class CreatePastebinForm(FlaskForm):
    types = [
        "Text","Bash", "C", "C#", "C++", "CSS", "GO", "HTML", "HTTP", "INI",
        "Java", "JavaScript", "JSON", "Kotlin", "LUA", "Markdown", "Objective-C",
        "Perl", "PHP", "Python", "R", "Ruby", "Rust", "SQL", "TypeScript"
    ]

    dates = [
        "Never",
        "1 Minute",
        "15 Minutes",
        "1 Hour",
        "1 Day",
        "1 Week",
        "1 Month", 
        "1 Year"
    ]

    title = StringField("Title", default="Untitled", validators=[Length(max=100, message="Title needs to be at least %(min)d characters long and can't exceed %(max)d characters.")])
    content = TextAreaField("Paste", validators=[DataRequired(), Length(max=60000, message="Pastebin can't be longer than %(max)d characters.")])
    syntax = SelectField("Syntax type", choices=types, validators=[DataRequired()])
    private = BooleanField("Private")
    password = StringField()
    expire = SelectField("Expiration", choices=dates, validators=[DataRequired()])
    submit = SubmitField("Create")

class PrivatePastebin(FlaskForm):
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Enter")
