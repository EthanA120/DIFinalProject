from sqlalchemy import exc
from app import app, login_mngr, mail
from app.forms import RegisterForm, LoginForm, ForgotPassForm
from app.models import db, Player, Score, Game
from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, login_required, logout_user
from flask_mail import Message
from random import randint


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
    form = RegisterForm()

    if form.validate_on_submit():
        if not db.session.query(Player).filter_by(email=form.email.data).first():
            try:
                player = Player(username=form.user_name.data.lower(), email=form.email.data.lower(), password=generate_password_hash(form.password.data), score=Score())
                player.add_user()
                return redirect(url_for('login'))

            except exc.IntegrityError:
                flash('Username or email are already in use, please try again.', 'warning')

    return render_template('loginRegister/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
    
    email_sent = False
    reset_code = None
    code_validation = None

    if 'reset' in request.form and db.session.query(Player).filter_by(email=form.email.data.lower()).first():
        user = db.session.query(Player).filter_by(email=form.email.data.lower()).first()
        reset_code = randint(100000, 1000000)
        msg = Message("Reset password", sender="noreply@demo.com", recipients=["EthanA120@Gmail.com"])
        msg.body = f'Use this code to reset your password: {str(reset_code)}'
        mail.send(msg)
        email_sent = True
    else:
        flash('Email does\'nt exist', 'warning')
        
    if 'validation' in request.form:  # and form.reset_code.data == reset_code
        print(reset_code, form.reset_code.data, type(reset_code), type(form.reset_code.data))
        code_validation = form.reset_code.data
    else:
        flash('Verification code does\'nt match', 'warning')
    
    if form.validate_on_submit() and reset_code and code_validation:
        user.password = generate_password_hash(form.new_pass.data)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('loginRegister/forgotpass.html', form=form, email_sent=email_sent, reset_code=reset_code,
                           code_validation=code_validation)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
