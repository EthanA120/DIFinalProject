from app.routes import current_user
from random import choice


class Blackjack:

    def __init__(self):
        self.msg = "Lets play a round"
        self.blackjack = False
        self.hand = []
        self.aces = []
        self.sum = 0

        self.back = choice(['red', 'blue', 'gray', 'purple', 'yellow', 'green'])
        self.cards = [[num, str(num) + shape] for num in range(1, 13) for shape in ['H', 'D', 'S', 'C']]
        self.initial_hand = [self.new_card(), self.new_card()]

    def get_card(self):
        is_ace = False
        card = choice(self.cards)
        self.cards.remove(card)

        if card[0] > 10:
            card[0] = 10
        elif card[0] == 1 and self.sum < 11:
            card[0] = 11
            is_ace = True
        return card, is_ace

    def game_alive(self):
        # Turn aces from 11 to 1 if sum of cards are higher than 21
        aces = [self.hand[x] for x in self.aces]  # get the aces from the hand
        while self.sum > 21 and any([x[0] == 11 for x in aces]):  # while higher than 21 and there are any 11 aces
            for index in self.aces:
                if self.hand[index][0] == 11:
                    self.hand[index][0] = 1
                    self.sum = sum([x[0] for x in self.hand])  # the sum is changing
                    aces = [self.hand[x] for x in self.aces]  # and also the aces list

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
        card = self.get_card()
        self.hand.append(card[0])
        self.sum = sum([x[0] for x in self.hand])

        if card[1]:
            self.aces.append(len(self.hand) - 1)
        self.game_alive()
