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


# ─── 2. Coin Flip Sequence & Streak Analyzer ───────────────────────────────────


def analyze_coin_flips(flips: List[str]) -> Dict[str, Any]:
    """
    Analyzes a sequence of coin flips for statistical properties and streak metrics.

    Args:
        flips: List of 'Heads' / 'Tails' strings.

    Returns:
        Dictionary containing counts, percentages, max streak lengths, and state transitions.

    Raises:
        ValueError: If flips list is empty.
    """
    if not isinstance(flips, list):
        raise TypeError(f"Expected list of flips, got {type(flips).__name__}")
    if not flips:
        raise ValueError("Flips list cannot be empty")

    total = len(flips)
    heads_count = flips.count("Heads")
    tails_count = flips.count("Tails")

    max_heads_streak = 0
    max_tails_streak = 0
    curr_streak_val = None
    curr_streak_len = 0

    transitions = {"H_to_H": 0, "H_to_T": 0, "T_to_H": 0, "T_to_T": 0}

    for i, flip in enumerate(flips):
        # Streak tracking
        if flip == curr_streak_val:
            curr_streak_len += 1
        else:
            curr_streak_val = flip
            curr_streak_len = 1

        if flip == "Heads":
            max_heads_streak = max(max_heads_streak, curr_streak_len)
        elif flip == "Tails":
            max_tails_streak = max(max_tails_streak, curr_streak_len)

        # Transition tracking
        if i > 0:
            prev = flips[i - 1]
            if prev == "Heads" and flip == "Heads":
                transitions["H_to_H"] += 1
            elif prev == "Heads" and flip == "Tails":
                transitions["H_to_T"] += 1
            elif prev == "Tails" and flip == "Heads":
                transitions["T_to_H"] += 1
            elif prev == "Tails" and flip == "Tails":
                transitions["T_to_T"] += 1

    return {
        "total_flips": total,
        "heads_count": heads_count,
        "tails_count": tails_count,
        "heads_percentage": round((heads_count / total) * 100, 2),
        "tails_percentage": round((tails_count / total) * 100, 2),
        "max_heads_streak": max_heads_streak,
        "max_tails_streak": max_tails_streak,
        "transitions": transitions,
    }

