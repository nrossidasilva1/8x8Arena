# import the built-in random module
import random  # to use the shuffle function

#create the card deck
cards = ["MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT", "POWER_PILL", "TURBO"]
weights = [20, 20, 20, 20, 10, 10]

# function with return a random card
def draw_card():
    return random.choices(cards, weights = weights, k = 1)[0]

# function to retur x cards to build inicial deck with 4 cards
def draw_hand(size = 4):
    hand = []
    for _ in range(size):
        hand.append(draw_card())
    return hand 
    

# test the functions
if __name__=="__main__":
    print("Testing deck functions...")
    print(draw_card())
    print(draw_hand())
