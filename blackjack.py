# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = list()

    def __str__(self):
        # return a string representation of a hand
        return "Your hand contains " + " ".join([str(i) for i in self.cards])

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        aces = 0
        for card in self.cards:
            rank = card.get_rank()
            value += VALUES.get(rank)
            if rank == "A":
                aces += 1
        value_10 = value + (10 * aces) - aces
        if value_10 <= 21:
            value = value_10
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self.cards:
            card.draw(canvas, (pos[0] + (30 * i), pos[1]))
            i += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = list()
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        return "Deck contains" + " ".join([str(i) for i in self.cards])



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score
    # your code goes here
    if in_play:
        score -= 1
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    for i in range(2):
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
    dealer.cards[-1].show = False
    in_play = True
    
def hit():
    # replace with your code below
    global outcome, in_play, score
    if not in_play:
        return
    # if the hand is in play, hit the player
    player.add_card(deck.deal_card())
    outcome = "Hit or Stand?"
    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() > 21:
        outcome = "Player busts. New deal?"
        in_play = False
        score -= 1
           
def stand():
    # replace with your code below
    global outcome, in_play, score
    if not in_play:
        return
    dealer.cards[-1].show = True
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())
    if dealer.get_value() > 21:
        score += 1
        outcome = "Dealer busts. New deal?"
    elif player.get_value() > dealer.get_value():
        score += 1
        outcome = "Player wins. New deal?"
    else:
        score -= 1
        outcome = "Dealer wins. New deal?"
    in_play = False
   
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Blackjack', (50, 200), 36, "Orange")
    canvas.draw_text(outcome, (300, 150), 16, "White")
    # draw score
    canvas.draw_text('Score = ' + str(score), (300, 200), 24, "White")
    
    pos = [100, 300]
    if in_play:
        card_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0],CARD_BACK_CENTER[1] + CARD_BACK_SIZE[1])  

    
    # draw hands
    dealer.draw(canvas, pos)
    player.draw(canvas, [pos[0], pos[1] + 100])
    

def mouse(position):
    HANDLERS = (deal, hit, stand)
    COORDS = (((40, 120), (280, 305)), ((40, 120), (315, 340)), ((130, 210), (315, 340)))
    
    i = 0
    for x, y in COORDS:
        if x[0] <= position[0] <= x[1] and y[0] <= position[1] <= y[1]:
            return HANDLERS[i]()
        i += 1


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric