from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, Optional

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

    title = StringField("Title", validators=[Optional(), Length(max=100, message="Title can't exceed %(max)d characters.")], filters= [lambda x: x or None])
    content = TextAreaField("Paste", validators=[DataRequired(), Length(max=60000, message="Pastebin can't be longer than %(max)d characters.")])
    syntax = SelectField("Syntax type", choices=types, validators=[DataRequired()])
    private = BooleanField("Private")
    password = StringField()
    expire = SelectField("Expiration", choices=dates, validators=[DataRequired()])
    submit = SubmitField("Create")

    def validate_title(self, title):
        """
        Check if user with this username already exists, then check for bad characters in username
        """
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in title.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in title.")

class PrivatePastebin(FlaskForm):
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Enter")
