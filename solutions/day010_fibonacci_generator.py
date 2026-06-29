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


if __name__ == "__main__":
    main()
