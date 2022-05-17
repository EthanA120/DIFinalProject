from app.blackjack.models import Blackjack
from flask_login import login_required, current_user
from flask import Blueprint, request, render_template, make_response

blackjack = Blueprint('blackjack', __name__)


@blackjack.route("/blackjack", methods=["GET", "POST"])
@login_required
def play_game():
    blj = Blackjack()
    if 'start' in request.form:
        blj = Blackjack()

    game_cookie = request.cookies.get("game_board")
    if game_cookie:
        blj.hand = game_cookie.split(',')

    if blj.game_alive():
        if 'card' in request.form:
            blj.new_card()

    resp = make_response(render_template("games/blackjack.html", msg=blj.msg, hand=blj.hand, hand_sum=blj.sum))
    c = ",".join([x[0] for x in blj.hand])
    print(c)
    resp.set_cookie("game_board", c, expires=0)
    return resp
