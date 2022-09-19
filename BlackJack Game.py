import random

#store the suits, ranks, and values of each card as arrays
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

# In[3]:

# Card class
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

# In[4]:

# Deck Class 
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        return '\n'.join(str(card) for card in self.deck)
    
    # shuffle cards in deck
    def shuffle(self):
        random.shuffle(self.deck)
    
    # deal a card from the deck
    def deal(self):
        return self.deck.pop(0)

# In[5]:

# Class to keep track of players hand
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    # add card to players hand
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    # check to see if player has an ace in their hand
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
         
# In[6]:

# Class to keep track of players chips
class Chips:
    
    def __init__(self,total = 100):
        self.total = total # This can be set to a default value or supplied by a user input
        self.bet = 0
    
    # adds bet to chips if player wins
    def win_bet(self):
        self.total += self.bet
    
    # takes away bet from chips if players loses
    def lose_bet(self):
        self.total -= self.bet

# In[7]:

# takes a bet from the player 
def take_bet(chips):  
   while True:
        try:
            chips.bet = int(input("Please enter your bet: "))
            print("\n")
        except:
            print("Your bet must be an integer")
            continue
        else:
            if chips.total < chips.bet:
                print(f"Your bet cannot exceed {chips.total}")
            else:
                break
        
# In[8]:

# adds a card to players hand if they hit
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# In[9]:

# prompts player to hit or stand
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    choice = input("Would you like to hit or stand? ")
    print('\n')
    
    if choice == 'hit':
        hit(deck,hand)
    else:
        print('Player stands, dealer is playing')
        print('\n')
        playing = False

# In[10]:

# functions to show player's and dealer's hands

def show_some(player,dealer):
    print("Dealers Hand:")
    print("(card hidden)")
    print(dealer.cards[1])
    
    print('\n')
    
    print("Player's Hand:")
    for card in player.cards:
        print(card)
    
    print('\n')
    
def show_all(player,dealer):
    print("Dealer's Hand:")
    for card in dealer.cards:
        print(card)
    print(f"Dealers's value: {dealer.value}")
    
    print('\n')
        
    print("Player's Hand:")
    for card in player.cards:
        print(card)
    print(f"Player's value: {player.value}")
         
# In[11]:

# functions to handle scenarioes in which the game ends

def player_busts(player,dealer,chips):
    print("Player Busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player Wins!")
    chips.win_bet()
        
def dealer_busts(player,dealer,chips):
    print("Dealer Busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer Wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")

# In[12]:

# game logic:

while True:
    # print an opening statement
    print('\nWelcome to BlackJack! Get as close to 21 as you can without going over!\nDealer hits until she reaches 17. Aces count as 1 or 11.\n')
    
    # create & shuffle the deck, deal two cards to each player
    gamedeck = Deck()
    gamedeck.shuffle()
    
    dealer = Hand()
    player = Hand()
    
    dealer.add_card(gamedeck.deal())
    player.add_card(gamedeck.deal())
    dealer.add_card(gamedeck.deal())
    player.add_card(gamedeck.deal())
        
    # set up the player's chips
    
    chips = Chips()
    
    # prompt the player for their bet
    take_bet(chips)

    # show cards (but keep one dealer card hidden)
    show_some(player,dealer)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # prompt for player to hit or stand
        hit_or_stand(gamedeck,player)
        
        # show cards (but keep one dealer card hidden)
        show_some(player,dealer)
        
        # if player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(player,dealer,chips)
            break

    # if Player hasn't busted, play dealer's hand until dealer reaches 17
    if player.value <= 21:
        
        while dealer.value < 17:
            hit(gamedeck,dealer)
    
        # show all cards
        show_all(player,dealer)
    
        # run different winning scenarios
        if dealer.value > 21:
            dealer_busts(player,dealer,chips)
        elif player.value > dealer.value:
            player_wins(player,dealer,chips)
        elif player.value < dealer.value:
            dealer_wins(player,dealer,chips)
        elif player.value == dealer.value:
            push(player,dealer)
    
    # inform Player of their chips total
    print(f'\nYour chip total is now: {chips.total}')
    
    # ask to play again
    replay = input("Would you like to play again? Enter y or n: ")
    if replay[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing!")
        break
