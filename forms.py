from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import sqlalchemy
import app


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        with app.app.app_context():
            user = app.db.session.scalar(sqlalchemy.select(app.models.User).where(
                app.models.User.username == username.data))
            if user is not None:
                raise ValidationError('Invalid Username')

    def validate_email(self, email):
        with app.app.app_context():
            user = app.db.session.scalar(sqlalchemy.select(app.models.User).where(
                app.models.User.email == email.data))
            if user is not None:
                raise ValidationError('Invalid Email')

