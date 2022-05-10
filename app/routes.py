from app import app
from app.models import db
from app.forms import RegisterForm, LoginForm
from flask import render_template, redirect, url_for, session, request, flash

db.create_all()
db.session.commit()


@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    return render_template('loginRegister/register.html', form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    return render_template('loginRegister/login.html', form=form)
