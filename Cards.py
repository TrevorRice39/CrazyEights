import random

class Card:

        def __init__(self, rank, suit):
            self.rank = rank # rank of card
            self.suit = suit # suit of card

            # unique id for a card
            self.id = "{0}{1}".format(self.rank, self.suit)

        def __str__(self):
            # printing the card
            return "{0} of {1}".format(self.rank, self.suit)

            
class Deck:
    # the four suits
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]

    # ranks of our cards
    rank_names = ["Ace", "One", "Two", "Three",
                  "Four", "Five", "Six", "Seven",
                  "Eight", "Nine", "Ten", "Jack",
                  "Queen", "King"]
            
    def __init__(self):
        # dictionary of all cards {card id -> card)
        self.deck_dict = {card.id:card for card in self.getDeck()}

        # list of shuffled card ids
        self.deck = [cardId for cardId in self.deck_dict]
        random.shuffle(self.deck)
        self.size = len(self.deck)

    def getDeck(self):
        for rank in self.rank_names:
            for suit in self.suits:
                yield Card(rank, suit) # yields all the combinations of cards
    def getTop(self):
        return self.deck_dict[self.deck[-1]]

    def removeTop(self):
        return self.deck_dict[self.deck.pop()]

class Hand:

    def __init__(self, player_number):
        self.cards = []
        self.size = 0
        self.player_number = player_number

    def __str__(self):
        hand_str = "Player {0}'s hand: ".format(self.player_number)
        for card in self.cards:
            hand_str += str(card) + ", "

        return hand_str[0 : -2]
    def addCard(self, card):
        self.cards.append(card)
        self.size += 1
    
    def removeCard(self, position):
        self.cards.pop(position)
        self.size -= 1
