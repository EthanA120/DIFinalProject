from sqlalchemy import exc
from app import app, login_mngr
from app.models import db, Player, Score
from app.forms import RegisterForm, LoginForm
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, session, request, flash


@login_mngr.user_loader
def load_user(userid):
    userid = int(userid)
    return db.session.query(Player).get(userid)


@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            Player(username=form.user_name.data, email=form.email.data, password=form.password.data, score=Score()).add_user()

            return redirect(url_for('index'))

        except exc.IntegrityError:
            flash('Username or email are already in use, please try again', 'warning')

    return render_template('loginRegister/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(Player).filter_by(email=form.email.data).first()

        if user is None or not user.password == form.password.data:
            flash('Invalid username or password', 'warning')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('loginRegister/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
