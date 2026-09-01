# Day 55: Flip a Coin
#
# Problem:
#   Write a Python program / module to simulate flipping a coin.
#   Includes fair & biased coin flips, batch simulation, sequence streak analysis, binomial distribution modeling,
#   hypothesis testing for coin fairness (chi-square/z-test), 1D random walk & Gambler's Ruin, multi-outcome weighted coins, unit tests, and Java practice.

import math
import random
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Coin Simulator ───────────────────────────────────────────────────


def flip_coin(bias: float = 0.5, seed: Optional[int] = None) -> str:
    """
    Simulates a single coin flip.

    Args:
        bias: Probability of getting 'Heads' (0.0 <= bias <= 1.0). Default 0.5 (fair coin).
        seed: Optional random seed for deterministic testing.

    Returns:
        'Heads' or 'Tails'.

    Raises:
        ValueError: If bias is not between 0.0 and 1.0 inclusive.
    """
    if not isinstance(bias, (int, float)):
        raise TypeError(f"Expected float/int bias, got {type(bias).__name__}")
    if not (0.0 <= bias <= 1.0):
        raise ValueError(f"Bias must be between 0.0 and 1.0 inclusive, got {bias}")

    if seed is not None:
        random.seed(seed)

    return "Heads" if random.random() < bias else "Tails"


def flip_coins_batch(count: int, bias: float = 0.5, seed: Optional[int] = None) -> List[str]:
    """
    Simulates a batch of N coin flips.

    Args:
        count: Number of coin flips to perform (count >= 1).
        bias: Probability of getting 'Heads'.
        seed: Optional random seed.

    Returns:
        List of 'Heads' / 'Tails' outcomes.

    Raises:
        ValueError: If count < 1.
    """
    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError(f"Expected integer count, got {type(count).__name__}")
    if count < 1:
        raise ValueError(f"Count must be at least 1, got {count}")

    if seed is not None:
        random.seed(seed)

    return ["Heads" if random.random() < bias else "Tails" for _ in range(count)]
