from app import db, login_mngr
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
    black_jack = db.Column(db.Integer, default=0)


# db.drop_all()
db.create_all()
db.session.commit()
