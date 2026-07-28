# Day 26: Caesar Encryption
#
# Problem:
#   Write a Python program to perform Caesar cipher encryption and decryption.
#   - Encrypt plain text using a user-specified shift key.
#   - Decrypt cipher text using the matching shift key.
#   - Support custom alphabets, upper/lower preservation, and non-alphabetic character handling.
#   - Built-in ROT13 cipher implementation.
#   - Automated brute-force cracking and frequency analysis for keyless decryption.
#   - ASCII visualizer chart illustrating shift mapping and cipher wheel.
#   - Interactive CLI explorer with built-in test suites.
#
# This exercise covers string manipulation, ASCII indexing, modular arithmetic,
# cryptography fundamentals, frequency analysis, ASCII charts, and CLI interactions.

import string


def caesar_encrypt(plaintext, shift, alphabet=None):
    """
    Encrypt plaintext using Caesar cipher with specified shift key.
    Preserves uppercase/lowercase cases and leaves non-alphabet characters intact.
    Time Complexity: O(n), Space Complexity: O(n).
    """
    if alphabet is None:
        alphabet_lower = string.ascii_lowercase
        alphabet_upper = string.ascii_uppercase
    else:
        alphabet_lower = alphabet
        alphabet_upper = alphabet.upper()

    shifted_chars = []
    for char in plaintext:
        if char in alphabet_lower:
            idx = alphabet_lower.index(char)
            new_char = alphabet_lower[(idx + shift) % len(alphabet_lower)]
            shifted_chars.append(new_char)
        elif char in alphabet_upper:
            idx = alphabet_upper.index(char)
            new_char = alphabet_upper[(idx + shift) % len(alphabet_upper)]
            shifted_chars.append(new_char)
        else:
            shifted_chars.append(char)

    return "".join(shifted_chars)


def caesar_decrypt(ciphertext, shift, alphabet=None):
    """
    Decrypt ciphertext using Caesar cipher with specified shift key.
    Time Complexity: O(n), Space Complexity: O(n).
    """
    return caesar_encrypt(ciphertext, -shift, alphabet=alphabet)


def rot13(text):
    """
    Perform ROT13 cipher transformation on input text.
    Time Complexity: O(n), Space Complexity: O(n).
    """
    return caesar_encrypt(text, 13)


def crack_caesar(ciphertext):
    """
    Brute-force crack Caesar ciphertext using English letter frequency analysis.
    Scores each candidate shift (0..25) based on chi-squared / frequency match against English.
    Returns list of candidate decryptions sorted by likelihood (highest score first).
    """
    english_freqs = {
        'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
        'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
        'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
        'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
        'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,
        'z': 0.00074
    }

    candidates = []
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        score = 0.0
        for char in decrypted.lower():
            if char in english_freqs:
                score += english_freqs[char]
        candidates.append((score, shift, decrypted))

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates


def draw_shift_visualization(shift, sample_text="HELLOPYTHON"):
    """
    Render ASCII diagram illustrating Caesar shift mapping and sample transformation.
    """
    alpha = string.ascii_uppercase
    shifted_alpha = alpha[shift % 26:] + alpha[:shift % 26]

    print("\n   ┌" + "─" * 62 + "┐")
    print("   │" + f"🔒 CAESAR CIPHER SHIFT MAPPING (Shift = {shift})".center(62) + "│")
    print("   ├" + "─" * 62 + "┤")
    print("   │ Plain : " + " ".join(list(alpha[:13])) + " │")
    print("   │ Cipher: " + " ".join(list(shifted_alpha[:13])) + " │")
    print("   │ " + "─" * 60 + " │")
    print("   │ Plain : " + " ".join(list(alpha[13:])) + " │")
    print("   │ Cipher: " + " ".join(list(shifted_alpha[13:])) + " │")
    print("   ├" + "─" * 62 + "┤")

    encrypted_sample = caesar_encrypt(sample_text, shift)
    print("   │ Sample Transformation:".ljust(63) + "│")
    print(f"   │   Input : {sample_text:<48} │")
    print(f"   │   Output: {encrypted_sample:<48} │")
    print("   └" + "─" * 62 + "┘")


def parse_input_text(prompt_text):
    """Parse user input text for cipher operations."""
    return input(prompt_text).strip()


