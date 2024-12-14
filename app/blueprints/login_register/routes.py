from sqlalchemy import exc
from app import mail, login_mngr
from app.forms import RegisterForm, LoginForm, ForgotPassForm
from app.models import db, Player, Score
from flask import render_template, redirect, url_for, flash, session, request
from argon2 import PasswordHasher, exceptions
from flask_login import current_user, login_user, login_required, logout_user
from flask_mail import Message
from random import randint
from colorich import printr
from flask import Blueprint, render_template, request, session

login_register = Blueprint('login_register', __name__)
phash = PasswordHasher()

@login_mngr.user_loader
def load_user(userid):
    userid = int(userid)
    return db.session.query(Player).get(userid)

@login_register.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated: # if already logged on:
        return redirect(url_for('index')) # redirect to homepage
    
    form = RegisterForm() # specify what form to relate to in this def

    if form.validate_on_submit():
        if not db.session.query(Player).filter_by(email=form.email.data).first(): # if email does'nt exist in database:
            try:
                player = Player(username=form.user_name.data, email=form.email.data.lower(), password=phash.hash(form.password.data), score=Score()) # add player object with the values in registration form
                player.add_user() # register to database
                return redirect(url_for('login_register.login')) # redirect to url defined in 'login' def

            except exc.IntegrityError: # except if one of the values are already exist in the database
                flash('Username or email are already in use, please try again.', 'warning')

    return render_template('loginRegister/register.html', form=form) # show html file (location of html file, variables to send to file)


@login_register.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # if already logged on:
        return redirect(url_for('index')) # redirect to homepage

    # session variables from forget pass def, reset vars when returning to login page after reseting password
    session['code_validation'] = None
    if 'user_mail' not in session:
        session['user_mail'] = None
        session['email_sent'] = False
        session['reset_code'] = None
    
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(Player).filter_by(email=form.email.data.lower()).first()
        print(form.email.data.lower())

        if user is None:
            printr("User doesn't exist", "Red")
            flash('Invalid username or password.', 'warning')  # Consistent message for both cases
            return redirect(url_for('login_register.login'))

        try:
            phash.verify(user.password, form.password.data)  # Argon2 verification
        except exceptions.VerifyMismatchError:
            printr("Password doesn't match", "Red")
            flash('Invalid username or password.', 'warning')  # Consistent message
            return redirect(url_for('login_register.login'))  
        except exceptions.InvalidHashError:
            printr("Hashed password doesn't exist, please hash it again", "OrangeRed")

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('loginRegister/login.html', form=form)


@login_register.route('/forgotpass', methods=["POST", "GET"])
def forgotpass():
    form = ForgotPassForm()

    if 'reset' in request.form: # html submit name of email form
        if db.session.query(Player).filter_by(email=form.email.data.lower()).first():
            session['user_mail'] = form.email.data.lower()
            session['reset_code'] = str(randint(100000, 1000000))
            printr(session['reset_code'], 'OrangeRed')
            msg = Message("Reset password", sender="noreply@demo.com", recipients=["EthanA120@Gmail.com"])
            msg.body = f"Use this code to reset your password: {session['reset_code']}"
            mail.send(msg)
            session['email_sent'] = True
        else:
            flash('Email does\'nt exist', 'warning')
    
    if 'validation' in request.form: # html submit name of reset code validation form
        if form.reset_code.data == session['reset_code']:
            session['code_validation'] = form.reset_code.data
        else:
            flash('Verification code does\'nt match', 'warning')
            
    if form.submit.data and session['reset_code'] and session['code_validation']:
        rs_user = db.session.query(Player).filter_by(email=session['user_mail']).first()
        rs_user.password = phash.hash(form.new_pass.data)
        db.session.commit()
        session['user_mail'] = None
        session['email_sent'] = False
        session['reset_code'] = None
        return redirect(url_for('login_register.login'))

    return render_template('loginRegister/forgotpass.html', form=form, email_sent=session['email_sent'], reset_code=session['reset_code'],
                           code_validation=session['code_validation'])

@login_register.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_register.login'))
