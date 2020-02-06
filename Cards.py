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
        # empty deck for discard pile
        self.deck_dict = dict()
        self.deck = list()
        self.size = 0

    # create a deck of 52 cards
    def getDeck(self):
        for rank in self.rank_names:
            for suit in self.suits:
                yield Card(rank, suit) # yields all the combinations of cards

    # return top card without removing it
    def peekTop(self):
        return self.deck_dict[self.deck[-1]]

    # remove and return top card
    def removeTop(self):
        self.size -= 1 # lower card size by 1
        return self.deck_dict[self.deck.pop()]

    # add a card to the deck
    def addCard(self, card):
        # add the card to the dictionary
        self.deck_dict[card.id] = card
        # append it to our deck
        self.deck.append(card.id)
        # increase size by 1
        self.size += 1

# class for a hand of cards for each player
class Hand:

    def __init__(self, player_number):
        # list of cards in hand
        self.cards = []
        # size of hand
        self.size = 0
        # setting the player number
        self.player_number = player_number

    # overriding __str__ method to show player's current hand
    def __str__(self):
        hand_str = "Your hand: "
        for index, card in enumerate(self.cards):
            hand_str += str(card) + "({0}), ".format(index) # card seperated by , and space
        return hand_str[0: -2] # remove the last comma and space

    # add card to hand
    def addCard(self, card):
        # append the card to the cards list
        self.cards.append(card)
        # increase size by 1
        self.size += 1

    # remove a card from a given position
    def removeCard(self, position):
        # remove card
        self.cards.pop(position)
        # decrease size
        self.size -= 1

    # return but dont' remove card at index
    def getCard(self, index):
        # return card
        return self.cards[index]

# the core of the game
class Game:

    # initialize scores to 0 and start a new round
    def __init__(self):
        self.player1Score = 0
        self.player2Score = 0

        self.newGame()

    # resets the score
    def resetScore(self):
        self.player1Score = 0
        self.player2Score = 0

    # sets up a new round
    def newGame(self):

        # make the deck for the game
        self.deck = Deck()

        self.discard = Deck()  # discard pile
        self.discard.newEmptyDeck()  # empty deck

        # create the players
        self.player1 = Hand(1)
        self.player2 = Hand(2)

    # start the game
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
        ret = "1i" # meaning player 1 invalid
        if playerNumber == 1: # if player 1 is moving
            if cardIndex == "d": # if they want to draw
                newCard = None # temp card
                if self.deck.size > 0: # make sure deck has cards
                    newCard = self.deck.removeTop() # get the top of the deck
                    # keep drawing until a playable card is drawn
                    while newCard.rank != "Eight" and newCard.suit != self.currentSuit and newCard.rank != self.discard.peekTop().rank and self.deck.size > 0:
                        self.player1.addCard(newCard) # add card to player 1's hand
                        newCard = self.deck.removeTop() # remove it from deck
                    if newCard is not None: # add the last card if it is there
                        self.player1.addCard(newCard)
                self.turn = 1 # player 1 goes again
                ret = "1v"
            else:
                self.turn = 2 # player 2 will go again
                card = self.player1.getCard(cardIndex) # get the card they are playing
                if card.rank == "Eight": # is it an eight?
                    # remove it
                    self.player1.removeCard(cardIndex)
                    # add card to discard
                    self.discard.addCard(card)
                    # replace suit with new suit
                    self.currentSuit = newSuit
                    ret = "1v" # player 1 valid move
                elif card.suit == self.currentSuit: # does the played card match the current suit
                    # remove card from hand
                    self.player1.removeCard(cardIndex)
                    # add it to discard
                    self.discard.addCard(card)
                    ret = "1v" # player 1 valid move
                elif card.rank == self.discard.peekTop().rank: # does played card match current rank
                    # remove card from hand
                    self.player1.removeCard(cardIndex)
                    # add it to discard
                    self.discard.addCard(card)
                    # set the suit to the card just played
                    self.currentSuit = card.suit
                    ret = "1v" # player 1 valid move
                else: # must be an invalid move
                    self.turn = 1 # player one goes again
                    ret = "1i" # 1 invalid move
        else: # same as player 1
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

        # if the deck is zero, put discard cards into deck
        if self.deck.size == 0:
            # grab all but top and put it in the deck
            self.deck.deck = self.discard.deck[0 : -1]
            # only leave the top card in discard
            self.discard.cards = self.discard.deck[-1]
        # if player 1 made invalid move
        if ret == "1i":
            return (False, "p1i")
        elif ret == "2i": # player 2 invalid
            return (False, "p2i")
        elif ret == "1v" and self.player1.size == 0: # player 1 win
            self.calculateScore("p1") # calculate score
            return (True, "p1w")
        elif ret == "2v" and self.player2.size == 0: # player 2 win
            self.calculateScore("p2") # calculate score
            return (True, "p2w")
        else: # valid move, no wins
            return (True, "pv")

    # calculates the score based on a given winner
    def calculateScore(self, winner):

        # make a Rank:Score dictionary
        rank_names = ["Ace", "Two", "Three",
                      "Four", "Five", "Six", "Seven",
                      "Eight", "Nine", "Ten", "Jack",
                      "Queen", "King"]
        score_dict = dict()
        for i in range(0, 10):
            score_dict[rank_names[i]] = i + 1
        score_dict["Eight"] = 50
        score_dict["Jack"] = 10
        score_dict["Queen"] = 10
        score_dict["King"] = 10

        # if p1 wins add points
        if winner == "p1":
            for card in self.player2.cards: # for all cards in p2's hand
                self.player1Score += score_dict[card.rank] # add points to player 1 score
        else: # if p2 wins add points
            for card in self.player1.cards: # for card in p1's hand
                self.player2Score += score_dict[card.rank] # add points to player 2 score

