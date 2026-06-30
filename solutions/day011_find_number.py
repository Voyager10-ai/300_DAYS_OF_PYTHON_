# Day 11: Find Number
#
# Problem:
#   Write a Python program that implements various search algorithms and number finding logic.
#   - Find numbers divisible by 7 and multiple of 5 in a range (e.g., 1500 to 2700)
#   - Implement Linear Search and Binary Search algorithms
#   - Find special numbers in a range (Armstrong numbers, Perfect numbers)
#   - Step-by-step search process visualization
#   - Interactive search explorer
#
# This exercise covers iteration, search algorithms, search complexity, and number properties.

# ---------- Range-Based Number Finding ----------
def find_divisible_multiples(start=1500, end=2700, div=7, mult=5):
    """Find all numbers in [start, end] divisible by div and multiples of mult."""
    results = [num for num in range(start, end + 1) if num % div == 0 and num % mult == 0]
    print(f"\n   🔍 Numbers in [{start}, {end}] divisible by {div} & multiple of {mult}:")
    print(f"      Count: {len(results)}")
    print(f"      Matches: {results}")
    return results


# ---------- Classic Search Algorithms ----------
def linear_search(arr, target):
    """Perform linear search on list arr to find target. Returns index or -1."""
    for idx, val in enumerate(arr):
        if val == target:
            return idx
    return -1


def binary_search(arr, target):
    """Perform binary search on sorted list arr to find target. Returns index or -1."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 11: FIND NUMBER")
    print("=" * 50)
    print()

    print(">>> Range-Based Finding Demo <<<")
    find_divisible_multiples(1500, 2700, 7, 5)
    print()

    print(">>> Search Algorithms Demo <<<")
    numbers = [24, 8, 42, 16, 90, 5, 73, 11]
    sorted_numbers = sorted(numbers)
    target = 16
    
    print(f"   Original List: {numbers}")
    print(f"   Sorted List:   {sorted_numbers}")
    print(f"   Target to find: {target}")
    
    l_idx = linear_search(numbers, target)
    b_idx = binary_search(sorted_numbers, target)
    
    print(f"      Linear Search index in original: {l_idx}")
    print(f"      Binary Search index in sorted:   {b_idx}")


# ---------- Custom Special Number Finding ----------
def is_armstrong(n):
    """Check if a number is an Armstrong number (sum of digits raised to the power of number of digits)."""
    if n < 0:
        return False
    digits = [int(char) for char in str(n)]
    power = len(digits)
    return sum(d**power for d in digits) == n


def is_perfect(n):
    """Check if a number is a Perfect number (sum of its proper divisors equals the number)."""
    if n <= 1:
        return False
    divisors = [1]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i * i != n:
                divisors.append(n // i)
    return sum(divisors) == n


def find_special_numbers(start=1, end=1000):
    """Find Armstrong and Perfect numbers within [start, end]."""
    armstrongs = [n for n in range(start, end + 1) if is_armstrong(n)]
    perfects = [n for n in range(start, end + 1) if is_perfect(n)]
    
    print(f"\n   ✨ Special Numbers in [{start}, {end}]:")
    print(f"      Armstrong Numbers: {armstrongs}")
    print(f"      Perfect Numbers:   {perfects}")
    return armstrongs, perfects


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 11: FIND NUMBER")
    print("=" * 50)
    print()

    print(">>> Range-Based Finding Demo <<<")
    find_divisible_multiples(1500, 2700, 7, 5)
    print()

    print(">>> Search Algorithms Demo <<<")
    numbers = [24, 8, 42, 16, 90, 5, 73, 11]
    sorted_numbers = sorted(numbers)
    target = 16
    
    print(f"   Original List: {numbers}")
    print(f"   Sorted List:   {sorted_numbers}")
    print(f"   Target to find: {target}")
    
    l_idx = linear_search(numbers, target)
    b_idx = binary_search(sorted_numbers, target)
    
    print(f"      Linear Search index in original: {l_idx}")
    print(f"      Binary Search index in sorted:   {b_idx}")
    print()

    print(">>> Special Number Finding <<<")
    find_special_numbers(1, 1000)


# ---------- Interactive Search Explorer ----------
def interactive_search_explorer():
    """Allows interactive search and finding features."""
    print("\n   🔍 Interactive Search Explorer:")
    print("      1. Search target number in a list (Linear & Binary)")
    print("      2. Find divisible & multiples in range")
    print("      3. Find special numbers (Armstrong & Perfect)")
    choice = input("      Select option (1-3): ").strip()
    
    if choice == "1":
        list_str = input("      Enter numbers separated by spaces: ").strip()
        target_str = input("      Enter target number to find: ").strip()
        try:
            arr = [int(x) for x in list_str.split()]
            target = int(target_str)
            sorted_arr = sorted(arr)
            
            l_idx = linear_search(arr, target)
            b_idx = binary_search(sorted_arr, target)
            
            print(f"      Linear Search index: {l_idx}")
            print(f"      Binary Search index (on sorted {sorted_arr}): {b_idx}")
        except ValueError:
            print("      ❌ Invalid inputs.")
            
    elif choice == "2":
        try:
            start = int(input("      Enter start of range: ").strip())
            end = int(input("      Enter end of range: ").strip())
            div = int(input("      Enter divisibility factor: ").strip())
            mult = int(input("      Enter multiple factor: ").strip())
            find_divisible_multiples(start, end, div, mult)
        except ValueError:
            print("      ❌ Invalid inputs.")
            
    elif choice == "3":
        try:
            start = int(input("      Enter start of range: ").strip())
            end = int(input("      Enter end of range: ").strip())
            find_special_numbers(start, end)
        except ValueError:
            print("      ❌ Invalid inputs.")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 11: FIND NUMBER")
    print("=" * 50)
    print()

    print(">>> Range-Based Finding Demo <<<")
    find_divisible_multiples(1500, 2700, 7, 5)
    print()

    print(">>> Search Algorithms Demo <<<")
    numbers = [24, 8, 42, 16, 90, 5, 73, 11]
    sorted_numbers = sorted(numbers)
    target = 16
    
    print(f"   Original List: {numbers}")
    print(f"   Sorted List:   {sorted_numbers}")
    print(f"   Target to find: {target}")
    
    l_idx = linear_search(numbers, target)
    b_idx = binary_search(sorted_numbers, target)
    
    print(f"      Linear Search index in original: {l_idx}")
    print(f"      Binary Search index in sorted:   {b_idx}")
    print()

    print(">>> Special Number Finding <<<")
    find_special_numbers(1, 1000)
    print()

    print(">>> Interactive Explorer <<<")
    interactive_search_explorer()


if __name__ == "__main__":
    main()
