from flask_wtf import FlaskForm  # Flask wrapper
from wtforms import StringField, PasswordField, BooleanField, SubmitField   # Python WTF elements
from wtforms.validators import DataRequired


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
