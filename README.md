# A/B Testing in Practice

> **Built for learning and exploring A/B testing in depth** — using real data, working implementations, and business commentary at every step. This is not a textbook summary. Every concept is implemented in Python against a real dataset, compared to industry practice, and interpreted in a business context.

An end-to-end portfolio covering the full experimentation lifecycle — from experiment design and statistical rigor to the methods used inside Meta, DoorDash, Netflix, and LinkedIn.

---

## Navigation

See [METHODS.md](METHODS.md) for a decision guide: given your situation, which method to use and which notebook covers it.

### Foundations

| Notebook | Topic | Key concepts |
|---|---|---|
| [01](notebooks/01_experiment_design.ipynb) | Experiment Design | Hypothesis, MDE, sample size, test duration, peeking problem |
| [02](notebooks/02_sampling_randomization.ipynb) | Sampling & Randomization | Stratified randomization, hash-based assignment, bootstrapping, multi-armed bandits |
| [03](notebooks/03_data_validation.ipynb) | Data Validation | SRM check, deduplication, mismatched assignments, baseline sanity |
| [04](notebooks/04_statistical_analysis.ipynb) | Statistical Analysis | z-test, p-value interpretation, confidence intervals, null distribution |
| [05](notebooks/05_practical_significance.ipynb) | Practical Significance | Cohen's h, CI vs MDE, four-quadrant decision framework |
| [06](notebooks/06_segment_analysis.ipynb) | Segment Analysis | Device/gender breakdown, novelty effect, Simpson's Paradox, interaction effects |
| [07](notebooks/07_multiple_testing.ipynb) | Multiple Testing | FWER, Bonferroni, Holm, Benjamini-Hochberg FDR |
| [08](notebooks/08_business_impact.ipynb) | Business Impact | Revenue CI, expected value framework, decision narrative, write-up template |

### Industry-Grade Methods (Live Experiments)

| Notebook | Topic | Key concepts |
|---|---|---|
| [09](notebooks/09_industry_methods.ipynb) | Industry Methods | CUPED (LinkedIn/Netflix), delta method (Meta/Airbnb), sequential testing (Spotify) |
| [10](notebooks/10_advanced_designs.ipynb) | Advanced Designs | Switchback (DoorDash/Lyft), interleaving (Netflix/Spotify), cluster randomization (Meta/LinkedIn) |

### When You Can't Randomize *(planned)*

| Notebook | Topic |
|---|---|
| 11 | Observational Methods — Difference-in-Differences, Propensity Score Matching, RDD, Synthetic Control |

---

## Three Contexts for A/B Testing

**Live experiment** — users are being assigned in real time. Use notebooks 01–10.
Key concerns: SRM, peeking, novelty effects, ratio metric variance.

**Historical / observational data** — feature was already shipped, no randomization.
Selection bias is the core problem. Use causal inference methods (notebook 11, planned).

**Sampling** — how you draw your sample and assign groups affects all downstream analysis.
Covered in notebook 02 before any data collection happens.

---

## Datasets

**Landing page conversion** (`data/AB Testing Data.csv`)
~294k users, 12 columns including `device_type`, `gender`, `purchase_amount`.
Binary outcome (converted / not converted).

**Cookie Cats mobile game** (`data/cookie_cats.csv`)
~90k users. Day-1 and Day-7 retention after gate placement experiment (level 30 vs 40).

Data files are gitignored — download from Kaggle (see [CLAUDE.md](CLAUDE.md) for links).

---

## Setup

```bash
git clone https://github.com/JesJH/ab-testing-in-practice.git
cd ab-testing-in-practice
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Run notebooks in order. Notebooks 03–10 depend on `data/ab_data_clean.csv` produced by notebook 03.

## Reusable Code

`src/ab_stats.py` — importable functions used across all notebooks:

| Function | What it does |
|---|---|
| `sample_size_per_group` | Required N given MDE, power, alpha |
| `two_proportion_ztest` | z-test for conversion rate difference |
| `confidence_interval` | Wilson score CI for a proportion |
| `check_sample_ratio_mismatch` | Chi-square SRM test |
| `cohens_h` | Effect size for proportions |
| `cuped_adjust` | CUPED variance reduction |
| `delta_method_ratio_test` | Correct SE for ratio metrics |
| `obrien_fleming_boundary` | Sequential testing critical values |
| `bonferroni_correct` | Bonferroni multiple testing correction |
| `benjamini_hochberg` | BH false discovery rate correction |
