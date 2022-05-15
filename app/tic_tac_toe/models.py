from easyAI import TwoPlayerGame
from app.routes import current_user, db


class TicTacToe(TwoPlayerGame):
    """The board positions are numbered as follows:
    1 2 3
    4 5 6
    7 8 9
    """

    WIN_LINES = [
        [1, 2, 3],  # Horizontal
        [4, 5, 6],
        [7, 8, 9],
        [1, 4, 7],  # Vertical
        [2, 5, 8],
        [3, 6, 9],
        [1, 5, 9],  # Diagonal
        [3, 5, 7],
    ]

    def __init__(self, players):
        self.players = players
        self.board = [0 for i in range(9)]
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        return [i + 1 for i, e in enumerate(self.board) if e == 0]  # Tiles remain on the board

    def make_move(self, move):
        self.board[int(move) - 1] = self.current_player  # Tile selected is X or O depend on whose playing

    def unmake_move(self, move):  # Optional method (speeds up the AI)
        self.board[int(move) - 1] = 0

    def lose(self, who=None):
        """ Has the opponent three in line? """
        if who is None:
            who = self.opponent_index
        wins = [all([(self.board[c - 1] == who) for c in line]) for line in self.WIN_LINES]
        return any(wins)

    def is_over(self):
        return (
            (self.possible_moves() == [])
            or self.lose()
            or self.lose(who=self.current_player)
        )

    def show(self):
        print(
            "\n"
            + "\n".join(
                [
                    " ".join([[".", "O", "X"][self.board[3 * j + i]] for i in range(3)])
                    for j in range(3)
                ]
            )
        )

    def spot_string(self, i, j):
        return [" ", "O", "X"][self.board[3 * j + i]]

    def scoring(self):
        opp_won = self.lose()
        i_won = self.lose(who=self.current_player)
        if opp_won and not i_won:
            return -1
        if i_won and not opp_won:
            return 1
        return 0

    def winner(self):
        if self.lose(who=2):
            current_user.score.ctic_tac_toe += 1
            return "Computer Wins"
        elif self.lose(who=1):
            current_user.score.tic_tac_toe += 1
            return f"{current_user.username} Wins"
        return "It's a Tie"
