"""Chapter 30: the two-proportion summary used in section 30.9, as a function that can be tested."""
import numpy as np
from statsmodels.stats.proportion import proportions_ztest


def two_proportion_summary(k_a: int, n_a: int, k_b: int, n_b: int) -> dict:
    """Compare group B's rate with group A's: the difference, its 95% interval, and the p-value."""
    p_a, p_b = k_a / n_a, k_b / n_b
    diff = p_b - p_a
    se = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    z, p_value = proportions_ztest([k_b, k_a], [n_b, n_a])
    return {"diff": diff, "ci_low": diff - 1.96 * se, "ci_high": diff + 1.96 * se, "p_value": p_value}
