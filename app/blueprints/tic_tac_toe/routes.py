from app import db
from app.blueprints.tic_tac_toe.models import TicTacToe
from easyAI import Human_Player, AI_Player, Negamax
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, make_response, session

tic_tac_toe = Blueprint('tic_tac_toe', __name__)


@tic_tac_toe.route("/tictactoe", methods=["GET", "POST"])
@login_required
def play_game():
    if 'lock' not in session:
        session['lock'] = None

    ttt = TicTacToe([Human_Player(), AI_Player(Negamax(5))])

    game_cookie = request.cookies.get("game_board")
    if game_cookie:
        ttt.board = [int(x) for x in game_cookie.split(",")]

    if "choice" in request.form:
        ttt.play_move(request.form["choice"])
        if not ttt.is_over():
            ai_move = ttt.get_move()
            ttt.play_move(ai_move)

    if 'reset' in request.form or 'reset_score' in request.form:
        ttt.board = [0 for i in range(9)]
        session['lock'] = False

    if 'reset_score' in request.form:
        current_user.score.tic_tac_toe = 0
        current_user.score.ctic_tac_toe = 0
        db.session.commit()

    if ttt.is_over() and not session['lock']:
        msg = ttt.winner()
        db.session.commit()
        session['lock'] = True
    else:
        msg = "It's your turn to play"

    resp = make_response(render_template("games/tic_tac_toe.html", ttt=ttt, msg=msg))
    c = ",".join(map(str, ttt.board))
    resp.set_cookie("game_board", c)
    return resp
