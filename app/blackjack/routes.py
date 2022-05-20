from app.blackjack.models import Blackjack
from flask_login import login_required, current_user
from flask import Blueprint, request, render_template, session


blackjack = Blueprint('blackjack', __name__)
start = False


@blackjack.route("/blackjack", methods=["GET", "POST"])
@login_required
def play_game():
    deal = False
    wager = 0
    global start
    global blj

    if 'start' in request.form or not start:
        start = True
        deal = True
        session['lock'] = False
        blj = Blackjack()

    if 'deal' in request.form:
        deal = False
        wager = request.form.get('deal')

    if 'hit' in request.form and blj.p_game_alive[0]:
        blj.p_sum, blj.p_game_alive = blj.new_card(blj.p_hand, blj.p_aces, blj.p_sum)

    if ('stand' in request.form or not blj.p_game_alive[0]) and not session['lock']:
        blj.cover = blj.open_cards()
        blj.dealing(wager)
        session['lock'] = True

    p_alive = blj.p_game_alive[0]
    p_hand = [x[1] for x in blj.p_hand]
    c_hand = [x[1] for x in blj.c_hand]
    p_msg = blj.p_game_alive[2]
    c_msg = blj.c_game_alive[2]

    return render_template("games/blackjack.html",
                           back=blj.back, msg=blj.msg, p_msg=p_msg, c_msg=c_msg, p_hand=p_hand,
                           p_sum=blj.p_sum, c_hand=c_hand, c_sum=blj.c_sum, cover=blj.cover,
                           p_alive=p_alive, deal=deal, wager=wager
                           )
