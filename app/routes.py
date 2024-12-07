from app import app
from app.models import db, Player, Game
from flask import render_template, session


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

