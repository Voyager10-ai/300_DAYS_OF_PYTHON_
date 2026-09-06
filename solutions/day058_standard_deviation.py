# Day 58: Standard Deviation
#
# Problem:
#   Write a Python program / module to calculate standard deviation and variance for datasets.
#   Includes population and sample formulas, Welford's single-pass online algorithm,
#   grouped data frequency tables, Z-score normalization & outlier detection,
#   Standard Error of the Mean (SEM) & confidence intervals, axis-wise matrix operations,
#   synthetic dataset generation, unit tests, and Java practice.

import math
import random
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Variance & Standard Deviation Functions ─────────────────────────


def calculate_mean(data: List[float]) -> float:
    """
    Calculates the arithmetic mean of a list of numbers.

    Args:
        data: List of numerical values.

    Returns:
        Arithmetic mean as a float.

    Raises:
        ValueError: If dataset is empty.
        TypeError: If dataset contains non-numeric elements.
    """
    if not data:
        raise ValueError("Cannot calculate mean of an empty dataset.")
    
    total = 0.0
    for val in data:
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise TypeError(f"Invalid element type {type(val).__name__} in dataset.")
        total += float(val)
    
    return total / len(data)


def calculate_variance(data: List[float], is_sample: bool = True) -> float:
    """
    Calculates the variance of a list of numbers.

    Args:
        data: List of numerical values.
        is_sample: If True, calculates sample variance (n - 1 degrees of freedom).
                   If False, calculates population variance (n degrees of freedom).

    Returns:
        Variance value as a float.

    Raises:
        ValueError: If data has fewer than 2 elements for sample, or is empty for population.
    """
    if not data:
        raise ValueError("Cannot calculate variance of an empty dataset.")
    
    n = len(data)
    if is_sample and n < 2:
        raise ValueError("Sample variance requires at least 2 data points.")

    mean = calculate_mean(data)
    sum_squared_diff = sum((x - mean) ** 2 for x in data)
    divisor = (n - 1) if is_sample else n
    
    return sum_squared_diff / divisor


def calculate_std_dev(data: List[float], is_sample: bool = True) -> float:
    """
    Calculates the standard deviation of a list of numbers.

    Args:
        data: List of numerical values.
        is_sample: If True, returns sample standard deviation (s).
                   If False, returns population standard deviation (sigma).

    Returns:
        Standard deviation value as a float.
    """
    var = calculate_variance(data, is_sample=is_sample)
    return math.sqrt(var)


# ─── 2. Welford's Single-Pass Online Accumulator ─────────────────────────────


class WelfordAccumulator:
    """
    Implements Welford's algorithm for computing streaming mean, variance, and
    standard deviation in a single numerical-stable pass without storing history.
    """

    def __init__(self) -> None:
        """Initializes an empty Welford accumulator."""
        self._count: int = 0
        self._mean: float = 0.0
        self._M2: float = 0.0  # Sum of squared differences from current mean

    def update(self, x: float) -> None:
        """
        Updates the accumulator with a new value x.

        Args:
            x: Numerical value to stream in.
        """
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError(f"Expected numeric input, got {type(x).__name__}")

        self._count += 1
        delta = x - self._mean
        self._mean += delta / self._count
        delta2 = x - self._mean
        self._M2 += delta * delta2

    def update_batch(self, data: List[float]) -> None:
        """
        Updates the accumulator with a list of values.

        Args:
            data: List of numerical values.
        """
        for val in data:
            self.update(val)

    @property
    def count(self) -> int:
        """Returns the number of elements processed."""
        return self._count

    @property
    def mean(self) -> float:
        """Returns the current streaming mean."""
        if self._count == 0:
            raise ValueError("No data points accumulated yet.")
        return self._mean

    @property
    def variance_sample(self) -> float:
        """Returns the current sample variance (s^2)."""
        if self._count < 2:
            raise ValueError("Sample variance requires at least 2 data points.")
        return self._M2 / (self._count - 1)

    @property
    def variance_population(self) -> float:
        """Returns the current population variance (sigma^2)."""
        if self._count < 1:
            raise ValueError("Population variance requires at least 1 data point.")
        return self._M2 / self._count

    @property
    def std_dev_sample(self) -> float:
        """Returns the current sample standard deviation (s)."""
        return math.sqrt(self.variance_sample)

    @property
    def std_dev_population(self) -> float:
        """Returns the current population standard deviation (sigma)."""
        return math.sqrt(self.variance_population)

    def reset(self) -> None:
        """Resets the accumulator state."""
        self._count = 0
        self._mean = 0.0
        self._M2 = 0.0


