from app import app
from app.models import db
# from app.forms import *
from flask import render_template, redirect, url_for, session, request, flash

db.create_all()
db.session.commit()


@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')
