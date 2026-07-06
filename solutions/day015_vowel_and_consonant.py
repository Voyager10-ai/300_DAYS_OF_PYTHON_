# Day 15: Vowel and Consonant
#
# Problem:
#   Write a Python program that analyzes string input to count, analyze, and highlight
#   vowels and consonants.
#   - Count the total number of vowels and consonants in a text.
#   - Provide a percentage breakdown of vowels and consonants.
#   - Generate a character frequency distribution chart for vowels and consonants.
#   - Provide a visual highlighter in the console showing vowels and consonants.
#   - Offer options to strip vowels/consonants or replace them with custom symbols.
#   - Support analyzing either direct user input or text from a file.
#
# This exercise covers string manipulation, character iteration, dictionaries, math
# proportions, list comprehensions, and interactive terminal interface design.

import collections
import os

# ---------- Constants ----------
VOWELS = set("aeiouAEIOU")
CONSONANTS = set("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ")


# ---------- Core Analysis Logic ----------
def analyze_text(text):
    """
    Analyze the text and return statistics.
    Returns a dictionary of counts, frequencies, and ratios.
    """
    stats = {
        "vowel_count": 0,
        "consonant_count": 0,
        "digit_count": 0,
        "space_count": 0,
        "special_count": 0,
        "total_chars": len(text),
        "vowel_freq": collections.Counter(),
        "consonant_freq": collections.Counter()
    }
    
    for char in text:
        if char in VOWELS:
            stats["vowel_count"] += 1
            stats["vowel_freq"][char.lower()] += 1
        elif char in CONSONANTS:
            stats["consonant_count"] += 1
            stats["consonant_freq"][char.lower()] += 1
        elif char.isdigit():
            stats["digit_count"] += 1
        elif char.isspace():
            stats["space_count"] += 1
        else:
            stats["special_count"] += 1
            
    return stats


# ---------- Text Transformation ----------
def highlight_characters(text, highlight_mode):
    """
    Highlight characters based on mode.
    Modes:
      - 'vowels': Wraps vowels in square brackets like [a]
      - 'consonants': Wraps consonants in square brackets like [b]
      - 'color': Wraps vowels in cyan color and consonants in yellow color (ANSI codes)
    """
    result = []
    
    # ANSI escape sequences for coloring
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    
    for char in text:
        if highlight_mode == "vowels":
            if char in VOWELS:
                result.append(f"[{char}]")
            else:
                result.append(char)
        elif highlight_mode == "consonants":
            if char in CONSONANTS:
                result.append(f"[{char}]")
            else:
                result.append(char)
        elif highlight_mode == "color":
            if char in VOWELS:
                result.append(f"{CYAN}{char}{RESET}")
            elif char in CONSONANTS:
                result.append(f"{YELLOW}{char}{RESET}")
            else:
                result.append(char)
        else:
            result.append(char)
            
    return "".join(result)


def transform_text(text, op_type, replace_char="*"):
    """Transform text based on operation type."""
    if op_type == "strip_vowels":
        return "".join(c for c in text if c not in VOWELS)
    elif op_type == "strip_consonants":
        return "".join(c for c in text if c not in CONSONANTS)
    elif op_type == "replace_vowels":
        return "".join(replace_char if c in VOWELS else c for c in text)
    elif op_type == "replace_consonants":
        return "".join(replace_char if c in CONSONANTS else c for c in text)
    return text