# ─── 3. Frequency Table / Grouped Data Standard Deviation ────────────────────


def calculate_grouped_mean(values: List[float], frequencies: List[int]) -> float:
    """
    Calculates the mean of grouped / frequency-table data.

    Args:
        values: List of midpoints or distinct values.
        frequencies: List of corresponding frequencies for each value.

    Returns:
        Weighted mean as a float.

    Raises:
        ValueError: If lists differ in length, are empty, or total frequency is <= 0.
    """
    if len(values) != len(frequencies):
        raise ValueError("Values and frequencies lists must have the same length.")
    if not values:
        raise ValueError("Cannot calculate mean of empty frequency dataset.")

    total_freq = sum(frequencies)
    if total_freq <= 0:
        raise ValueError("Total frequency must be greater than zero.")

    weighted_sum = sum(v * f for v, f in zip(values, frequencies))
    return weighted_sum / total_freq


def calculate_grouped_variance(
    values: List[float], frequencies: List[int], is_sample: bool = True
) -> float:
    """
    Calculates the variance of grouped / frequency-table data.

    Args:
        values: List of midpoints or distinct values.
        frequencies: List of corresponding frequencies.
        is_sample: If True, calculates sample variance. Else population.

    Returns:
        Grouped variance as a float.

    Raises:
        ValueError: If total frequency is insufficient (<= 1 for sample).
    """
    mean = calculate_grouped_mean(values, frequencies)
    total_freq = sum(frequencies)

    if is_sample and total_freq < 2:
        raise ValueError("Grouped sample variance requires a total frequency >= 2.")

    sum_sq_diff = sum(f * ((v - mean) ** 2) for v, f in zip(values, frequencies))
    divisor = (total_freq - 1) if is_sample else total_freq
    return sum_sq_diff / divisor


def calculate_grouped_std_dev(
    values: List[float], frequencies: List[int], is_sample: bool = True
) -> float:
    """
    Calculates the standard deviation of grouped / frequency-table data.

    Args:
        values: List of midpoints or distinct values.
        frequencies: List of corresponding frequencies.
        is_sample: If True, returns sample standard deviation. Else population.

    Returns:
        Grouped standard deviation as a float.
    """
    var = calculate_grouped_variance(values, frequencies, is_sample=is_sample)
    return math.sqrt(var)


# ─── 4. Z-Score Standardization & Outlier Detection ──────────────────────────


def calculate_z_scores(data: List[float], is_sample: bool = True) -> List[float]:
    """
    Calculates Z-scores (standard scores) for each element in a dataset.
    Z = (X - mean) / std_dev

    Args:
        data: List of numerical values.
        is_sample: If True, uses sample std dev. Else population std dev.

    Returns:
        List of Z-scores corresponding to each element in data.

    Raises:
        ValueError: If standard deviation is zero (all elements equal).
    """
    mean = calculate_mean(data)
    std_dev = calculate_std_dev(data, is_sample=is_sample)

    if std_dev == 0.0:
        raise ValueError("Standard deviation is zero; Z-score cannot be calculated (constant dataset).")

    return [(x - mean) / std_dev for x in data]


def detect_outliers_zscore(
    data: List[float], threshold: float = 3.0, is_sample: bool = True
) -> List[Tuple[int, float, float]]:
    """
    Identifies outliers in a dataset based on Z-score magnitude.

    Args:
        data: List of numerical values.
        threshold: Absolute Z-score threshold (default is 3.0).
        is_sample: If True, uses sample std dev. Else population.

    Returns:
        List of tuples: (index, value, z_score) for each detected outlier.
    """
    z_scores = calculate_z_scores(data, is_sample=is_sample)
    outliers = []
    for idx, (val, z) in enumerate(zip(data, z_scores)):
        if abs(z) >= threshold:
            outliers.append((idx, val, z))
    return outliers


