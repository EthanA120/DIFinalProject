from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import SubmitField, StringField, PasswordField, BooleanField


class RegisterForm(FlaskForm):
    user_name = StringField('NewTask', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class ForgotPassForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    reset_code = StringField('NewTask', validators=[DataRequired(), Length(6, max=6)])
    new_pass = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Submit')
