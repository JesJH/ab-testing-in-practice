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


def cohens_h(p1, p2):
    """Cohen's h effect size for difference between two proportions."""
    return 2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2))


def bonferroni_correct(p_values, alpha=0.05):
    """
    Bonferroni correction for multiple comparisons.
    Returns adjusted alpha and array of booleans (True = reject H0).
    """
    p_values = np.array(p_values)
    adjusted_alpha = alpha / len(p_values)
    rejected = p_values < adjusted_alpha
    return adjusted_alpha, rejected, p_values * len(p_values)


def cuped_adjust(y, x):
    """
    CUPED variance reduction (Deng et al. 2013).
    Adjusts outcome y using pre-experiment covariate x.
    Returns (y_adjusted, theta, variance_reduction_pct).
    theta = Cov(Y, X) / Var(X) — the optimal linear coefficient.
    """
    theta = np.cov(y, x)[0, 1] / np.var(x)
    y_adj = y - theta * (x - np.mean(x))
    var_reduction = (1 - np.var(y_adj) / np.var(y)) * 100
    return y_adj, theta, var_reduction


def delta_method_ratio_test(y_c, x_c, y_t, x_t, alpha=0.05):
    """
    Two-sample test for difference in ratio metric R = mean(Y) / mean(X).
    Uses the delta method to correctly estimate variance of a ratio.
    Returns (R_c, R_t, diff, se_diff, z, p_value, ci_lo, ci_hi).
    """
    n_c, n_t = len(y_c), len(y_t)

    R_c = np.mean(y_c) / np.mean(x_c)
    R_t = np.mean(y_t) / np.mean(x_t)

    def ratio_var(y, x, R, n):
        mu_x = np.mean(x)
        cov = np.cov(y, x, ddof=1)[0, 1]
        return (np.var(y, ddof=1) / mu_x**2
                - 2 * R * cov / mu_x**2
                + R**2 * np.var(x, ddof=1) / mu_x**2) / n

    se_diff = np.sqrt(ratio_var(y_c, x_c, R_c, n_c) + ratio_var(y_t, x_t, R_t, n_t))
    z = (R_t - R_c) / se_diff
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    diff = R_t - R_c
    return R_c, R_t, diff, se_diff, z, p, diff - z_crit * se_diff, diff + z_crit * se_diff


def obrien_fleming_boundary(t, alpha=0.05):
    """
    O'Brien-Fleming alpha-spending boundary at information fraction t (0 < t <= 1).
    Returns the critical z-value — reject H0 if |z_observed| > this value.
    More conservative early in the experiment, converges to z_alpha/2 at t=1.
    """
    return stats.norm.ppf(1 - alpha / 2) / np.sqrt(t)


def benjamini_hochberg(p_values, alpha=0.05):
    """
    Benjamini-Hochberg FDR correction.
    Returns array of booleans (True = reject H0) and adjusted p-values.
    """
    p_values = np.array(p_values)
    n = len(p_values)
    order = np.argsort(p_values)
    ranks = np.arange(1, n + 1)

    adjusted = np.empty(n)
    adjusted[order] = p_values[order] * n / ranks

    # Enforce monotonicity: adjusted p-values must be non-decreasing from right
    for i in range(n - 2, -1, -1):
        adjusted[order[i]] = min(adjusted[order[i]], adjusted[order[i + 1]])

    adjusted = np.minimum(adjusted, 1.0)
    rejected = adjusted < alpha
    return rejected, adjusted
