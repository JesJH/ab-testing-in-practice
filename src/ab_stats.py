"""
Reusable A/B testing utility functions.
Imported by notebooks throughout the project.
"""

import numpy as np
from scipy import stats


def sample_size_per_group(baseline_rate, mde, alpha=0.05, power=0.80):
    """
    Calculate required sample size per group for a two-proportion z-test.

    baseline_rate: control group conversion rate (e.g. 0.10 for 10%)
    mde: minimum detectable effect as absolute change (e.g. 0.02 for +2pp)
    alpha: significance level (default 0.05)
    power: desired statistical power (default 0.80)
    """
    treatment_rate = baseline_rate + mde
    pooled = (baseline_rate + treatment_rate) / 2

    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    n = (
        (z_alpha * np.sqrt(2 * pooled * (1 - pooled)) +
         z_beta * np.sqrt(baseline_rate * (1 - baseline_rate) + treatment_rate * (1 - treatment_rate))) ** 2
        / mde ** 2
    )
    return int(np.ceil(n))


def two_proportion_ztest(control_conversions, control_n, treatment_conversions, treatment_n):
    """
    Two-sided z-test for difference in proportions.
    Returns: (z_stat, p_value, control_rate, treatment_rate, lift_abs, lift_rel)
    """
    p_c = control_conversions / control_n
    p_t = treatment_conversions / treatment_n
    p_pool = (control_conversions + treatment_conversions) / (control_n + treatment_n)

    se = np.sqrt(p_pool * (1 - p_pool) * (1 / control_n + 1 / treatment_n))
    z = (p_t - p_c) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    lift_abs = p_t - p_c
    lift_rel = lift_abs / p_c

    return z, p_value, p_c, p_t, lift_abs, lift_rel


def confidence_interval(conversions, n, alpha=0.05):
    """Wilson score confidence interval for a proportion."""
    p = conversions / n
    z = stats.norm.ppf(1 - alpha / 2)
    denominator = 1 + z ** 2 / n
    center = (p + z ** 2 / (2 * n)) / denominator
    margin = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / denominator
    return center - margin, center + margin


def check_sample_ratio_mismatch(control_n, treatment_n, expected_split=0.5, alpha=0.01):
    """
    Chi-square test for sample ratio mismatch.
    Returns True if SRM is detected (bad — stop analysis).
    """
    total = control_n + treatment_n
    expected_control = total * expected_split
    expected_treatment = total * (1 - expected_split)

    chi2, p_value = stats.chisquare(
        [control_n, treatment_n],
        [expected_control, expected_treatment]
    )
    srm_detected = p_value < alpha
    return srm_detected, chi2, p_value
