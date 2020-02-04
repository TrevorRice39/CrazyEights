import random
from random import randint

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
    rank_names = ["Ace", "Two", "Three",
                  "Four", "Five", "Six", "Seven",
                  "Eight", "Nine", "Ten", "Jack",
                  "Queen", "King"]
            
    def __init__(self):
        self.newDeck()
        
    def newDeck(self):
        # dictionary of all cards {card id -> card)
        self.deck_dict = {card.id:card for card in self.getDeck()}

        # list of shuffled card ids
        self.deck = [cardId for cardId in self.deck_dict]
        random.shuffle(self.deck)
        self.size = len(self.deck)

    def newEmptyDeck(self):
        self.deck_dict = dict()
        self.deck = list()
        self.size = 0

    def getDeck(self):
        for rank in self.rank_names:
            for suit in self.suits:
                yield Card(rank, suit) # yields all the combinations of cards
    def peekTop(self):
        return self.deck_dict[self.deck[-1]]

    def removeTop(self):
        self.size -= 1
        return self.deck_dict[self.deck.pop()]
        

    def addCard(self, card):
        self.deck_dict[card.id]  = card
        self.deck.append(card.id)
        self.size += 1

class Hand:

    def __init__(self, player_number):
        self.cards = []
        self.size = 0
        self.player_number = player_number

    def __str__(self):
        hand_str = "Your hand: ".format(self.player_number)
        for index, card in enumerate(self.cards):
            hand_str += str(card) + "({0}), ".format(index)

        return hand_str[0 : -2]
    def addCard(self, card):
        self.cards.append(card)
        self.size += 1
    
    def removeCard(self, position):
        self.cards.pop(position)
        self.size -= 1

    def getCard(self, index):
        return self.cards[index]

class Game:

    def __init__(self):
        self.player1Score = 0
        self.player2Score = 0

        self.newGame()

    def newGame(self):
        self.deck = Deck()
        # make the deck for the game
        self.deck = Deck()

        self.discard = Deck()  # discard pile
        self.discard.newEmptyDeck()  # empty deck

        # create the players
        self.player1 = Hand(1)
        self.player2 = Hand(2)

    def startGame(self):
        self.dealInitialHands() # deal the initial hands to the 2 players

        self.turn = randint(1, 2) # randomly choose player 1 or 2 to go first

        self.currentSuit = self.deck.peekTop().suit # get the suit of the top of the pile

        self.discard.addCard(self.deck.removeTop())

    def dealInitialHands(self):

        # deal each card one at a time to each player
        # each player gets a total of 5 cards
        self.player1.addCard(self.deck.removeTop())
        self.player2.addCard(self.deck.removeTop())
        self.player1.addCard(self.deck.removeTop())
        self.player2.addCard(self.deck.removeTop())
        self.player1.addCard(self.deck.removeTop())
        self.player2.addCard(self.deck.removeTop())
        self.player1.addCard(self.deck.removeTop())
        self.player2.addCard(self.deck.removeTop())
        self.player1.addCard(self.deck.removeTop())
        self.player2.addCard(self.deck.removeTop())

        if self.deck.peekTop().rank == "Eight": # restart the game if an eight is at the top
            self = Game()

    # player number signifies which player is moving
    # card is their move
    # newSuit must be specified if they play an eight
    def makeMove(self, playerNumber, cardIndex, newSuit):
        ret = "1i"
        if playerNumber == 1:
            if cardIndex == "d":
                newCard = None
                if self.deck.size > 0:
                    newCard = self.deck.removeTop()
                    while  newCard.suit != self.currentSuit and newCard.rank != self.discard.peekTop().rank and self.deck.size > 0:
                        self.player1.addCard(newCard)
                        newCard = self.deck.removeTop()
                    if newCard is not None:
                        self.player1.addCard(newCard)
                self.turn = 1
                ret = "1v"
            else:
                self.turn = 2
                card = self.player1.getCard(cardIndex)
                print(card)
                if card.rank == "Eight":
                    self.player1.removeCard(cardIndex)
                    self.discard.addCard(card)
                    self.currentSuit = newSuit
                    ret = "1v"
                elif card.suit == self.currentSuit:
                    self.player1.removeCard(cardIndex)
                    self.discard.addCard(card)
                    ret = "1v"
                elif card.rank == self.discard.peekTop().rank:
                    self.player1.removeCard(cardIndex)
                    self.discard.addCard(card)
                    self.currentSuit = card.suit
                    ret = "1v"
                else:
                    self.turn = 1
                    ret = "1i"
        else:
            if cardIndex == "d":
                newCard = None
                if self.deck.size > 0:
                    newCard = self.deck.removeTop()
                    while newCard.suit != self.currentSuit and newCard.rank != self.discard.peekTop().rank and self.deck.size > 0:
                        self.player2.addCard(newCard)
                        newCard = self.deck.removeTop()
                    self.player2.addCard(newCard)    
                self.turn = 2
                ret = "2v"
            else:
                self.turn = 1
                card = self.player2.getCard(cardIndex)
                print(card)
                if card.rank == "Eight":
                    self.player2.removeCard(cardIndex)
                    self.discard.addCard(card)
                    self.currentSuit = newSuit
                    ret = "2v"
                elif card.suit == self.currentSuit:
                    self.player2.removeCard(cardIndex)
                    self.discard.addCard(card)
                    ret = "2v"
                elif card.rank == self.discard.peekTop().rank:
                    self.player2.removeCard(cardIndex)
                    self.discard.addCard(card)
                    self.currentSuit = card.suit
                    ret = "2v"

                else:
                    self.turn = 2
                    ret = "2i"
        if self.deck.size == 0:
            self.deck.deck = self.discard.deck[0 : -1]
            self.discard.cards = self.discard.deck[-1]
        if ret == "1i":
            return (False, "p1i")
        elif ret == "2i":
            return (False, "p2i")
        elif ret == "1v" and self.player1.size == 0:
            return (True, "p1w")
        elif ret == "2v" and self.player2.size == 0:
            return (True, "p2w")
        else:
            return (True, "pv")

        def calculateScore():
            pass