# ─── 5. Standard Error of the Mean & Confidence Intervals ────────────────────


def calculate_sem(data: List[float], is_sample: bool = True) -> float:
    """
    Calculates the Standard Error of the Mean (SEM).
    SEM = std_dev / sqrt(n)

    Args:
        data: List of numerical values.
        is_sample: If True, uses sample standard deviation.

    Returns:
        Standard Error of the Mean as a float.

    Raises:
        ValueError: If data is empty.
    """
    if not data:
        raise ValueError("Cannot calculate SEM of an empty dataset.")
    std_dev = calculate_std_dev(data, is_sample=is_sample)
    return std_dev / math.sqrt(len(data))


def calculate_confidence_interval(
    data: List[float], confidence: float = 0.95, is_sample: bool = True
) -> Tuple[float, float]:
    """
    Calculates the confidence interval for the sample mean using standard normal Z-critical values.

    Supported confidence levels: 0.90 (Z=1.645), 0.95 (Z=1.960), 0.99 (Z=2.576).

    Args:
        data: List of numerical values.
        confidence: Confidence level (0.90, 0.95, or 0.99).
        is_sample: If True, uses sample standard deviation.

    Returns:
        Tuple of (lower_bound, upper_bound).

    Raises:
        ValueError: If unsupported confidence level is specified.
    """
    z_critical_map = {
        0.90: 1.6448536269514722,
        0.95: 1.959963984540054,
        0.99: 2.5758293035489004,
    }

    if confidence not in z_critical_map:
        raise ValueError(f"Unsupported confidence level {confidence}. Choose from {list(z_critical_map.keys())}.")

    mean = calculate_mean(data)
    sem = calculate_sem(data, is_sample=is_sample)
    margin_of_error = z_critical_map[confidence] * sem

    return (mean - margin_of_error, mean + margin_of_error)


# ─── 6. Multi-Column / Matrix Axis-Wise Standard Deviation ──────────────────


def matrix_std_dev(
    matrix: List[List[float]], axis: int = 0, is_sample: bool = True
) -> List[float]:
    """
    Computes standard deviation along a matrix axis.

    Args:
        matrix: 2D list of numbers (rows x cols).
        axis: 0 for column-wise std dev, 1 for row-wise std dev.
        is_sample: If True, calculates sample std dev.

    Returns:
        List of standard deviations for each slice along the specified axis.

    Raises:
        ValueError: If matrix is empty, irregular (ragged), or axis invalid.
    """
    if not matrix or not matrix[0]:
        raise ValueError("Matrix cannot be empty.")

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    for row in matrix:
        if len(row) != num_cols:
            raise ValueError("All rows in the matrix must have the same length.")

    if axis == 0:
        # Column-wise std dev
        col_std_devs = []
        for col_idx in range(num_cols):
            col_data = [matrix[row_idx][col_idx] for row_idx in range(num_rows)]
            col_std_devs.append(calculate_std_dev(col_data, is_sample=is_sample))
        return col_std_devs

    elif axis == 1:
        # Row-wise std dev
        return [calculate_std_dev(row, is_sample=is_sample) for row in matrix]

    else:
        raise ValueError(f"Invalid axis {axis}. Must be 0 (column-wise) or 1 (row-wise).")


def normalize_matrix_zscore(
    matrix: List[List[float]], axis: int = 0, is_sample: bool = True
) -> List[List[float]]:
    """
    Normalizes a 2D matrix by converting values to Z-scores along the specified axis.

    Args:
        matrix: 2D list of numbers (rows x cols).
        axis: 0 for column-wise normalization, 1 for row-wise normalization.
        is_sample: If True, uses sample std dev.

    Returns:
        New 2D matrix with Z-score normalized values.
    """
    if not matrix or not matrix[0]:
        raise ValueError("Matrix cannot be empty.")

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    if axis == 0:
        # Normalize each column
        normalized = [[0.0] * num_cols for _ in range(num_rows)]
        for j in range(num_cols):
            col = [matrix[i][j] for i in range(num_rows)]
            col_z = calculate_z_scores(col, is_sample=is_sample)
            for i in range(num_rows):
                normalized[i][j] = col_z[i]
        return normalized

    elif axis == 1:
        # Normalize each row
        return [calculate_z_scores(row, is_sample=is_sample) for row in matrix]

    else:
        raise ValueError(f"Invalid axis {axis}. Must be 0 or 1.")


# ─── 7. Synthetic Dataset Generator & Summary Engine ─────────────────────────


def generate_normal_dataset(
    n: int, target_mean: float = 0.0, target_std_dev: float = 1.0, seed: Optional[int] = None
) -> List[float]:
    """
    Generates a pseudo-random dataset approximating a normal distribution (Box-Muller transform).

    Args:
        n: Number of samples to generate (must be >= 2).
        target_mean: Target mean for distribution.
        target_std_dev: Target standard deviation for distribution.
        seed: Random seed for reproducibility.

    Returns:
        List of floats drawn from normal distribution.
    """
    if n < 2:
        raise ValueError("n must be at least 2 to generate distribution.")
    if target_std_dev < 0:
        raise ValueError("Target standard deviation cannot be negative.")

    if seed is not None:
        random.seed(seed)

    samples = []
    while len(samples) < n:
        u1 = random.random()
        u2 = random.random()
        # Avoid log(0)
        while u1 == 0:
            u1 = random.random()

        # Box-Muller transform
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        z1 = math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)

        samples.append(target_mean + z0 * target_std_dev)
        if len(samples) < n:
            samples.append(target_mean + z1 * target_std_dev)

    return samples


def summary_statistics(data: List[float]) -> Dict[str, float]:
    """
    Computes a comprehensive statistical summary dictionary for a dataset.

    Args:
        data: List of numerical values.

    Returns:
        Dictionary containing count, mean, sample_var, pop_var, sample_std, pop_std, sem, min, max, range.
    """
    if not data:
        raise ValueError("Cannot generate summary for an empty dataset.")

    n = len(data)
    mean_val = calculate_mean(data)
    sample_var = calculate_variance(data, is_sample=True) if n >= 2 else 0.0
    pop_var = calculate_variance(data, is_sample=False)
    sample_std = calculate_std_dev(data, is_sample=True) if n >= 2 else 0.0
    pop_std = calculate_std_dev(data, is_sample=False)
    sem_val = calculate_sem(data, is_sample=True) if n >= 2 else 0.0
    min_val = min(data)
    max_val = max(data)

    return {
        "count": float(n),
        "mean": mean_val,
        "sample_variance": sample_var,
        "population_variance": pop_var,
        "sample_std_dev": sample_std,
        "population_std_dev": pop_std,
        "sem": sem_val,
        "min": float(min_val),
        "max": float(max_val),
        "range": float(max_val - min_val),
    }


# ─── 8. Unit Tests ───────────────────────────────────────────────────────────


