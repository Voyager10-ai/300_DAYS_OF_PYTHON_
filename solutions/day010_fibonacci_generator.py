# Day 10: Fibonacci Generator
#
# Problem:
#   Write a Python program that generates the Fibonacci sequence.
#   - Generate the first N Fibonacci numbers (iterative and generator-based)
#   - Recursive Fibonacci implementation with memoization (lru_cache)
#   - Check if a given number is a valid Fibonacci number
#   - Mathematical properties (Golden Ratio approximation)
#   - Interactive Fibonacci explorer
#
# This exercise covers generators, recursion, caching, mathematical ratios,
# and sequence validation.

from functools import lru_cache

# ---------- Generation (Iterative & Generator) ----------
def fibonacci_iterative(n):
    """Generate the first N Fibonacci numbers iteratively."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq


def fibonacci_generator(n):
    """Yield the first N Fibonacci numbers one by one."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


# ---------- Recursive with Memoization ----------
@lru_cache(maxsize=None)
def fibonacci_recursive(n):
    """Calculate the N-th Fibonacci number recursively with caching."""
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative integers.")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


# ---------- Fibonacci Number Validation ----------
def is_fibonacci_number(n):
    """Check if a number is a valid Fibonacci number using the perfect square formula."""
    import math
    if n < 0:
        return False
    # A number is Fibonacci if and only if one of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square
    val1 = 5 * n * n + 4
    val2 = 5 * n * n - 4
    
    root1 = math.isqrt(val1)
    root2 = math.isqrt(val2)
    
    return (root1 * root1 == val1) or (root2 * root2 == val2)


# ---------- Mathematical Properties (Golden Ratio) ----------
def golden_ratio_convergence(n=15):
    """Demonstrate how the ratio of consecutive Fibonacci numbers converges to the Golden Ratio."""
    seq = fibonacci_iterative(n + 1)
    import math
    golden_ratio = (1 + math.sqrt(5)) / 2
    
    print(f"\n   ✨ Golden Ratio approximation (Actual: {golden_ratio:.10f}):")
    print(f"      {'Term N':<8} {'Fib(N)':<8} {'Ratio (N/N-1)':<18} {'Difference':<12}")
    print(f"      {'-' * 50}")
    
    for i in range(2, len(seq)):
        prev = seq[i - 1]
        curr = seq[i]
        if prev == 0:
            continue
        ratio = curr / prev
        diff = abs(ratio - golden_ratio)
        print(f"      {i:<8} {curr:<8} {ratio:<18.10f} {diff:<12.10f}")


# ---------- Visualizer & Interactive Explorer ----------
def draw_fibonacci_spiral_blocks(n=8):
    """Visualize Fibonacci growth using horizontal block bars."""
    seq = fibonacci_iterative(n)
    print("\n   🎨 Fibonacci Visual Growth:")
    for i, val in enumerate(seq):
        bar = "█" * val
        print(f"      F({i:<2}) = {val:<3} | {bar}")


def interactive_explorer():
    """Prompt the user for inputs to run the various generator features."""
    print("\n   🌀 Interactive Fibonacci Explorer:")
    print("      1. Generate first N terms")
    print("      2. Check if a number is Fibonacci")
    choice = input("      Select option (1-2): ").strip()
    
    if choice == "1":
        val = input("      Enter N terms to generate: ").strip()
        if val.isdigit():
            num = int(val)
            print(f"      Terms: {fibonacci_iterative(num)}")
            if num <= 10:
                draw_fibonacci_spiral_blocks(num)
        else:
            print("      ❌ Invalid input.")
    elif choice == "2":
        val = input("      Enter a non-negative integer to check: ").strip()
        if val.isdigit():
            num = int(val)
            res = "is a Fibonacci number! 🎉" if is_fibonacci_number(num) else "is NOT a Fibonacci number."
            print(f"      Number {num} {res}")
        else:
            print("      ❌ Invalid input.")


def show_mastery_box():
    """Print an artistic summary box."""
    width = 44
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "  🌀 FIBONACCI GENERATOR COMPLETE! 🌀  ".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║" + "  Features: Iterative, Caching Recurse,".ljust(width - 2) + "║")
    print("   ║" + "            Generators, Golden Ratio,  ".ljust(width - 2) + "║")
    print("   ║" + "            Perfect Square Check, Art  ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 10: FIBONACCI GENERATOR")
    print("=" * 50)
    print()

    print(">>> Iterative Generation <<<")
    n = 10
    print(f"   First {n} terms: {fibonacci_iterative(n)}")

    print("\n>>> Generator-based (yield) <<<")
    gen = fibonacci_generator(n)
    print(f"   First {n} terms from generator: {list(gen)}")

    print("\n>>> Recursive with Caching <<<")
    rec_terms = [fibonacci_recursive(i) for i in range(n)]
    print(f"   First {n} terms recursively: {rec_terms}")
    print(f"   50th Fibonacci number: {fibonacci_recursive(50)}")

    print("\n>>> Fibonacci Number Validation <<<")
    test_nums = [0, 1, 4, 5, 9, 13, 20, 21, 34, 100]
    for num in test_nums:
        status = "✅ YES" if is_fibonacci_number(num) else "❌ NO"
        print(f"   Is {num:<3} a Fibonacci number? {status}")

    print("\n>>> Golden Ratio Convergence <<<")
    golden_ratio_convergence(12)

    print("\n>>> Fibonacci Growth Visualization <<<")
    draw_fibonacci_spiral_blocks(8)

    print("\n>>> Interactive Explorer <<<")
    interactive_explorer()
    show_mastery_box()


if __name__ == "__main__":
    main()
