from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import Email, EqualTo, DataRequired, Length, ValidationError
from flask_blog1.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm password', 
                                    validators = [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')

    def validate_username(self,username): #To check whether a user is trying to register with previously existing username
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken')

    def validate_email(self,email): #To check whether a user is trying to register with previously existing email
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email has already been taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Log In')
    