# Methods Guide

Use this guide to find the right approach for your situation.

---

## Context 1: Live Experiment (Randomization Is Happening Now)

You are assigning users to groups in real time and collecting data as the experiment runs.

### Design
| Question | Answer | Notebook |
|---|---|---|
| How many users do I need? | Sample size calculation (MDE, power, α) | 01 |
| How do I split users fairly? | Stratified randomization | 02 |
| How do I assign groups in production? | Hash-based assignment | 02 |
| Can I peek at results as data comes in? | Sequential testing (OBF / mSPRT) | 09 |

### Data Quality (Before Analyzing)
| Check | What to look for | Notebook |
|---|---|---|
| Sample ratio mismatch | Is the actual split close to the intended split? Chi-square test, p < 0.01 = problem | 03 |
| Duplicate users | Same user appearing multiple times — keep first record only | 03 |
| Mismatched assignments | User in "treatment" group but saw "control" experience (or vice versa) | 03 |
| Novelty effect | Does the treatment effect shrink over time? Check weekly breakdown | 06 |
| SRM by segment | Is the split balanced within device type, country, etc.? | 03, 06 |

### Live Data Checklist
Before calling a result:
- [ ] SRM check passed (chi-square p > 0.01)
- [ ] No duplicate user IDs
- [ ] No mismatched page/group assignments
- [ ] Experiment ran for at least 1 full week (weekly seasonality)
- [ ] End date was committed to before launch (no peeking)
- [ ] Primary metric pre-specified (not chosen after seeing results)
- [ ] Guardrail metrics checked

### Analysis
| Situation | Method | Notebook |
|---|---|---|
| Binary outcome (conversion rate) | Two-proportion z-test | 04 |
| Continuous outcome (revenue, time) | Two-sample t-test | 04 |
| Ratio metric (revenue/session, CTR) | Delta method — NOT a standard z-test | 09 |
| Skewed metric (median, 90th pct) | Bootstrapping | 02 |
| Many segments tested | Bonferroni or BH-FDR correction | 07 |
| Variance too high / test too slow | CUPED with pre-experiment covariate | 09 |
| Marketplace / two-sided platform | Switchback experiment | 10 |
| Ranking / recommendation algorithm | Interleaving | 10 |
| Social / network feature | Cluster randomization | 10 |

### Interpreting Results
| Result | What it means | Action |
|---|---|---|
| p < α, CI excludes 0, lift > MDE | Statistically and practically significant | Ship |
| p < α, lift < MDE | Statistically significant but practically insignificant | Probably don't ship |
| p > α, CI excludes MDE | Not significant, effect ruled out | Don't ship |
| p > α, CI includes MDE | Inconclusive — can't rule out a real effect | Rerun with more data |
| p > α, power too low | Underpowered — result is uninformative | Rerun with correct sample size |

---

## Context 2: Historical / Observational Data (No Randomization)

You have data from a feature that was shipped, a natural event, or a non-randomized rollout.
The key challenge: **selection bias** — the treated and untreated groups differ in ways you can't
fully observe. No statistical test fixes a bad comparison group.

| Situation | Method | When it works |
|---|---|---|
| You have a before/after period + untreated comparison group | Difference-in-Differences (DiD) | Parallel trends assumption holds |
| You have rich user features, no assignment | Propensity Score Matching (PSM) | No unobserved confounders |
| Treatment assigned by a score threshold | Regression Discontinuity (RDD) | Units near cutoff are comparable |
| Geo or city-level rollout | Synthetic Control | Good pre-treatment fit of control group |
| Instrument that predicts treatment but not outcome | Instrumental Variables (IV) | Valid instrument exists |

> Notebook 11 (planned): Observational Methods — DiD, PSM, RDD, Synthetic Control

---

## Context 3: Sampling

How you draw your sample and assign users affects everything downstream.

| Need | Method | Notebook |
|---|---|---|
| Basic assignment | Simple random sampling | 02 |
| Guaranteed balance on device/country | Stratified randomization | 02 |
| Production assignment at scale | Hash-based (MD5/MurmurHash) | 02 |
| CI on skewed or non-standard metric | Bootstrapping | 02 |
| Minimize user cost during experiment | Multi-armed bandit (Thompson Sampling) | 02 |

---

## Metric Selection & Tradeoffs

> Notebook 11 (planned): covers metric selection, counter-metrics, and tradeoff valuation.

Quick reference:

| Situation | Approach |
|---|---|
| Treatment improves primary metric but hurts a guardrail | Do not ship — investigate root cause |
| Two metrics move in opposite directions (tradeoff) | Define a composite metric or business value function |
| Hard to pick one primary metric | Use OEC (Overall Evaluation Criterion) — weighted sum |
| Metric moves but you don't know if it's causal | Check for novelty effect, segment confounders, SRM |