# ---------- ASCII Visualizations ----------
def draw_bar_chart(label, count, total, bar_length=20):
    """Draw a text-based progress/bar chart."""
    if total == 0:
        pct = 0.0
        filled = 0
    else:
        pct = (count / total) * 100
        filled = int((count / total) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    return f"{label:<12} {bar} {count:>4} ({pct:.1f}%)"


def print_analysis_report(text, stats):
    """Print a detailed, beautiful analysis report."""
    print("\n   📊 Text Analysis Results:")
    print("      " + "-" * 45)
    
    # Calculate denominator for vowel/consonant ratio (letters only)
    letters_total = stats["vowel_count"] + stats["consonant_count"]
    
    print(f"      - Total Characters Analyzed: {stats['total_chars']}")
    print(f"      - Total Letters Found:     {letters_total}")
    print()
    print("      --- Distribution Summary ---")
    print("      " + draw_bar_chart("Vowels", stats["vowel_count"], stats["total_chars"]))
    print("      " + draw_bar_chart("Consonants", stats["consonant_count"], stats["total_chars"]))
    print("      " + draw_bar_chart("Digits", stats["digit_count"], stats["total_chars"]))
    print("      " + draw_bar_chart("Whitespaces", stats["space_count"], stats["total_chars"]))
    print("      " + draw_bar_chart("Special/Punct", stats["special_count"], stats["total_chars"]))
    print()
    
    if letters_total > 0:
        print("      --- Vowel vs. Consonant Ratio (of Letters) ---")
        print("      " + draw_bar_chart("Vowels", stats["vowel_count"], letters_total))
        print("      " + draw_bar_chart("Consonants", stats["consonant_count"], letters_total))
        print()
        
    print("      --- Vowel Frequencies ---")
    if stats["vowel_freq"]:
        sorted_vowels = sorted(stats["vowel_freq"].items(), key=lambda x: x[1], reverse=True)
        vowel_strs = [f"{v.upper()}:{count}" for v, count in sorted_vowels]
        print(f"         {', '.join(vowel_strs)}")
    else:
        print("         No vowels found.")
        
    print("\n      --- Top Consonant Frequencies ---")
    if stats["consonant_freq"]:
        sorted_cons = sorted(stats["consonant_freq"].items(), key=lambda x: x[1], reverse=True)[:8]
        cons_strs = [f"{c.upper()}:{count}" for c, count in sorted_cons]
        print(f"         {', '.join(cons_strs)}")
    else:
        print("         No consonants found.")
    print("      " + "-" * 45)


# ---------- Interactive Features ----------
def analyze_interactive_text():
    """Prompt user for text input and perform analysis and highlighting."""
    print("\n   === Input Text to Analyze ===")
    text = input("      Enter your text below:\n      > ").strip()
    if not text:
        print("      ⚠️  Text cannot be empty.")
        return
        
    stats = analyze_text(text)
    print_analysis_report(text, stats)
    
    # Prompt for highlighting options
    print("\n   Highlighting Options:")
    print("      1. Highlight Vowels in [ ] brackets")
    print("      2. Highlight Consonants in [ ] brackets")
    print("      3. Highlight using Colors (Cyan: Vowels, Yellow: Consonants)")
    print("      4. Skip Highlighting")
    choice = input("\n      Select option (1-4): ").strip()
    
    if choice == "1":
        print(f"\n   📝 Highlighted Vowels:\n      {highlight_characters(text, 'vowels')}")
    elif choice == "2":
        print(f"\n   📝 Highlighted Consonants:\n      {highlight_characters(text, 'consonants')}")
    elif choice == "3":
        print(f"\n   📝 Colorized Output:\n      {highlight_characters(text, 'color')}")
        
    # Prompt for transformation options
    print("\n   Transformation Options:")
    print("      1. Strip all Vowels")
    print("      2. Strip all Consonants")
    print("      3. Redact Vowels (replace with *)")
    print("      4. Redact Consonants (replace with *)")
    print("      5. Skip Transformations")
    trans_choice = input("\n      Select option (1-5): ").strip()
    
    if trans_choice == "1":
        print(f"\n   🔄 Result: {transform_text(text, 'strip_vowels')}")
    elif trans_choice == "2":
        print(f"\n   🔄 Result: {transform_text(text, 'strip_consonants')}")
    elif trans_choice == "3":
        print(f"\n   🔄 Result: {transform_text(text, 'replace_vowels', '*')}")
    elif trans_choice == "4":
        print(f"\n   🔄 Result: {transform_text(text, 'replace_consonants', '*')}")


def analyze_file_text():
    """Read a local file and analyze its text content."""
    print("\n   === File-Based Text Analyzer ===")
    file_path = input("      Enter absolute or relative file path: ").strip()
    if not file_path:
        return
        
    if not os.path.exists(file_path):
        print(f"      ❌ File not found at: {file_path}")
        return
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"\n      📖 Read {len(content)} characters from file.")
        if len(content) > 2000:
            print("      ⚠️  File is large, analysis report shown. Preview of first 200 chars:")
            print(f"      \"{content[:200]}...\"")
        else:
            print(f"      Text Preview:\n      \"{content}\"")
            
        stats = analyze_text(content)
        print_analysis_report(content, stats)
    except Exception as e:
        print(f"      ❌ Error reading file: {e}")


def show_mastery_box():
    """Print an artistic summary box."""
    width = 44
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "  🔤 VOWELS & CONSONANTS ANALYSIS DONE! 🔤  ".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║" + "  Calculations: Letter Ratio Statistics,".ljust(width - 2) + "║")
    print("   ║" + "                Vowel/Consonant Counts, ".ljust(width - 2) + "║")
    print("   ║" + "                Frequency Distribution, ".ljust(width - 2) + "║")
    print("   ║" + "  Features: Color Highlighting,         ".ljust(width - 2) + "║")
    print("   ║" + "            Text Redaction & Stripping, ".ljust(width - 2) + "║")
    print("   ║" + "            File Reader Integration     ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    while True:
        print("\n" + "=" * 50)
        print("  DAY 15: VOWEL AND CONSONANT ANALYZER")
        print("=" * 50)
        print()
        print("   📂 Choose an option:")
        print("      1. Analyze text input interactively")
        print("      2. Analyze a text file")
        print("      3. Run built-in demo (Python quote)")
        print("      4. Exit")
        
        choice = input("\n      Select mode (1-4): ").strip()
        if choice == "1":
            analyze_interactive_text()
        elif choice == "2":
            analyze_file_text()
        elif choice == "3":
            demo_text = "Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex."
            print(f"\n   📝 Demo Text: \"{demo_text}\"")
            stats = analyze_text(demo_text)
            print_analysis_report(demo_text, stats)
            print(f"   🎨 Color Highlight Preview:\n      {highlight_characters(demo_text, 'color')}")
        elif choice == "4":
            print("\n      Goodbye!")
            break
        else:
            print("      ⚠️  Invalid selection. Please choose 1-4.")
            
    show_mastery_box()


if __name__ == "__main__":
    main()
