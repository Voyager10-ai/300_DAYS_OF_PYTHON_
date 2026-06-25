# Day 2: Input Age
#
# Problem:
#   Write a Python program that takes a user's age as input and performs
#   various operations on it.
#   - Take age as input from the user
#   - Validate the input (ensure it's a valid age)
#   - Calculate birth year, days lived, and future milestones
#   - Classify the age into life stages
#   - Display fun facts and statistics based on the age
#
# This exercise covers Python's input() function, type conversion,
# validation, and conditional logic.

from datetime import datetime


# ---------- Basic Input ----------
def basic_input():
    """Demonstrate simple input() and type conversion."""
    # input() always returns a string
    age_str = input("Enter your age: ")
    print(f"You entered: {age_str} (type: {type(age_str).__name__})")

    # Convert to integer
    age = int(age_str)
    print(f"Converted:  {age} (type: {type(age).__name__})")

    return age


def get_age_from_birth_year():
    """Calculate age from birth year input."""
    birth_year = int(input("Enter your birth year: "))
    current_year = datetime.now().year
    age = current_year - birth_year
    print(f"Born in {birth_year} → You are approximately {age} years old")
    return age


# ---------- Validation & Error Handling ----------
def validate_age(age_str):
    """Validate that the input is a valid age. Returns (is_valid, age_or_error)."""
    # Check if it's a number at all
    try:
        age = int(age_str)
    except ValueError:
        return False, f"'{age_str}' is not a valid integer"

    # Check reasonable range
    if age < 0:
        return False, "Age cannot be negative"
    if age > 150:
        return False, "Age cannot exceed 150 (oldest recorded: 122)"
    return True, age


def get_validated_age():
    """Keep asking until the user provides a valid age."""
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        age_str = input(f"Enter your age (attempt {attempt}/{max_attempts}): ")
        is_valid, result = validate_age(age_str)
        if is_valid:
            print(f"✅ Valid age: {result}")
            return result
        else:
            print(f"❌ Invalid: {result}")
    print("Too many invalid attempts. Using default age of 25.")
    return 25


def demonstrate_validation():
    """Show validation with various test cases (no user input needed)."""
    test_cases = ["25", "abc", "-5", "200", "0", "17", "3.5", ""]
    print(f"{'Input':<10} {'Valid?':<8} {'Result'}")
    print("-" * 40)
    for test in test_cases:
        is_valid, result = validate_age(test)
        status = "✅ Yes" if is_valid else "❌ No"
        print(f"{repr(test):<10} {status:<8} {result}")



