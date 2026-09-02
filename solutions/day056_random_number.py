# Day 56: Random Number
#
# Problem:
#   Write a Python program / module to generate random numbers.
#   Includes custom LCG engine, uniform integer/float generators, list & 2D matrix sampling,
#   Gaussian/Normal (Box-Muller) & Exponential probability distributions, statistical analysis & Chi-Square test,
#   Fisher-Yates shuffle & sampling, cryptographically secure generation, unit tests, and Java practice.

import math
import random
import secrets
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union, TypeVar

T = TypeVar("T")


# ─── 1. Custom Linear Congruential Generator (LCG) Engine ───────────────────────


class CustomLCG:
    """
    Implements a Linear Congruential Generator (LCG) pseudorandom number generator:
    X_{n+1} = (a * X_n + c) mod m

    Uses standard Numerical Recipes parameters:
    m = 2^32, a = 1664525, c = 1013904223
    """

    def __init__(self, seed: int = 123456789, m: int = 2**32, a: int = 1664525, c: int = 1013904223):
        if m <= 0:
            raise ValueError(f"Modulus m must be > 0, got {m}")
        self.m = m
        self.a = a
        self.c = c
        self.state = seed % m

    def next_int(self, min_val: int = 0, max_val: int = 100) -> int:
        """Generates a random integer in range [min_val, max_val]."""
        if min_val > max_val:
            raise ValueError(f"min_val ({min_val}) cannot be > max_val ({max_val})")
        self.state = (self.a * self.state + self.c) % self.m
        span = max_val - min_val + 1
        return min_val + (self.state % span)

    def next_float(self) -> float:
        """Generates a random float in range [0.0, 1.0)."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m
