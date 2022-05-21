from app import db

from app.routes import current_user
from random import choice


class Blackjack:

    def __init__(self):
        self.msg = "Lets play a round"
        self.cards = [[num, str(num) + shape] for num in range(1, 13) for shape in ['H', 'D', 'S', 'C']]
        self.back = choice(['red', 'blue', 'gray', 'purple', 'yellow', 'green'])
        self.cover = True

        self.p_hand = []
        self.p_aces = []
        self.new_card(self.p_hand, self.p_aces)
        self.new_card(self.p_hand, self.p_aces)
        self.p_sum = self.check_sum(self.p_hand, self.p_aces)
        self.p_game_alive = self.game_alive(self.p_sum)

        self.c_hand = []
        self.c_aces = []
        self.new_card(self.c_hand, self.c_aces)
        self.new_card(self.c_hand, self.c_aces)
        self.c_sum = self.check_sum(self.c_hand, self.c_aces)
        self.c_game_alive = self.game_alive(self.c_sum)

    @staticmethod
    def check_sum(hand, aces):
        cards_sum = sum([x[0] for x in hand])
        if cards_sum == 21:
            return cards_sum

        # Turn aces from 11 to 1 if sum of cards are higher than 21
        aces_in_hand = [hand[x] for x in aces]  # get the aces from the hand
        while cards_sum > 21 and any(
                [x[0] == 11 for x in aces_in_hand]):  # while higher than 21 and there are any 11 aces
            for index in aces:
                if cards_sum > 21 and hand[index][0] == 11:  # the values of the aces in the hand is changing
                    hand[index][0] = 1
                    cards_sum = sum([x[0] for x in hand])  # and also the sum
                    aces_in_hand = [hand[x] for x in aces]  # and the aces list
        return cards_sum

    @staticmethod
    def game_alive(cards_sum):
        if cards_sum <= 20:
            msg = "can draw"
            game = True
            blackjack = False
        elif cards_sum == 21:
            msg = "blackjack"
            game = False
            blackjack = True
        else:
            msg = "out"
            game = False
            blackjack = False
        return [game, blackjack, msg]

    def get_card(self, cards_sum):
        is_ace = False
        card = choice(self.cards)
        self.cards.remove(card)

        if card[0] > 10:
            card[0] = 10
        elif card[0] == 1 and cards_sum < 11:
            card[0] = 11
            is_ace = True
        return card, is_ace

    def new_card(self, hand, aces, cards_sum=0):
        card = self.get_card(cards_sum)
        hand.append(card[0])
        if card[1]:
            aces.append(len(hand) - 1)
        cards_sum = self.check_sum(hand, aces)
        game_alive = self.game_alive(cards_sum)
        return cards_sum, game_alive

    def computer_ai(self):
        if self.p_sum > self.c_sum:
            while self.c_sum < 16 and self.c_game_alive[0]:
                self.c_sum, self.c_game_alive = self.new_card(self.c_hand, self.c_aces, self.c_sum)
        return False

    def open_cards(self, wager):
        self.computer_ai()

        if any(self.p_game_alive[0:2]) and any(self.c_game_alive[0:2]):
            print('simple')
            if self.p_sum > self.c_sum:
                self.msg = f'{current_user.username} Win!'
                if self.p_game_alive[1]:
                    current_user.score.blackjack += wager * 2
                else:
                    current_user.score.blackjack += wager

            elif self.p_sum < self.c_sum:
                self.msg = 'Dealer Win!'
                current_user.score.blackjack -= wager
            else:
                self.msg = "It's a Tie!"

        elif any(self.p_game_alive[0:2]) and not any(self.c_game_alive[0:2]):
            print('c_burned')
            self.msg = f'{current_user.username} Win!'
            if self.p_game_alive[1]:
                current_user.score.blackjack += wager * 2
            else:
                current_user.score.blackjack += wager

        elif not any(self.p_game_alive[0:2]) and any(self.c_game_alive[0:2]):
            print('p_burned')
            self.msg = 'Dealer Win!'
            current_user.score.blackjack -= wager

        else:
            self.msg = "It's a Tie!"

        if current_user.score.blackjack <= 0:
            current_user.score.blackjack = 1000
            self.msg = "Here's a $1000 for a fresh start"

        db.session.commit()
        self.p_game_alive[0] = False
