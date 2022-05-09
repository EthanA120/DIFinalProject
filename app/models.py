from app import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tic_tac_toe = db.Column(db.Integer)
