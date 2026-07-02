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


# ---------- Difficulty Modes ----------
def get_difficulty_settings(choice):
    """Return (max_val, max_attempts, name) for selected difficulty level."""
    if choice == "1":
        return 50, 10, "Easy"
    elif choice == "3":
        return 500, 5, "Hard"
    else:
        return 100, 7, "Medium"


def play_difficulty_game():
    """Play a guessing game with a selected difficulty and attempt limits."""
    print("\n   Select Difficulty Level:")
    print("      1. Easy (Range: 1-50, Max attempts: 10)")
    print("      2. Medium (Range: 1-100, Max attempts: 7)")
    print("      3. Hard (Range: 1-500, Max attempts: 5)")
    choice = input("      Choose difficulty (1-3): ").strip()
    
    max_val, max_attempts, diff_name = get_difficulty_settings(choice)
    target = random.randint(1, max_val)
    attempts = 0
    
    print(f"\n   🎮 Playing {diff_name} Mode! You have {max_attempts} attempts.")
    
    while attempts < max_attempts:
        try:
            remaining = max_attempts - attempts
            guess_str = input(f"      [{remaining} left] Enter guess (1-{max_val}): ").strip()
            if not guess_str:
                continue
            guess = int(guess_str)
            
            if not (1 <= guess <= max_val):
                print(f"      ⚠️  Please enter a number between 1 and {max_val}.")
                continue
                
            attempts += 1
            if guess < target:
                print("      🔺 Too low!")
            elif guess > target:
                print("      🔻 Too high!")
            else:
                print(f"      🎉 Correct! You won in {attempts} attempts!")
                return True
        except ValueError:
            print("      ❌ Please enter a valid integer.")
            
    print(f"      💀 Game Over! You ran out of attempts. The number was {target}.")
    return False


# ---------- Temperature Hints & Proximity ----------
def get_temperature_hint(guess, target):
    """Return a descriptive hot/cold indicator based on closeness to target."""
    diff = abs(guess - target)
    if diff == 0:
        return "🎉 Correct!"
    elif diff <= 3:
        return "🥵 Burning Hot!"
    elif diff <= 7:
        return "☀️ Warm!"
    elif diff <= 15:
        return "❄️ Cool!"
    else:
        return "🧊 Ice Cold!"


def play_advanced_game():
    """Play a guessing game with higher/lower hints and Hot/Cold proximity feedback."""
    target = random.randint(1, 100)
    attempts = 0
    max_attempts = 8
    print(f"\n   🎮 Playing Proximity Guess Game (Range: 1-100, Max attempts: {max_attempts})")
    
    while attempts < max_attempts:
        try:
            remaining = max_attempts - attempts
            guess_str = input(f"      [{remaining} left] Enter guess: ").strip()
            if not guess_str:
                continue
            guess = int(guess_str)
            
            if not (1 <= guess <= 100):
                print("      ⚠️  Please enter a number between 1 and 100.")
                continue
                
            attempts += 1
            hint = get_temperature_hint(guess, target)
            
            if guess == target:
                print(f"      🎉 Correct! You won in {attempts} attempts. Closeness: {hint}")
                return True
                
            direction = "Higher 🔺" if guess < target else "Lower 🔻"
            print(f"      Feedback: {direction} | Closeness: {hint}")
        except ValueError:
            print("      ❌ Please enter a valid integer.")
            
    print(f"      💀 Game Over! The correct number was {target}.")
    return False



def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 12: GUESS GAME")
    print("=" * 50)
    print()

    print(">>> Basic Guess Game Demo <<<")
    # For testing, we can run the difficulty mode.
    play_difficulty_game()


if __name__ == "__main__":
    main()
