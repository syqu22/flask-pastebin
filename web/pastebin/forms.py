from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired, Length, ValidationError
from web.models import Pastebin


class CreatePastebinForm(FlaskForm):
    types = {
        "Text": "text",
        "Bash": "bash", 
        "C" : "c",
        "C#": "c#",
        "C++": "c++",
        "CSS": "css",
        "GO": "go",
        "HTML": "html",
        "HTTP": "http",
        "INI": "ini",
        "Java": "java",
        "JavaScript": "js",
        "JSON": "json",
        "Kotlin": "kotlin",
        "LUA": "lua",
        "Markdown": "markdown",
        "Objective-C": "objectivec",
        "Perl": "perl",
        "PHP": "php",
        "Python": "python",
        "R": "r",
        "Ruby": "ruby",
        "Rust": "rust",
        "SQL": "sql",
        "Swift": "swift",
        "TypeScript": "typescript"
    }

    dates = {
        "Never": None,
        "1 Minute": "1min",
        "15 Minutes": "15min",
        "1 Hour": "hour",
        "1 Day": "day",
        "1 Week": "week",
        "1 Month": "month", 
        "1 Year": "year"
    }

    title = StringField("Title", validators=[Length(min=2, max=100, message="Title needs to be at least %(min)d characters long and can't exceed %(max)d characters.")])
    content = TextAreaField("Paste", validators=[DataRequired(), Length(max=60000, message="Pastebin can't be longer than %(max)d characters.")])
    syntax = SelectField("Syntax type", choices=types, validators=[DataRequired()])
    private = BooleanField("Private")
    password = StringField()
    expire = BooleanField("Expiration")
    expire_date = SelectField(choices=dates, validators=[DataRequired()])
    submit = SubmitField("Create")

    

    
