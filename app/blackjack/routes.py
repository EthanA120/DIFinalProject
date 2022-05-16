from flask import Blueprint, render_template
from app.blackjack.models import Blackjack
from flask_login import login_required, current_user

blackjack = Blueprint('blackjack', __name__)


@blackjack.route("/blackjack", methods=["GET", "POST"])
@login_required
def play_game():
    return render_template("games/blackjack.html")
