# Day 13: Password Validation
#
# Problem:
#   Write a Python program that validates passwords based on specific strength criteria
#   and evaluates their security level.
#   - Check length (8-20 characters), uppercase, lowercase, numbers, and special characters.
#   - Calculate entropy (in bits) and estimate crack times under different attack scenarios.
#   - Generate random, cryptographically secure passwords that satisfy all rules.
#   - Support bulk validation of comma-separated passwords.
#   - Provide interactive menus and detailed feedback on rule violations.
#
# This exercise covers string manipulation, conditional statements, mathematical analysis (entropy),
# random selection, and interactive CLI dashboard design.

import math
import random
import string


# ---------- Configuration & Rules ----------
SPECIAL_CHARACTERS = '!@#$%^&*(),.?":{}|<>'

RULES = {
    "length": {
        "desc": "At least 8 and at most 20 characters",
        "check": lambda p: 8 <= len(p) <= 20
    },
    "uppercase": {
        "desc": "At least one uppercase letter (A-Z)",
        "check": lambda p: any(c.isupper() for c in p)
    },
    "lowercase": {
        "desc": "At least one lowercase letter (a-z)",
        "check": lambda p: any(c.islower() for c in p)
    },
    "digit": {
        "desc": "At least one digit (0-9)",
        "check": lambda p: any(c.isdigit() for c in p)
    },
    "special": {
        "desc": f"At least one special character ({SPECIAL_CHARACTERS})",
        "check": lambda p: any(c in SPECIAL_CHARACTERS for c in p)
    },
    "no_spaces": {
        "desc": "No whitespace characters allowed",
        "check": lambda p: not any(c.isspace() for c in p)
    }
}


# ---------- Core Validation Logic ----------
def validate_password(password):
    """
    Validate password against all rules.
    Returns (is_valid, passed_rules, failed_rules)
    """
    passed = []
    failed = []
    
    for rule_id, rule_info in RULES.items():
        if rule_info["check"](password):
            passed.append((rule_id, rule_info["desc"]))
        else:
            failed.append((rule_id, rule_info["desc"]))
            
    is_valid = len(failed) == 0
    return is_valid, passed, failed


# ---------- Strength & Entropy Calculations ----------
def calculate_entropy(password):
    """
    Calculate the Shannon entropy of a password based on character pool size.
    Formula: Entropy = length * log2(charset_size)
    """
    if not password:
        return 0.0
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in SPECIAL_CHARACTERS for c in password)
    
    charset_size = 0
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_special: charset_size += len(SPECIAL_CHARACTERS)
    
    # Handle characters outside standard categories (other symbols, unicode, spaces)
    extra_chars = set(password) - set(string.ascii_letters + string.digits + SPECIAL_CHARACTERS)
    if extra_chars:
        charset_size += len(extra_chars)
        
    if charset_size == 0:
        charset_size = 1
        
    entropy = len(password) * math.log2(charset_size)
    return entropy


def estimate_crack_time(entropy):
    """
    Estimate the time required to brute-force the password at various speeds.
    Returns formatted time strings for:
      - Online attack (100 guesses/sec)
      - Offline fast attack (10 billion guesses/sec)
      - Supercomputer/nation state (100 trillion guesses/sec)
    """
    guesses = 2**entropy
    
    def format_time(seconds):
        if seconds < 1:
            return "instantly"
        
        minutes = seconds / 60
        if minutes < 1:
            return f"{seconds:.1f} seconds"
        
        hours = minutes / 60
        if hours < 1:
            return f"{minutes:.1f} minutes"
        
        days = hours / 24
        if days < 1:
            return f"{hours:.1f} hours"
        
        years = days / 365
        if years < 1:
            return f"{days:.1f} days"
        
        if years < 1000:
            return f"{years:.1f} years"
        
        exponent = int(math.log10(years))
        if exponent >= 6:
            return f"10^{exponent} years"
        return f"{years:,.0f} years"
        
    online_time = format_time(guesses / 100)
    offline_time = format_time(guesses / 1e10)
    super_time = format_time(guesses / 1e14)
    
    return online_time, offline_time, super_time


def get_strength_rating(entropy, is_valid):
    """Get strength tier based on entropy bits and basic rules validity."""
    if not is_valid:
        return "❌ Invalid (Violates basic rules)", "🔴"
    if entropy < 28:
        return "Very Weak", "🔴"
    elif entropy < 36:
        return "Weak", "🟠"
    elif entropy < 60:
        return "Medium", "🟡"
    elif entropy < 80:
        return "Strong", "🟢"
    else:
        return "Very Strong (Excellent)", "💎"


# ---------- Password Generator ----------
def generate_strong_password(length=12):
    """Generate a strong password that strictly passes all validation rules."""
    if length < 8:
        length = 8
    elif length > 20:
        length = 20
        
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = SPECIAL_CHARACTERS
    
    # Build core to satisfy constraints
    password_parts = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the remaining slots
    all_allowed = lower + upper + digits + special
    for _ in range(length - 4):
        password_parts.append(random.choice(all_allowed))
        
    # Shuffle to ensure unpredictable positions
    random.shuffle(password_parts)
    return "".join(password_parts)


