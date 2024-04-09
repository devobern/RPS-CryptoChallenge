import hashlib
import random
import os
import time
import secrets

def collect_jitter_entropy(samples=1000):
    """Collect jitter entropy based on execution time variance."""
    deltas = []
    for _ in range(samples):
        start = time.perf_counter()
        # Executes a loop with a no-op 1000 times to measure execution time variance, 
        # leveraging system-level unpredictabilities as a source of entropy.
        for __ in range(1000):
            pass
        end = time.perf_counter()
        deltas.append(end - start)
    # Use the variance of execution time as a source of entropy
    entropy = float(sum(deltas)) / len(deltas) * 1000000  # Example conversion
    return entropy

def generate_nonce():
    """Generate a secure nonce using jitter entropy."""
    entropy = collect_jitter_entropy()
    random.seed(entropy)  # Seeding with collected entropy
    # Using secrets.token_hex for cryptographic purposes would be better, 
    # but cannot be seeded manually. For educational purposes, we use random (NOT SECURE!!!).
    #nonce = secrets.token_hex(64)  # Security Level 256 bits (64 * 4 = 256)
    nonce = ''.join(random.choices('0123456789abcdef', k=64))
    return nonce

def generate_commitment(choice, nonce):
    combined = choice + nonce
    # Using SHA3-256 here
    return hashlib.sha3_256(combined.encode()).hexdigest()

def verify_commitment(choice, nonce, commitment):
    combined = choice + nonce
    # Using SHA3-256 for verification
    return hashlib.sha3_256(combined.encode()).hexdigest() == commitment

def determine_winner(player1_choice, player2_choice):
    if player1_choice == player2_choice:
        return "It's a draw!"
    elif (player1_choice == "rock" and player2_choice == "scissors") or \
         (player1_choice == "paper" and player2_choice == "rock") or \
         (player1_choice == "scissors" and player2_choice == "paper"):
        return "Player 1 wins!"
    else:
        return "Player 2 wins!"

def is_valid_move(move):
    return move in ["rock", "paper", "scissors"]

def is_valid_nonce(nonce):
    return nonce.isdigit() and len(nonce) == 6
    
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

    
# Simulating the game
print("Welcome to Rock, Paper, Scissors!")

# Player 1
while True:
    player1_choice = input("Player 1, your move (rock, paper, scissors): ").lower()
    if not is_valid_move(player1_choice):
        print("Invalid move. Please choose rock, paper, or scissors.")
        continue

    break  # Break the loop if inputs are valid

print("Generating nonce for player 1...")
player1_nonce = generate_nonce()
print("Player 1, Nonce: ", player1_nonce)

input("Press any key to continue...")


player1_commitment = generate_commitment(player1_choice, player1_nonce)

# Clear console
clear_console()

print("Player 1, Commitment: ", player1_commitment)

# Player 2
while True:
    player2_choice = input("Player 2, your move (rock, paper, scissors): ").lower()
    if not is_valid_move(player2_choice):
        print("Invalid move. Please choose rock, paper, or scissors.")
        continue

    break  # Break the loop if inputs are valid

print("Generating nonce for player 2...")
player2_nonce = generate_nonce()
print("Player 2, Nonce: ", player2_nonce)


player2_commitment = generate_commitment(player2_choice, player2_nonce)

print("Player 2, Commitment: ", player2_commitment)

input("Press any key to continue...")

# Clear console
clear_console()

# Reveal the choices and nonces
print("Revealing the choices and nonces...")
print("Player 1, Commitment: ", player1_commitment)
print("Player 1, Nonce: ", player1_nonce)
print("Player 1, Choice: ", player1_choice)

print("Player 2, Commitment: ", player2_commitment)
print("Player 2, Nonce: ", player2_nonce)
print("Player 2, Choice: ", player2_choice)


# Verify the commitments
print("\nVerifying the commitments:")

fair_game = True

# Player 1 commitment verification
player1_commitment_c = input("Player 2, enter commitment from player 1: ")
player1_nonce_c = input("Player 2, enter nonce from player 1: ")
player1_choice_c = input("Player 2, enter choice from player 1: ")
if(verify_commitment(player1_choice_c, player1_nonce_c, player1_commitment_c)):
    print("Player 1 commitment verified: OK")
else:
    print("Player 1 commitment verification failed.")
    fair_game = False

# Player 2 commitment verification
player2_commitment_c = input("Player 1, enter commitment from player 2: ")
player2_nonce_c = input("Player 1, enter nonce from player 2: ")
player2_choice_c = input("Player 1, enter choice from player 2: ")
if(verify_commitment(player2_choice_c, player2_nonce_c, player2_commitment_c)):
    print("Player 2 commitment verified: OK")
else:
    print("Player 2 commitment verification failed.")
    fair_game = False

if fair_game:
    print(f"\nThe game is fair")
    # Determine the winner
    print("\nDetermining the winner...")
    print(determine_winner(player1_choice, player2_choice))
else:
    print(f"\nThe game is not fair")
