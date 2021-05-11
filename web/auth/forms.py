from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from web.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_username(self, username):
        """
        Check if user with this username exists
        """
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            raise ValidationError(f"User with name {username.data} doesn't exists.")

    def validate_password(self, password):
        """
        Check if password is correct for given username
        """
        user = User.query.filter_by(username=self.username.data).first()
        if not user.check_password(self.password.data):
            raise ValidationError(f"Wrong password.")
    

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64, message="Username needs to be at least %(min)d characters long and can't exceed %(max)d characters.")])
    email = StringField("E-Mail", validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, message="Password needs to be at least %(min)d characters long.")])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", message="Both passwords must be equal.")])
    submit = SubmitField("Submit")
    
    def validate_username(self, username):
        """
        Check if user with this username already exists, then check for bad characters in username
        """
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            raise ValidationError(f"User with name {username.data} already exists.")
        else:    
            excluded_chars = " *?!'^+%&/()=}][{$#"
            for char in self.username.data:
                if char in excluded_chars:
                    raise ValidationError(f"Character {char} is not allowed in username.")
    
    def validate_email(self, email):
        """
        Check if e-mail is already taken
        """
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            raise ValidationError(f"User already exists with this E-mail.")
