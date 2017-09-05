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
action = ""
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
        self.cards=[]

    def __str__(self):
        
        result = ""
        for card in self.cards:
            result += cstr(card)+ " "
        
        # return a string representation of a hand
        return "Hand contains " + result
        

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        has_aces = False
        
        for card in self.cards:
            rank = card.get_rank()
            if rank=='A':
                has_aces = True
            value += VALUES[card.get_rank()]
                
        if has_aces and value + 10 <= 21:
            value += 10
                
        return value
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas,pos)
            pos[0] += 75


class Deck:
    def __init__(self):
        self.deck = []

        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        for card in self.deck:
            result += str(i)+ " "

        return "Deck contains" + result


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score

    if in_play:
        outcome = "Player surrenders hand! Deal again?"
        score -= 1


    deck = Deck()
    outcome = ""
    action = "Hit or Stand?"
    in_play = True

    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    in_play = True

def hit():
    # replace with your code below
    global outcome, in_play, score
    
    # if the hand is in play, hit the player
    
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
    
            if player_hand.get_value() > 21:
                outcome = "You busted! Deal again?"
                in_play = False
                action = "Deal again?"
            
def stand():
    global outcome, score, in_play, action

    if in_play:
        if player_hand.get_value() <=21:
            while dealer_hand.get_value()< 17:
                dealer_hand.add_card(deck.deal_card())
    
        if dealer_hand.get_value() > 21:
            score += 1
            outcome = "Dealer busts!"
        elif dealer_hand.get_value () >= player_hand.get_value():
            score -= 1
            outcome = "Dealer wins"
        else:
            score +=1
            outcome = "Player wins!"
    
    in_play = False
    action = "New deal?"


        
            
# draw handler    
def draw(canvas):
    global outcome, in_play, card_back, card_loc, score

    canvas.draw_text("Blackjack", [100, 75], 100 ,"White")

    player_hand.draw(canvas, [100, 300])
    dealer_hand.draw(canvas, [100, 150])

    canvas.draw_text(outcome, [10, 500], 30 ,"White")
    canvas.draw_text(action, [10, 550], 30 ,"White")

    canvas.draw_text("Score: %s" % score, [400, 150], 40 ,"White")


    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136,199), CARD_BACK_SIZE)

#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])


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