# ---------- Interactive Features ----------
def interactive_check():
    """Evaluate a single password inputted by the user with step-by-step feedback."""
    print("\n   === Single Password Validator ===")
    password = input("      Enter a password to evaluate: ").strip()
    if not password:
        print("      ⚠️  Password cannot be empty.")
        return
        
    is_valid, passed, failed = validate_password(password)
    entropy = calculate_entropy(password)
    rating, emoji = get_strength_rating(entropy, is_valid)
    
    print("\n   📊 Rule Checklist:")
    for rule_id, desc in RULES.items():
        if any(p[0] == rule_id for p in passed):
            print(f"      ✅ [PASSED] {desc}")
        else:
            print(f"      ❌ [FAILED] {desc}")
            
    print("\n   🔒 Security Analysis:")
    print(f"      - Character Length: {len(password)}")
    print(f"      - Entropy Estimate: {entropy:.1f} bits")
    print(f"      - Security Rating:  {emoji} {rating}")
    
    if is_valid:
        online, offline, super_comp = estimate_crack_time(entropy)
        print("\n   ⏳ Brute-Force Time Estimates:")
        print(f"      - Online attack (100 attempts/sec):    {online}")
        print(f"      - Offline fast GPU (10 billion/sec):   {offline}")
        print(f"      - Nation-state (100 trillion/sec):     {super_comp}")
    else:
        print("\n   💡 Tips to Improve:")
        print("      - Fix all failed criteria above to meet the baseline policy.")
        print("      - Make it longer and combine character types to increase entropy.")


def interactive_generate():
    """Prompt user for length and generate a strong password."""
    print("\n   === Password Generator ===")
    try:
        len_str = input("      Enter password length (8-20, default 12): ").strip()
        if not len_str:
            length = 12
        else:
            length = int(len_str)
            if not (8 <= length <= 20):
                print("      ⚠️  Length must be between 8 and 20. Defaulting to 12.")
                length = 12
    except ValueError:
        print("      ❌ Invalid input. Defaulting to 12.")
        length = 12
        
    generated = generate_strong_password(length)
    entropy = calculate_entropy(generated)
    is_valid, _, _ = validate_password(generated)
    rating, emoji = get_strength_rating(entropy, is_valid)
    
    print("\n   ✨ Generated Password:")
    print(f"      🔑 {generated}")
    print(f"      - Entropy: {entropy:.1f} bits ({emoji} {rating})")
    print("      - Guaranteed to satisfy all validation rules.")


def bulk_check():
    """Allow user to enter comma-separated passwords and check them in bulk."""
    print("\n   === Bulk Password Validator ===")
    pw_input = input("      Enter passwords separated by commas:\n      > ").strip()
    if not pw_input:
        print("      ⚠️  No input provided.")
        return
        
    passwords = [p.strip() for p in pw_input.split(",") if p.strip()]
    if not passwords:
        print("      ⚠️  No valid passwords found in input.")
        return
        
    print(f"\n   📋 Results for {len(passwords)} passwords:")
    print("      " + "-" * 70)
    print("      %-22s | %-12s | %-10s | %-20s" % ("Password Preview", "Validity", "Entropy", "Details"))
    print("      " + "-" * 70)
    
    for pwd in passwords:
        is_valid, _, failed = validate_password(pwd)
        entropy = calculate_entropy(pwd)
        
        # Mask password preview if long
        preview = pwd if len(pwd) <= 20 else pwd[:17] + "..."
        valid_str = "✅ Valid" if is_valid else "❌ Invalid"
        
        if is_valid:
            detail = "Passes all rules"
        else:
            detail = f"Fails: {', '.join([f[0] for f in failed])}"
            
        print("      %-22s | %-12s | %-10.1f | %-20s" % (preview, valid_str, entropy, detail))
    print("      " + "-" * 70)


def show_mastery_box():
    """Print an artistic summary box."""
    width = 44
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "  🔒 PASSWORD VALIDATOR COMPLETE! 🔒  ".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║" + "  Features: Complex Rules Verification,".ljust(width - 2) + "║")
    print("   ║" + "            Shannon Entropy Bits,     ".ljust(width - 2) + "║")
    print("   ║" + "            Brute-Force Estimates,    ".ljust(width - 2) + "║")
    print("   ║" + "            Secure Random Generator,  ".ljust(width - 2) + "║")
    print("   ║" + "            Bulk Validator (Table)    ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    while True:
        print("\n" + "=" * 50)
        print("  DAY 13: PASSWORD VALIDATION & STRENGTH ANALYSIS")
        print("=" * 50)
        print()
        print("   🔑 Choose an option:")
        print("      1. Validate a single password")
        print("      2. Generate a secure strong password")
        print("      3. Bulk validate multiple passwords (comma-separated)")
        print("      4. Exit")
        
        choice = input("\n      Select mode (1-4): ").strip()
        if choice == "1":
            interactive_check()
        elif choice == "2":
            interactive_generate()
        elif choice == "3":
            bulk_check()
        elif choice == "4":
            print("\n      Goodbye!")
            break
        else:
            print("      ⚠️  Invalid selection. Please choose 1-4.")
            
    show_mastery_box()


if __name__ == "__main__":
    main()