class TestStandardDeviationOperations(unittest.TestCase):
    """Unit tests for all standard deviation modules and helper functions."""

    def setUp(self) -> None:
        self.sample_data = [10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0]
        # Mean = 18.0
        # Sum((x - 18)^2) = 64 + 36 + 25 + 25 + 4 + 25 + 9 + 4 = 192.0
        # Pop Var = 192 / 8 = 24.0, Pop Std = sqrt(24) ~ 4.898979485566356
        # Sample Var = 192 / 7 = 27.428571428571427, Sample Std ~ 5.237225546830482

    def test_core_mean_variance_std_dev(self) -> None:
        self.assertAlmostEqual(calculate_mean(self.sample_data), 18.0)
        self.assertAlmostEqual(calculate_variance(self.sample_data, is_sample=False), 24.0)
        self.assertAlmostEqual(calculate_variance(self.sample_data, is_sample=True), 192.0 / 7.0)
        self.assertAlmostEqual(calculate_std_dev(self.sample_data, is_sample=False), math.sqrt(24.0))
        self.assertAlmostEqual(calculate_std_dev(self.sample_data, is_sample=True), math.sqrt(192.0 / 7.0))

    def test_welford_accumulator(self) -> None:
        acc = WelfordAccumulator()
        for x in self.sample_data:
            acc.update(x)
        
        self.assertEqual(acc.count, 8)
        self.assertAlmostEqual(acc.mean, 18.0)
        self.assertAlmostEqual(acc.variance_population, 24.0)
        self.assertAlmostEqual(acc.variance_sample, 192.0 / 7.0)
        self.assertAlmostEqual(acc.std_dev_population, math.sqrt(24.0))
        self.assertAlmostEqual(acc.std_dev_sample, math.sqrt(192.0 / 7.0))

        acc.reset()
        self.assertEqual(acc.count, 0)
        acc.update_batch(self.sample_data)
        self.assertAlmostEqual(acc.mean, 18.0)

    def test_grouped_data(self) -> None:
        values = [5.0, 15.0, 25.0]
        frequencies = [2, 5, 3]  # total = 10
        # Mean = (10 + 75 + 75) / 10 = 16.0
        # Sum sq diff = 2*(5-16)^2 + 5*(15-16)^2 + 3*(25-16)^2 = 2*121 + 5*1 + 3*81 = 242 + 5 + 243 = 490
        # Pop var = 490 / 10 = 49.0 -> std = 7.0
        # Sample var = 490 / 9 -> std = sqrt(490/9)
        self.assertAlmostEqual(calculate_grouped_mean(values, frequencies), 16.0)
        self.assertAlmostEqual(calculate_grouped_variance(values, frequencies, is_sample=False), 49.0)
        self.assertAlmostEqual(calculate_grouped_std_dev(values, frequencies, is_sample=False), 7.0)
        self.assertAlmostEqual(calculate_grouped_variance(values, frequencies, is_sample=True), 490.0 / 9.0)

    def test_z_scores_and_outliers(self) -> None:
        data = [10.0, 10.0, 10.0, 10.0, 100.0]
        z_scores = calculate_z_scores(data, is_sample=False)
        self.assertEqual(len(z_scores), 5)
        self.assertAlmostEqual(sum(z_scores), 0.0)  # Sum of Z-scores is always 0

        outliers = detect_outliers_zscore(data, threshold=1.5, is_sample=False)
        self.assertEqual(len(outliers), 1)
        self.assertEqual(outliers[0][0], 4)
        self.assertEqual(outliers[0][1], 100.0)

    def test_sem_and_confidence_intervals(self) -> None:
        sem = calculate_sem(self.sample_data, is_sample=False)
        expected_sem = math.sqrt(24.0) / math.sqrt(8)
        self.assertAlmostEqual(sem, expected_sem)

        ci_low, ci_high = calculate_confidence_interval(self.sample_data, confidence=0.95, is_sample=True)
        self.assertTrue(ci_low < 18.0 < ci_high)

    def test_matrix_std_dev_and_norm(self) -> None:
        matrix = [
            [1.0, 10.0],
            [3.0, 20.0],
            [5.0, 30.0],
        ]
        # col 0: [1, 3, 5], mean=3, pop_var=((4+0+4)/3)=8/3, pop_std=sqrt(8/3)
        col_std = matrix_std_dev(matrix, axis=0, is_sample=False)
        self.assertAlmostEqual(col_std[0], math.sqrt(8.0 / 3.0))

        row_std = matrix_std_dev(matrix, axis=1, is_sample=False)
        self.assertEqual(len(row_std), 3)

        norm_mat = normalize_matrix_zscore(matrix, axis=0, is_sample=False)
        # Column 0 Z-scores for [1, 3, 5]: (1-3)/std, (3-3)/std, (5-3)/std
        self.assertAlmostEqual(norm_mat[1][0], 0.0)

    def test_dataset_generator_and_summary(self) -> None:
        ds = generate_normal_dataset(n=100, target_mean=50.0, target_std_dev=5.0, seed=42)
        self.assertEqual(len(ds), 100)
        summary = summary_statistics(ds)
        self.assertEqual(summary["count"], 100.0)
        self.assertAlmostEqual(summary["mean"], 50.0, delta=1.5)

    def test_edge_cases_and_exceptions(self) -> None:
        with self.assertRaises(ValueError):
            calculate_mean([])
        with self.assertRaises(ValueError):
            calculate_variance([5.0], is_sample=True)
        with self.assertRaises(ValueError):
            calculate_z_scores([5.0, 5.0, 5.0])
        with self.assertRaises(TypeError):
            calculate_mean([1, "invalid", 3])


