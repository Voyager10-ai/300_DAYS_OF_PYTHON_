def remove_nth_character(s, n):
    """
    Remove the nth character from a string.
    Note: n is 0-indexed.
    """
    if n < 0 or n >= len(s):
        return s
    return s[:n] + s[n+1:]

if __name__ == "__main__":
    test_str = "Python"
    n = 3
    print(f"Original string: {test_str}")
    print(f"Removing character at index {n}: {remove_nth_character(test_str, n)}")
