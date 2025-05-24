import random
from collections import Counter

# Define rank and suit orders
RANK_ORDER = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'Black Joker', 'Red Joker']
SUIT_ORDER = ['C', 'D', 'H', 'S']  # Clubs, Diamonds, Hearts, Spades

# Create index maps for fast lookup
RANK_INDEX = {r: i for i, r in enumerate(RANK_ORDER)}
SUIT_INDEX = {s: i for i, s in enumerate(SUIT_ORDER)}

# Create and shuffle a full deck
def create_deck():
    deck = []
    for rank in RANK_ORDER[:-2]:  # Exclude Jokers for now
        for suit in SUIT_ORDER:
            deck.append(rank + suit)
    deck.append('Black Joker')
    deck.append('Red Joker')
    random.shuffle(deck)
    return deck

# Get rank index of a card
def rank_value(card):
    for rank in RANK_INDEX:
        if rank in card:
            return RANK_INDEX[rank]
    return -1

# Get suit index of a card
def suit_value(card):
    for suit in SUIT_INDEX:
        if suit in card:
            return SUIT_INDEX[suit]
    return -1

# Compare two cards by rank, then suit
def compare_cards(c1, c2):
    r1 = rank_value(c1)
    r2 = rank_value(c2)
    if r1 != r2:
        return r1 - r2
    return suit_value(c1) - suit_value(c2)

# Parse and validate user input
def parse_play(input_str, hand):
    if input_str.upper() == "PASS":
        return None
    cards = input_str.strip().split()
    for card in cards:
        if card not in hand:
            return None
    return cards

# Check if play is valid (only single or pair allowed)
def is_valid_play(play):
    if not play:
        return True
    if len(play) == 1:
        return True
    if len(play) == 2:
        return play[0][:-1] == play[1][:-1]
    return False

# Check if current play beats last play
def is_play_stronger(play, last_play):
    if not last_play:
        return True
    if len(play) != len(last_play):
        return False
    if len(play) == 1:
        return compare_cards(play[0], last_play[0]) > 0
    if len(play) == 2:
        return compare_cards(play[1], last_play[1]) > 0
    return False

# Bot chooses a valid play if available
def bot_play(bot_name, hand, last_play):
    card_counter = Counter(card[:-1] for card in hand if "Joker" not in card)
    sorted_hand = sorted(hand, key=lambda x: (rank_value(x), suit_value(x)))

    if not last_play or len(last_play) == 1:
        for card in sorted_hand:
            if not last_play or compare_cards(card, last_play[0]) > 0:
                print(f"{bot_name} plays: {card}")
                hand.remove(card)
                return [card]
    elif len(last_play) == 2:
        for rank, count in card_counter.items():
            if count >= 2:
                pair = []
                for card in sorted_hand:
                    if card.startswith(rank):
                        pair.append(card)
                        if len(pair) == 2:
                            break
                if len(pair) == 2 and compare_cards(pair[1], last_play[1]) > 0:
                    print(f"{bot_name} plays: {pair[0]} {pair[1]}")
                    hand.remove(pair[0])
                    hand.remove(pair[1])
                    return pair
    print(f"{bot_name} passes")
    return None

# Main game loop
def main():
    print("Welcome to the Card Game")

    deck = create_deck()
    p1 = deck[:20]       # You (landlord)
    p2 = deck[20:37]     # Bot A
    p3 = deck[37:54]     # Bot B

    players = [("You", p1), ("Bot A", p2), ("Bot B", p3)]

    # Sort each player's hand
    for i in range(3):
        name, hand = players[i]
        sorted_hand = sorted(hand, key=lambda x: (rank_value(x), suit_value(x)))
        players[i] = (name, sorted_hand)

    turn = 0
    last_play = None
    last_player = None
    pass_count = 0

    while True:
        name, hand = players[turn]
        print(f"\n{name}'s turn. Cards left: {len(hand)}")

        if name == "You":
            print("Your hand:", ' '.join(hand))
            while True:
                move_input = input("Enter card(s) to play (or PASS): ")
                move = parse_play(move_input, hand)

                if move_input.upper() == "PASS":
                    print("You passed")
                    pass_count += 1
                    move = None
                    break

                if move is None:
                    print("Invalid input. Please enter cards that are in your hand.")
                    continue

                if not is_valid_play(move):
                    print("Invalid combination. Only single cards or pairs are allowed.")
                    continue

                if not is_play_stronger(move, last_play):
                    print("Your play is not strong enough to beat the last play.")
                    continue

                for card in move:
                    hand.remove(card)
                last_play = move
                last_player = name
                pass_count = 0
                break
        else:
            move = bot_play(name, hand, last_play)
            if move:
                last_play = move
                last_player = name
                pass_count = 0
            else:
                pass_count += 1

        if not hand:
            print(f"\n{name} wins the game")
            break

        if pass_count >= 2:
            print(f"\nAll players passed. {last_player} plays again")
            last_play = None
            pass_count = 0
            for i in range(3):
                if players[i][0] == last_player:
                    turn = i
                    break
        else:
            turn = (turn + 1) % 3

if __name__ == "__main__":
    main()
