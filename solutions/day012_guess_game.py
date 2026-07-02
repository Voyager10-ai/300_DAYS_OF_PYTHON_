# Day 12: Guess Game
#
# Problem:
#   Write a Python program that implements an interactive number guessing game.
#   - Single-player mode with varying difficulties (Easy, Medium, Hard)
#   - Interactive menu, score tracker, and bounds validation
#   - Dynamic hints (higher/lower and proximity/temperature hints)
#   - Local multiplayer mode (one player chooses, another guesses)
#   - Creative ASCII dashboard and progress visualizer
#
# This exercise covers standard imports (random), user inputs, loops, game state
# management, and ASCII visual styling.

import random


# ---------- Basic Single-Player Game ----------
def play_basic_game():
    """Play a simple guessing game with a random number between 1 and 100."""
    target = random.randint(1, 100)
    attempts = 0
    print("\n   🎮 Playing Basic Guess Game (Range: 1-100)")
    
    while True:
        try:
            guess_str = input("      Enter your guess: ").strip()
            if not guess_str:
                continue
            guess = int(guess_str)
            attempts += 1
            
            if guess < target:
                print("      🔺 Too low! Try a higher number.")
            elif guess > target:
                print("      🔻 Too high! Try a lower number.")
            else:
                print(f"      🎉 Correct! You found the number in {attempts} attempts.")
                break
        except ValueError:
            print("      ❌ Invalid input. Please enter a valid integer.")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 12: GUESS GAME")
    print("=" * 50)
    print()

    print(">>> Basic Guess Game Demo <<<")
    # For testing, we can simulate or let user play. We will add a menu in final commits.
    # We call play_basic_game() here for demonstration.
    play_basic_game()
