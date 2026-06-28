# Day 8: Count Digit Letter
#
# Problem:
#   Write a Python program that accepts a sentence and calculates the number of
#   letters and digits in it.
#   - Basic counting using built-in string methods (.isalpha(), .isdigit())
#   - Custom counting using ASCII value ranges
#   - Character frequency distribution (counts for each letter and digit)
#   - Visual representation (ASCII bar chart of character categories)
#   - Interactive input analyzer
#
# This exercise covers string manipulation, character classification, loops,
# dictionary usage, and visual data representation in terminal.


# ---------- Basic Counting ----------
def count_builtins(text):
    """Count letters and digits using standard string methods."""
    letters = sum(1 for char in text if char.isalpha())
    digits = sum(1 for char in text if char.isdigit())
    others = len(text) - letters - digits

    print(f"\n   📝 Analyzing: '{text}'")
    print(f"      🔤 Letters: {letters}")
    print(f"      🔢 Digits:  {digits}")
    print(f"      ✨ Others:  {others}")
    return letters, digits, others


# ---------- Custom ASCII Range Counting ----------
def count_ascii_ranges(text):
    """Count letters and digits using raw ASCII integer comparisons (ord())."""
    letters = 0
    digits = 0
    others = 0

    for char in text:
        code = ord(char)
        # Check uppercase (65-90) or lowercase (97-122)
        if (65 <= code <= 90) or (97 <= code <= 122):
            letters += 1
        # Check digit (48-57)
        elif 48 <= code <= 57:
            digits += 1
        else:
            others += 1

    print(f"\n   📝 ASCII analysis: '{text}'")
    print(f"      🔤 Letters: {letters} (ASCII 65-90, 97-122)")
    print(f"      🔢 Digits:  {digits} (ASCII 48-57)")
    print(f"      ✨ Others:  {others}")
    return letters, digits, others


# ---------- Character Frequency Distribution ----------
def character_frequency(text):
    """Calculate and display counts for each unique letter and digit."""
    freq = {}
    for char in text:
        if char.isalnum():
            # count case-insensitively
            c = char.lower()
            freq[c] = freq.get(c, 0) + 1

    print(f"\n   📊 Character Frequencies (alphanumeric only, case-insensitive) in '{text}':")
    if not freq:
        print("      No letters or digits found.")
        return freq

    # Sort by character
    sorted_chars = sorted(freq.items())
    # Sort by frequency descending
    sorted_freqs = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    print("      Sorted by char:      " + ", ".join(f"'{c}': {count}" for c, count in sorted_chars))
    print("      Sorted by frequency: " + ", ".join(f"'{c}': {count}" for c, count in sorted_freqs))
    return freq


# ---------- Visual Data Representation ----------
def visualize_categories(text):
    """Draw a horizontal ASCII bar chart of character categories."""
    letters = sum(1 for char in text if char.isalpha())
    digits = sum(1 for char in text if char.isdigit())
    others = len(text) - letters - digits
    total = len(text)

    print(f"\n   📊 Category Chart for '{text}':")
    if total == 0:
        print("      Empty string.")
        return

    # Scale to max width of 30 characters
    max_bar_width = 30
    l_width = int(letters / total * max_bar_width) if total > 0 else 0
    d_width = int(digits / total * max_bar_width) if total > 0 else 0
    o_width = int(others / total * max_bar_width) if total > 0 else 0

    # Ensure we show at least one block if count > 0
    if letters > 0 and l_width == 0: l_width = 1
    if digits > 0 and d_width == 0: d_width = 1
    if others > 0 and o_width == 0: o_width = 1

    print(f"      🔤 Letters: [{ '█' * l_width }{ '░' * (max_bar_width - l_width) }] {letters} ({letters/total*100:.1f}%)")
    print(f"      🔢 Digits:  [{ '█' * d_width }{ '░' * (max_bar_width - d_width) }] {digits} ({digits/total*100:.1f}%)")
    print(f"      ✨ Others:  [{ '█' * o_width }{ '░' * (max_bar_width - o_width) }] {others} ({others/total*100:.1f}%)")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 8: COUNT DIGIT LETTER")
    print("=" * 50)
    print()

    print(">>> Basic Counting Demo <<<")
    count_builtins("hello world! 123")
    count_builtins("Python 3.10 is awesome!")
    print()

    print(">>> ASCII Range Counting Demo <<<")
    count_ascii_ranges("User#123! Pass@456")
    print()

    print(">>> Alphanumeric Frequencies <<<")
    character_frequency("Abrakadabra! 99 Luftballons.")
    print()

    print(">>> Visual Data Representation <<<")
    visualize_categories("Today is June 28, 2026. The time is 1:46 PM.")


if __name__ == "__main__":
    main()