# ---------- Age Calculations & Milestones ----------
def calculate_age_stats(age):
    """Calculate interesting statistics based on age."""
    days_lived = age * 365 + (age // 4)  # accounting for leap years
    hours_lived = days_lived * 24
    heartbeats = hours_lived * 60 * 72  # avg 72 beats per minute
    breaths = hours_lived * 60 * 16  # avg 16 breaths per minute

    print(f"📊 Age Statistics for {age} years old:")
    print(f"   Days lived:       ~{days_lived:,}")
    print(f"   Hours lived:      ~{hours_lived:,}")
    print(f"   Heartbeats:       ~{heartbeats:,}")
    print(f"   Breaths taken:    ~{breaths:,}")


def calculate_milestones(age):
    """Show upcoming and past life milestones."""
    milestones = {
        1: "🎒 First birthday",
        5: "🏫 Started school",
        13: "🎮 Became a teenager",
        16: "🛵 Can learn to drive (many countries)",
        18: "🎓 Legal adult / Voting age",
        21: "🍷 Legal drinking age (US)",
        25: "🧠 Brain fully developed",
        30: "💼 Career prime begins",
        40: "🏆 Life begins at 40",
        50: "🥇 Half-century milestone",
        60: "🌅 Retirement approaching",
        65: "🏖️  Retirement age (many countries)",
        75: "💎 Diamond jubilee of life",
        100: "💯 Centenarian!",
    }

    print(f"🏁 Life Milestones (age {age}):")
    for milestone_age, description in milestones.items():
        if milestone_age <= age:
            print(f"   ✅ Age {milestone_age:>3}: {description}")
        elif milestone_age <= age + 20:
            years_left = milestone_age - age
            print(f"   ⏳ Age {milestone_age:>3}: {description} (in {years_left} years)")



# ---------- Age Classification ----------
def classify_age(age):
    """Classify age into life stages using conditional logic."""
    stages = [
        (0, 0, "👶 Newborn"),
        (1, 3, "🍼 Infant / Toddler"),
        (4, 12, "🧒 Child"),
        (13, 17, "🎮 Teenager"),
        (18, 24, "🎓 Young Adult"),
        (25, 39, "💼 Adult"),
        (40, 59, "🏆 Middle-aged"),
        (60, 74, "🌅 Senior"),
        (75, 89, "👴 Elderly"),
        (90, 150, "💎 Super Senior"),
    ]

    print(f"🏷️  Age Classification for {age}:")
    for low, high, label in stages:
        marker = " 👈 YOU" if low <= age <= high else ""
        print(f"   {low:>3}-{high:<3} : {label}{marker}")


def identify_generation(age):
    """Identify which generation the user belongs to."""
    current_year = datetime.now().year
    birth_year = current_year - age

    generations = [
        (1928, 1945, "Silent Generation", "🤫"),
        (1946, 1964, "Baby Boomers", "👶"),
        (1965, 1980, "Generation X", "❌"),
        (1981, 1996, "Millennials (Gen Y)", "📱"),
        (1997, 2012, "Generation Z", "💻"),
        (2013, 2025, "Generation Alpha", "🤖"),
    ]

    print(f"\n🌍 Generation Identifier (born ~{birth_year}):")
    for start, end, name, emoji in generations:
        if start <= birth_year <= end:
            print(f"   {emoji} You are a {name} ({start}-{end})")
            return name

    print("   🔮 Generation not in database")
    return "Unknown"



# ---------- Creative & Fun Display ----------
def display_age_progress_bar(age, max_age=100):
    """Show a visual progress bar for life progress."""
    progress = min(age / max_age, 1.0)
    bar_width = 30
    filled = int(bar_width * progress)
    empty = bar_width - filled

    bar = "█" * filled + "░" * empty
    percent = progress * 100

    print(f"\n🎯 Life Progress (assuming {max_age} years):")
    print(f"   [{bar}] {percent:.1f}%")
    print(f"   {age} of {max_age} years")


def fun_facts(age):
    """Display fun and quirky facts based on the user's age."""
    years_sleeping = round(age * 0.33, 1)
    years_eating = round(age * 0.04, 1)
    years_on_phone = round(age * 0.05, 1) if age >= 10 else 0
    words_spoken = age * 16_000 * 365  # avg 16,000 words/day

    print(f"\n🎲 Fun Facts About Your {age} Years:")
    print(f"   😴 Time spent sleeping:    ~{years_sleeping} years")
    print(f"   🍽️  Time spent eating:      ~{years_eating} years")
    if years_on_phone > 0:
        print(f"   📱 Time on phone:          ~{years_on_phone} years")
    print(f"   💬 Words spoken:           ~{words_spoken:,}")
    print(f"   🌍 Earth orbits completed: {age}")
    print(f"   🚀 Distance through space: ~{age * 584_000_000:,} miles")
    print(f"      (Earth travels ~584M miles/year around the Sun)")


def display_age_art(age):
    """Create a simple artistic display of the age."""
    width = 36
    print()
    print("+" + "-" * (width - 2) + "+")
    print("|" + " " * (width - 2) + "|")
    print("|" + f"🎂 You are {age} years young! 🎂".center(width - 2) + "|")
    print("|" + " " * (width - 2) + "|")
    # Birthday candles
    candles = "🕯️" * min(age, 10)
    if age > 10:
        candles += f" (+{age - 10} more)"
    print("|" + candles.center(width - 2) + "|")
    print("|" + " " * (width - 2) + "|")
    print("+" + "-" * (width - 2) + "+")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 2: INPUT AGE")
    print("=" * 50)
    print()

    print(">>> Basic Input <<<")
    age = basic_input()
    print()

    print(">>> Age from Birth Year <<<")
    get_age_from_birth_year()
    print()

    print(">>> Validation Demo <<<")
    demonstrate_validation()
    print()

    print(">>> Age Statistics <<<")
    calculate_age_stats(age)
    print()

    print(">>> Life Milestones <<<")
    calculate_milestones(age)
    print()

    print(">>> Age Classification <<<")
    classify_age(age)
    identify_generation(age)
    print()

    print(">>> Fun Facts & Visuals <<<")
    display_age_progress_bar(age)
    fun_facts(age)
    display_age_art(age)
if __name__ == "__main__":
    main()
