from app.blackjack.models import Blackjack
from flask_login import login_required, current_user
from flask import Blueprint, request, render_template, make_response, redirect, url_for, session


blackjack = Blueprint('blackjack', __name__)
start = False


@blackjack.route("/blackjack", methods=["GET", "POST"])
@login_required
def play_game():
    global start
    global blj

    if 'start' in request.form or not start:
        start = True
        blj = Blackjack()

    if 'card' in request.form and blj.game_alive():
        blj.new_card()

    hand = [x[1] for x in blj.hand]

    return render_template("games/blackjack.html", msg=blj.msg, hand=hand, hand_sum=blj.sum, back=blj.back)