# ─── 9. Interactive CLI Runner ───────────────────────────────────────────────


def main() -> None:
    """Demonstrates all standard deviation capabilities with rich outputs."""
    print("=" * 70)
    print(" DAY 58: STANDARD DEVIATION & STATISTICAL VARIANCE TOOLKIT")
    print("=" * 70)

    raw_data = [10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0]
    print(f"\n1. Raw Sample Data ({len(raw_data)} points): {raw_data}")
    
    mean_val = calculate_mean(raw_data)
    sample_var = calculate_variance(raw_data, is_sample=True)
    pop_var = calculate_variance(raw_data, is_sample=False)
    sample_std = calculate_std_dev(raw_data, is_sample=True)
    pop_std = calculate_std_dev(raw_data, is_sample=False)

    print(f"   • Mean (x̄): {mean_val:.4f}")
    print(f"   • Sample Variance (s²): {sample_var:.4f}")
    print(f"   • Population Variance (σ²): {pop_var:.4f}")
    print(f"   • Sample Std Dev (s): {sample_std:.4f}")
    print(f"   • Population Std Dev (σ): {pop_std:.4f}")

    print("\n2. Streaming Welford Accumulator:")
    acc = WelfordAccumulator()
    for item in raw_data:
        acc.update(item)
    print(f"   • Count: {acc.count}")
    print(f"   • Streaming Mean: {acc.mean:.4f}")
    print(f"   • Streaming Sample Std Dev: {acc.std_dev_sample:.4f}")

    print("\n3. Grouped Frequency Data:")
    values = [5.0, 15.0, 25.0]
    freqs = [2, 5, 3]
    grp_mean = calculate_grouped_mean(values, freqs)
    grp_std = calculate_grouped_std_dev(values, freqs, is_sample=True)
    print(f"   • Midpoints: {values}, Frequencies: {freqs}")
    print(f"   • Grouped Mean: {grp_mean:.4f}")
    print(f"   • Grouped Sample Std Dev: {grp_std:.4f}")

    print("\n4. Z-Scores & Outlier Detection:")
    data_with_outlier = [10.0, 12.0, 11.0, 10.5, 12.5, 95.0]
    z_scores = calculate_z_scores(data_with_outlier)
    outliers = detect_outliers_zscore(data_with_outlier, threshold=2.0)
    print(f"   • Dataset: {data_with_outlier}")
    print(f"   • Z-Scores: {[round(z, 2) for z in z_scores]}")
    print(f"   • Outliers (|Z| >= 2.0): {outliers}")

    print("\n5. Standard Error of the Mean (SEM) & 95% Confidence Interval:")
    sem = calculate_sem(raw_data)
    ci_low, ci_high = calculate_confidence_interval(raw_data, confidence=0.95)
    print(f"   • SEM: {sem:.4f}")
    print(f"   • 95% CI for Mean: [{ci_low:.4f}, {ci_high:.4f}]")

    print("\n6. Matrix Column-wise Standard Deviation:")
    mat = [[1.0, 10.0], [3.0, 20.0], [5.0, 30.0]]
    mat_std = matrix_std_dev(mat, axis=0, is_sample=True)
    print(f"   • Matrix: {mat}")
    print(f"   • Column Sample Std Devs: {[round(s, 4) for s in mat_std]}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    unittest.main(exit=False)
    print()
    main()








