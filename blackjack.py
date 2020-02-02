import random

suits=('Hearts','Diamonds','Spades','Clubs')

ranks=('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')

values={'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

playing=True

class Card():
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        
    def __str__(self):
        return self.rank + " of " +self.suit
    
class Deck():
    def __init__(self):
        self.deck=[]
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_comp=''
        for card in self.deck:
            deck_comp+='\n'+card.__str__()
        return 'The deck has: '+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card=self.deck.pop();
        return single_card

class Hand():
    
    def __init__(self):
        self.cards=[]
        self.value=0
        self.aces=0 
    
    def add_card(self,card):
        self.cards.append(card)
        self.value+=values[card.rank]
        
        #track aces
        if card.rank=='Ace':
            self.aces+=1
            
    def got_aces(self):
        while self.value>21 and self.aces:
            self.value-=10
            self.aces-=1

class chips():
    
    def __init__(self,total=100):
        self.total=total
        self.bet=0

    def win_bet(self):
        self.total+=self.bet
        
    def lose_bet(self):
        self.total-=self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet=int(input('How much would you like to place: '))
        except:
            print('Please provide an integer')
        else:
            if chips.bet>chips.total:
                print(f'You have only {chips.total} chips')
            else:
                break
            
def hit(deck,hand):
    single_card=deck.deal()
    hand.add_card(single_card)
    hand.got_aces()
    
def hit_or_stand(deck,hand):
    global playing
    while True:
        x=input('Hit or Stand? enter h or s:')
        if x[0].lower()=='h':
            hit(deck,hand)
        elif x[0].lower()=='s':
            print('Player wants to stand..Dealer turn')
            playing=False
        else:
            print('Invalid Input!')
            continue
        break

def show_some(player,dealer):
    print('\n Dealers Hand: ')
    print('<Card Hidden>')
    print('',dealer.cards[1])
    print('\n Players Hand: ',*player.cards,sep='\n')

    
def show_all(player,dealer):
    print('\n Dealers Hand: ',*dealer.cards,sep='\n')
    print('Dealers Hand= ',dealer.value)
    print('\n Players Hand: ',*player.cards,sep='\n')
    print('Players Hand= ',player.value)

def player_lose(player,dealer,chips):
    print('Player Busted!!!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player Win!!!')
    chips.win_bet()
    
def dealer_lose(player,dealer,chips):
    print('Dealer Busted!!!')
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print('Dealer Win!!!')
    chips.lose_bet()

def push(player,dealer):
    print('Its a tie')


t=100
while True:
    print ('Welcome to the Club')
    
    deck=Deck()
    deck.shuffle()
    
    player_hand=Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    player_hand.got_aces()

    dealer_hand=Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.got_aces()
    
    #setup player chips
    player_chips = chips(t)
    #ask for bet
    take_bet(player_chips)
    #show cards
    show_some(player_hand,dealer_hand)
    
    while playing:
        if(player_hand.value==21 and dealer_hand.value==21):
            push(player_hand,dealer_hand)
            break
        elif player_hand.value==21:
            player_wins(player_hand,dealer_hand,player_chips)
            break
        elif dealer_hand.value==21:
            dealer_wins(player_hand,dealer_hand,player_chips)
            break
        else:
            hit_or_stand(deck,player_hand)
            show_some(player_hand,dealer_hand)
            
            # Criteria for 21 num check
            if player_hand.value > 21:
                player_lose(player_hand,dealer_hand,player_chips)
                break
    if(playing==False):
        while(dealer_hand.value<17):
            hit(deck,dealer_hand)
    
        # show all cards
        show_all(player_hand,dealer_hand)

        if dealer_hand.value>21:
            dealer_lose(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value==21 or dealer_hand.value>player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value<player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
        
    print(f"\nPlayer total chips are { player_chips.total }")

    #Ask the player to play again
    t=player_chips.total
    new_game=input('Would you like to play[y/n]:')
    if new_game[0].lower()=='y' and t!=0:
        playing =True
        continue
    else:
        print('Thanks for playing')
        break