def interactive_explorer():
    """Prompt user for text and shift key to perform interactive cipher analysis."""
    print("\n" + "=" * 50)
    print("   🔐 INTERACTIVE CAESAR CIPHER EXPLORER")
    print("=" * 50)

    text = parse_input_text("\n   Enter text to analyze: ")
    if not text:
        print("   ⚠️  No text entered.")
        return

    try:
        shift_str = input("   Enter shift key integer (e.g., 3): ").strip()
        shift = int(shift_str) if shift_str else 3
    except ValueError:
        print("   ⚠️  Invalid shift key. Defaulting to 3.")
        shift = 3

    encrypted = caesar_encrypt(text, shift)
    decrypted = caesar_decrypt(encrypted, shift)
    rot13_text = rot13(text)

    print("\n   📋 Cipher Results:")
    print("   " + "─" * 45)
    print(f"   🔹 Original Text : {text}")
    print(f"   🔹 Shift Key     : {shift}")
    print(f"   🔹 Encrypted Text: {encrypted}")
    print(f"   🔹 Decrypted Text: {decrypted}")
    print(f"   🔹 ROT13 Variant : {rot13_text}")

    print("\n   🕵️  Automated Frequency Analysis Crack Top 3:")
    top_candidates = crack_caesar(encrypted)[:3]
    for rank, (score, cand_shift, cand_text) in enumerate(top_candidates, 1):
        print(f"      Rank {rank}: Shift={cand_shift:2d} | Score={score:.3f} | Text: '{cand_text}'")

    draw_shift_visualization(shift, sample_text=text[:15].upper() if text else "HELLOPYTHON")


def show_mastery_box():
    """Print an artistic summary box."""
    width = 46
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "👑 CAESAR CIPHER MASTERED! 👑".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║  Features: Shift Encryption & Decryption,     ".ljust(width - 2) + "║")
    print("   ║            Case & Non-alpha preservation,     ".ljust(width - 2) + "║")
    print("   ║            ROT13 Transformation,              ".ljust(width - 2) + "║")
    print("   ║            Brute-force Frequency Cracker,     ".ljust(width - 2) + "║")
    print("   ║            ASCII Shift Diagram Visualization  ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    while True:
        print("\n" + "=" * 50)
        print("  DAY 26: CAESAR ENCRYPTION")
        print("=" * 50)
        print()
        print("   📂 Choose an option:")
        print("      1. Run interactive Caesar cipher explorer")
        print("      2. Run built-in demo cases")
        print("      3. Exit")

        choice = input("\n      Select option (1-3): ").strip()
        if choice == "1":
            interactive_explorer()
        elif choice == "2":
            print("\n   >>> Running Built-in Demo Cases <<<")

            # Demo 1: Standard Encryption & Decryption
            t1 = "Hello World! Python Cryptography 101."
            s1 = 5
            print(f"\n      Demo 1: Standard Shift {s1}")
            print(f"      👉 Input    : '{t1}'")
            enc1 = caesar_encrypt(t1, s1)
            print(f"      👉 Encrypted: '{enc1}'")
            print(f"      👉 Decrypted: '{caesar_decrypt(enc1, s1)}'")
            draw_shift_visualization(s1, "HELLOPYTHON")

            # Demo 2: ROT13 Transformation
            t2 = "The Quick Brown Fox Jumps Over The Lazy Dog"
            print(f"\n      Demo 2: ROT13 Transformation")
            print(f"      👉 Input  : '{t2}'")
            r2 = rot13(t2)
            print(f"      👉 ROT13  : '{r2}'")
            print(f"      👉 Un-ROT : '{rot13(r2)}'")

            # Demo 3: Keyless Brute-force Frequency Cracking
            secret_msg = "Attack the eastern castle at dawn when the fog clears"
            secret_shift = 17
            encrypted_secret = caesar_encrypt(secret_msg, secret_shift)
            print(f"\n      Demo 3: Automated Keyless Cipher Cracker")
            print(f"      👉 Intercepted Ciphertext: '{encrypted_secret}'")
            print("      👉 Running English Letter Frequency Analysis...")
            top_crack = crack_caesar(encrypted_secret)[0]
            print(f"      🎉 Cracked Key: Shift {top_crack[1]} | Decrypted: '{top_crack[2]}'")

        elif choice == "3":
            print("\n      Goodbye!")
            break
        else:
            print("      ⚠️  Invalid selection. Please choose 1-3.")

    show_mastery_box()


if __name__ == "__main__":
    main()
