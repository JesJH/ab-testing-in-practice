# A/B Testing in Practice

Built for deep learning and exploration of A/B testing using real data and working implementations. Every concept is implemented in Python, compared to industry practice, and interpreted in a business context.

## Project Goal

Cover the full experimentation lifecycle — from experiment design through statistical analysis to the advanced methods used at Meta, DoorDash, Netflix, and LinkedIn — with real datasets and reusable code.

## Datasets

**Primary: Landing Page Conversion**
- ~294k users, 12 columns
- Place at: `data/AB Testing Data.csv`
- Columns: user_id, timestamp, group, landing_page, converted, age, gender, location, session_duration, pages_visited, device_type, purchase_amount

**Secondary: Cookie Cats Mobile Game (Kaggle)**
- ~90k users, Day-1 and Day-7 retention metrics
- Place at: `data/cookie_cats.csv`

## Repo Structure

```
ab-testing-in-practice/
├── CLAUDE.md                              # This file
├── README.md                              # Public-facing overview
├── METHODS.md                             # Decision guide: situation → method → notebook
├── requirements.txt                       # Python dependencies
├── data/                                  # Raw data (gitignored)
├── notebooks/
│   ├── 01_experiment_design.ipynb         # Hypothesis, MDE, sample size, duration
│   ├── 02_sampling_randomization.ipynb    # Stratified, hash-based, bootstrap, bandits
│   ├── 03_data_validation.ipynb           # SRM, dedup, mismatches, baseline check
│   ├── 04_statistical_analysis.ipynb      # z-test, p-values, CIs, null distribution
│   ├── 05_practical_significance.ipynb    # Cohen's h, CI vs MDE, decision quadrants
│   ├── 06_segment_analysis.ipynb          # Device/gender, novelty, Simpson's Paradox
│   ├── 07_multiple_testing.ipynb          # Bonferroni, Holm, BH-FDR
│   ├── 08_business_impact.ipynb           # Revenue CIs, expected value, decision template
│   ├── 09_industry_methods.ipynb          # CUPED, delta method, sequential testing
│   ├── 10_advanced_designs.ipynb          # Switchback, interleaving, cluster randomization
│   └── 11_observational_methods.ipynb     # DiD, PSM, RDD, synthetic control (planned)
├── scripts/
│   └── generate_notebooks.py             # Generates notebooks 02-10 from Python source
└── src/
    └── ab_stats.py                        # Reusable stats utility functions
```

## Three Contexts

**Live experiment** (notebooks 01–10): randomization is happening now. Covers design, sampling, validation, analysis, and industry-grade methods.

**Historical / observational data** (notebook 11, planned): feature was already shipped. Covers causal inference methods for when you can't randomize.

**Sampling** (notebook 02): how to draw samples and assign groups — covered before data collection.

See [METHODS.md](METHODS.md) for a full decision guide.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Run notebooks 01 → 10 in order. Notebooks 03–10 depend on `data/ab_data_clean.csv` produced by notebook 03.

## Working Across Machines

- Data files are gitignored — place CSVs in `data/` after cloning (see dataset paths above)
- Regenerate notebooks at any time: `python scripts/generate_notebooks.py`
- `src/ab_stats.py` contains all shared functions imported by the notebooks

## Status

### Foundations
- [x] 01 Experiment Design
- [x] 02 Sampling & Randomization
- [x] 03 Data Validation
- [x] 04 Statistical Analysis
- [x] 05 Practical Significance
- [x] 06 Segment Analysis
- [x] 07 Multiple Testing
- [x] 08 Business Impact

### Industry-Grade Methods
- [x] 09 Industry Methods (CUPED, Delta Method, Sequential Testing)
- [x] 10 Advanced Designs (Switchback, Interleaving, Network Randomization)

### Observational / Historical Data
- [ ] 11 Observational Methods (DiD, PSM, RDD, Synthetic Control)
