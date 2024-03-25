import random

# GLOBAL VARIABLES

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# FUNCTIONS

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                new_card = Card(suit,rank)
                self.all_cards.append(new_card)

    def shuffle(self):
        random.shuffle(self.all_cards)
    
    def deal(self):
        return self.all_cards.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1
            self.adjust_for_ace()
        
    def adjust_for_ace(self):
        while self.aces > 0 and self.value > 21:
            self.value -= 10  # Treat one ace as 1 instead of 11
            self.aces -= 1
        
    
class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        try:
            bet = int(input(f'You have {chips.total} chips. Please place your bet: '))
            if bet > 0 and bet <= chips.total:
                break
            else:
                print('Please input a valid bet!')
                continue                
        except:
            print(f'You cant place that bet. You have {chips.total} chips.')
    chips.bet = bet

def hit(deck,hand):
    
    hand.add_card(deck.deal()) 


def show_some(player,dealer):
    
    print(f'\nDEALER:\n{dealer.cards[0]} | HIDDEN\n\nPLAYER:\n', end='')
    for card in player.cards:
        print(f'{card} | ', end='')
    print(f'\nVALUE - {player.value}')
    
    
def show_all(player,dealer):

    print('\nDEALER:')
    for card in dealer.cards:
        print(f'{card} | ', end='')
    print(f'\nVALUE - {dealer.value}')

    print('\nPLAYER:')
    for card in player.cards:
        print(f'{card} | ', end='')
    print(f'\nVALUE - {player.value}')

def player_busts(player):
    if player.value > 21:
        return True
    return False

def dealer_busts(dealer):
    if dealer.value > 21:
        return True
    return False

def player_wins(player,dealer):
    if player.value > dealer.value and player.value <= 21 and dealer.value <= 21:
        return True
    return False
    
def dealer_wins(player,dealer):
    if player.value < dealer.value and player.value <= 21 and dealer.value <= 21:
        return True
    return False
    
def push(player,dealer):
    if player.value == dealer.value:
        return True
    return False


# GAME LOGIC

# Set up the Player's chips
player_chips = Chips()

while True:
    # Print an opening statement
    print('Welcome to BLACKJACK!!!\n')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    playing = True

    for x in range(2):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
   
    # Prompt the Player for their bet
    if player_chips.total > 0:
        take_bet(player_chips)
    else: 
        print('You have insufficient balance!')
        break
    
    # Show cards (but keep one dealer card hidden)
    show_some(player,dealer)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        action = ''
        while action != 'H' and action != 'S':
            action = input('\nDo you wish to hit or stand? (H or S): ')

        if action == 'H':
            hit(deck,player)
            show_some(player,dealer)     
            if player_busts(player):
                print(f'\nALAS!! YOU BUSTED. YOU LOSE {player_chips.bet} chips.')
                player_chips.lose_bet()
                break   
        else:
            playing = False
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if not player_busts(player):
        # Show all cards
        show_all(player,dealer)  
        while dealer.value < 17:
            print('\nDEALER hits again!')
            hit(deck,dealer)
            show_all(player,dealer)  
            if dealer_busts(dealer):
                print(f'\nHOORAY!! DEALER BUSTED. YOU WIN {player_chips.bet} chips.')
                player_chips.win_bet()      
    
    # Run different winning scenarios
    if player_wins(player,dealer):
        print(f'\nHOORAY!! YOU WIN {player_chips.bet} chips.')
        player_chips.win_bet()
    
    if dealer_wins(player,dealer):
        print(f'\nALAS!! YOU LOSE {player_chips.bet} chips.')
        player_chips.lose_bet()
    
    if push(player,dealer):
        print(f"\nIT'S A DRAW!!")
                      
    # Inform Player of their chips total 
    print(f'\nTotal Chips: {player_chips.total}')  

    # Ask to play again
    play_again = ''
    while play_again != 'Y' and play_again != 'N':
        play_again = input('\nDo you want to play again? (Y or N): ')   
    if play_again == 'Y':
        continue
    else:
        break