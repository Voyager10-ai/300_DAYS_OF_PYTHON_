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


# ─── 3. Streak Target Simulator ────────────────────────────────────────────────


def simulate_streaks(
    target_streak: int,
    target_outcome: str = "Heads",
    bias: float = 0.5,
    seed: Optional[int] = None,
    max_flips: int = 100000,
) -> Tuple[int, List[str]]:
    """
    Simulates coin flips until a target consecutive streak length of target_outcome is achieved.

    Args:
        target_streak: Target consecutive streak length (e.g. 5 consecutive Heads).
        target_outcome: 'Heads' or 'Tails'.
        bias: Probability of Heads.
        seed: Optional random seed.
        max_flips: Safety limit to prevent infinite loops.

    Returns:
        Tuple of (total_flips_required, flip_history_sequence).

    Raises:
        ValueError: If parameters are out of valid bounds.
    """
    if target_streak < 1:
        raise ValueError(f"Target streak must be >= 1, got {target_streak}")
    if target_outcome not in ("Heads", "Tails"):
        raise ValueError(f"Target outcome must be 'Heads' or 'Tails', got {target_outcome}")

    if seed is not None:
        random.seed(seed)

    history: List[str] = []
    current_streak = 0

    for _ in range(max_flips):
        flip = flip_coin(bias=bias)
        history.append(flip)

        if flip == target_outcome:
            current_streak += 1
            if current_streak == target_streak:
                return len(history), history
        else:
            current_streak = 0

    return len(history), history


# ─── 4. Binomial Coin Probability Model ────────────────────────────────────────


class BinomialCoinModel:
    """
    Theoretical Binomial distribution model for coin flipping experiments.
    Evaluates probability mass function (PMF), cumulative distribution (CDF),
    expected mean, variance, and standard deviation.
    """

    def __init__(self, n_flips: int, p_heads: float = 0.5):
        if n_flips < 0:
            raise ValueError(f"Number of flips must be >= 0, got {n_flips}")
        if not (0.0 <= p_heads <= 1.0):
            raise ValueError(f"Probability p must be in [0, 1], got {p_heads}")

        self.n = n_flips
        self.p = p_heads

    def pmf(self, k: int) -> float:
        """
        Calculates Probability Mass Function P(X = k) = C(n, k) * p^k * (1-p)^(n-k).
        """
        if not (0 <= k <= self.n):
            return 0.0

        comb = math.comb(self.n, k)
        return comb * (self.p ** k) * ((1.0 - self.p) ** (self.n - k))

    def cdf(self, k: int) -> float:
        """
        Calculates Cumulative Distribution Function P(X <= k).
        """
        if k < 0:
            return 0.0
        if k >= self.n:
            return 1.0

        return sum(self.pmf(j) for j in range(k + 1))

    @property
    def mean(self) -> float:
        """Expected mean E[X] = n * p."""
        return self.n * self.p

    @property
    def variance(self) -> float:
        """Variance Var(X) = n * p * (1-p)."""
        return self.n * self.p * (1.0 - self.p)

    @property
    def std_dev(self) -> float:
        """Standard deviation SD(X) = sqrt(n * p * (1-p))."""
        return math.sqrt(self.variance)


# ─── 5. Hypothesis Testing for Coin Fairness ───────────────────────────────────


def test_coin_fairness(heads_count: int, total_flips: int, alpha: float = 0.05) -> Dict[str, Any]:
    """
    Performs Chi-Square Goodness-of-Fit and Z-Test for proportion to evaluate coin fairness.

    Null Hypothesis (H0): The coin is fair (p = 0.5).
    Alternative Hypothesis (H1): The coin is biased (p != 0.5).

    Args:
        heads_count: Number of observed Heads.
        total_flips: Total number of flips (total_flips > 0).
        alpha: Significance level (default 0.05).

    Returns:
        Dictionary containing Chi-Square stat, Z-score, p-hat, and decision verdict.

    Raises:
        ValueError: If inputs are invalid.
    """
    if total_flips <= 0:
        raise ValueError(f"Total flips must be > 0, got {total_flips}")
    if not (0 <= heads_count <= total_flips):
        raise ValueError(f"Heads count {heads_count} out of range [0, {total_flips}]")

    tails_count = total_flips - heads_count
    expected_heads = total_flips * 0.5
    expected_tails = total_flips * 0.5

    # Chi-Square Statistic: sum((O - E)^2 / E)
    chi2_stat = (((heads_count - expected_heads) ** 2) / expected_heads) + (
        ((tails_count - expected_tails) ** 2) / expected_tails
    )

    # Z-Statistic for one-sample proportion test: (p_hat - p0) / sqrt(p0*(1-p0)/n)
    p_hat = heads_count / total_flips
    z_stat = (p_hat - 0.5) / math.sqrt(0.25 / total_flips)

    # Critical Chi2 value for df=1 at alpha=0.05 is ~3.841, alpha=0.01 is ~6.635
    critical_chi2_05 = 3.8415
    is_fair = chi2_stat <= critical_chi2_05

    return {
        "total_flips": total_flips,
        "observed_heads": heads_count,
        "observed_tails": tails_count,
        "sample_proportion_heads": round(p_hat, 4),
        "chi2_stat": round(chi2_stat, 4),
        "z_stat": round(z_stat, 4),
        "alpha": alpha,
        "null_hypothesis_accepted": is_fair,
        "verdict": "Fair Coin (Fail to reject H0)" if is_fair else "Biased Coin (Reject H0)",
    }




