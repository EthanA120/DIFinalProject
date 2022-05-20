from app import db
from flask_login import UserMixin


class Player(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    score = db.relationship("Score", back_populates="player", uselist=False)

    def add_user(self):
        db.session.add(self)
        db.session.commit()


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), unique=True)
    player = db.relationship("Player", back_populates="score", uselist=False)

    tic_tac_toe = db.Column(db.Integer, default=0)
    ctic_tac_toe = db.Column(db.Integer, default=0)

    blackjack = db.Column(db.Integer, default=0)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(50), unique=True)
    image = db.Column(db.String(250), unique=True)
    title = db.Column(db.String(50), unique=True)
    info = db.Column(db.String(500))


# db.drop_all()
db.create_all()
db.session.commit()
