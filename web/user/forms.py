from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from web.models import User

class EditUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64, message="Username needs to be at least %(min)d characters long and can't exceed %(max)d characters.")])
    email = StringField("E-Mail", validators=[DataRequired(), Email(), Length(max=100)])
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=6, message="Password needs to be at least %(min)d characters long.")])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", message="Both passwords must be equal.")])
    submit = SubmitField("Edit")
    
    def validate_username(self, username):
        """
        Check if user with this username already exists, then check for bad characters in username
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"Username {username.data} is already taken.")
        else:    
            excluded_chars = " *?!'^+%&/()=}][{$#"
            for char in username.data:
                if char in excluded_chars:
                    raise ValidationError(f"Character {char} is not allowed in username.")
    
    def validate_email(self, email):
        """
        Check if e-mail is already taken
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"E-Mail is already taken.")

    def validate_new_password(self, new_password):
        """
        Check if password is the same as old password
        """
        if new_password.data == self.password.data and self.password.data == self.confirm_password.data:
            raise ValidationError(f"New and old passwords are the same")
