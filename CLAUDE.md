# A/B Testing in Practice

A portfolio project demonstrating end-to-end A/B testing — from experiment design through statistical analysis to business impact quantification.

## Project Goal

Showcase the full A/B testing lifecycle using real public datasets, with emphasis on correct statistical interpretation and translating results into business decisions.

## Datasets

**Primary: Landing Page Conversion (Kaggle)**
- ~300k users, binary outcome (converted / not converted)
- Place at: `data/AB Testing Data.csv`
- Columns: user_id, timestamp, group, landing_page, converted, age, gender, location, session_duration, pages_visited, device_type, purchase_amount

**Secondary: Cookie Cats Mobile Game (Kaggle)**
- ~90k users, Day-1 and Day-7 retention metrics
- Download from: https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing
- Place at: `data/cookie_cats.csv`

## Repo Structure

```
ab-testing-in-practice/
├── CLAUDE.md                         # This file
├── README.md                         # Public-facing overview
├── requirements.txt                  # Python dependencies
├── data/                             # Raw data (gitignored)
├── notebooks/
│   ├── 01_experiment_design.ipynb    # Hypothesis, metrics, framing
│   ├── 02_data_validation.ipynb      # SRM checks, AA test validity
│   ├── 03_statistical_analysis.ipynb # z-test, t-test, p-values, CIs
│   ├── 04_practical_significance.ipynb # Effect size, MDE, lift vs. noise
│   ├── 05_segment_analysis.ipynb     # Breakdown by device, cohort, etc.
│   ├── 06_multiple_testing.ipynb     # Bonferroni, FDR correction
│   └── 07_business_impact.ipynb      # Translating lift % to revenue/users
└── src/
    └── ab_stats.py                   # Reusable stats utility functions
```

## Concepts Covered

1. Experiment framing (null/alternative hypothesis, primary metric)
2. Pre-experiment checks (sample ratio mismatch, AA test)
3. Sample size & statistical power (MDE, why underpowered tests mislead)
4. Statistical significance (p-values, confidence intervals, choosing the right test)
5. Practical significance (significant ≠ worth shipping)
6. Segment analysis (does the effect hold across subgroups?)
7. Multiple testing correction (Bonferroni, Benjamini-Hochberg FDR)
8. Business impact quantification (lift → revenue → decision)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Working Across Machines

- Data files are gitignored — download from Kaggle links above after cloning
- Notebooks are numbered and meant to be worked through in order
- `src/ab_stats.py` contains shared functions imported by the notebooks

## Status

- [x] 01 Experiment Design
- [x] 02 Data Validation
- [x] 03 Statistical Analysis
- [x] 04 Practical Significance
- [x] 05 Segment Analysis
- [x] 06 Multiple Testing
- [x] 07 Business Impact
- [x] 08 Industry-Grade Methods (CUPED, Delta Method, Sequential Testing)
- [x] 09 Advanced Experiment Designs (Switchback, Interleaving, Network Randomization)
