from app.routes import current_user
from random import choice


class Blackjack:

    def __init__(self):
        self.msg = "Lets play a round"
        self.blackjack = False
        self.sum = 0

        self.cards = [str(num) + shape for num in range(1, 13) for shape in ['h', 'd', 's', 'c']]
        self.hand = [self.get_card(), self.get_card()]
        self.sum = sum([x[1] for x in self.hand])

    def get_card(self):
        card = choice(self.cards)
        card_num = int(card[0])
        self.cards.remove(card)

        if card_num > 10:
            return card, 10
        elif card_num == 1 and self.sum < 11:
            return card, 11
        else:
            return card, card_num

    def game_alive(self):
        if self.sum <= 20:
            self.msg = "Do you want to draw a new card?"
            return True
        elif self.sum == 21:
            self.msg = "You've got Blackjack!"
            self.blackjack = True
            return False
        else:
            self.msg = "You're out of the game!"
            return False

    def new_card(self):
        # if self.game_alive():
        card = self.get_card()
        self.sum += card[1]
        self.hand.append(card)
