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


if __name__ == "__main__":
    main()
