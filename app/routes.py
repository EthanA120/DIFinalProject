from builtins import id

from sqlalchemy import exc
from app import app, login_mngr
from app.forms import RegisterForm, LoginForm
from app.models import db, Player, Score, Game
from flask import render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, login_required, logout_user


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
                player = Player(username=form.user_name.data, email=form.email.data, password=generate_password_hash(form.password.data), score=Score())
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
        user = db.session.query(Player).filter_by(email=form.email.data).first()

        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Invalid username or password.', 'warning')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('loginRegister/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
