from sqlalchemy import exc
from app import app, login_mngr, mail
from app.forms import RegisterForm, LoginForm, ForgotPassForm
from app.models import db, Player, Score, Game
from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, login_required, logout_user
from flask_mail import Message
from random import randint
from enrich import printr


@login_mngr.user_loader
def load_user(userid):
    userid = int(userid)
    return db.session.query(Player).get(userid)


@app.route('/', methods=["POST", "GET"])
def index():
    # del session['deal']
    games_list = db.session.query(Game).all()
    if 'deal' not in session:
        session['deal'] = None
        print(session)
    if not session['deal']:
        session['hide'] = True
    
    return render_template('index.html', games_list=games_list)


@app.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated: # if already logged on:
        return redirect(url_for('index')) # redirect to homepage
    
    form = RegisterForm() # specify what form to relate to in this def

    if form.validate_on_submit():
        if not db.session.query(Player).filter_by(email=form.email.data).first(): # if email does'nt exist in database:
            try:
                player = Player(username=form.user_name.data, email=form.email.data.lower(), password=generate_password_hash(form.password.data), score=Score()) # add player object with the values in registration form
                player.add_user() # register to database
                return redirect(url_for('login')) # redirect to url defined in 'login' def

            except exc.IntegrityError: # except if one of the values are already exist in the database
                flash('Username or email are already in use, please try again.', 'warning')

    return render_template('loginRegister/register.html', form=form) # show html file (location of html file, variables to send to file)


@app.route('/login', methods=['GET', 'POST'])
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

        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Invalid username or password.', 'warning')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('loginRegister/login.html', form=form)


@app.route('/forgotpass', methods=["POST", "GET"])
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
        rs_user.password = generate_password_hash(form.new_pass.data)
        db.session.commit()
        session['user_mail'] = None
        session['email_sent'] = False
        session['reset_code'] = None
        return redirect(url_for('login'))

    return render_template('loginRegister/forgotpass.html', form=form, email_sent=session['email_sent'], reset_code=session['reset_code'],
                           code_validation=session['code_validation'])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
