# A/B Testing in Practice

> Built for learning and exploring A/B testing end-to-end — using real data, working Python implementations, and business commentary at every step.

An end-to-end portfolio covering the full experimentation lifecycle: from experiment design and statistical rigor to the advanced methods used inside Meta, DoorDash, Netflix, and LinkedIn.

---

## Goal

Most A/B testing resources stop at p-values. This project goes further:

- **Design experiments correctly** before touching data — hypothesis, metric selection, sample size, test duration
- **Validate data quality** before drawing conclusions — SRM checks, deduplication, mismatched assignments
- **Understand the statistics** deeply — not just whether p < 0.05, but what it means and when it's not enough
- **Reason about practical significance** — a statistically significant result that's too small to matter should not be shipped
- **Apply industry-grade methods** — CUPED for variance reduction, delta method for ratio metrics, sequential testing for early stopping
- **Handle advanced experiment designs** — switchback experiments, interleaving, network randomization
- **Know when you can't randomize** — causal inference methods for historical data

---

## Methodology

The full decision guide — given your situation, which method to use, and which notebook covers it — is in [docs/METHODS.md](docs/METHODS.md).

### Key steps in the analysis process

1. **Design** — define the hypothesis, select the primary metric and guardrails, calculate required sample size and test duration
2. **Sample & randomize** — assign users to groups; check for confounders; verify covariate balance
3. **Validate** — confirm data integrity before any analysis (SRM, duplicates, assignment mismatches)
4. **Analyze** — run the appropriate statistical test; compute confidence intervals; check power
5. **Interpret** — distinguish statistical significance from practical significance; apply corrections for multiple comparisons
6. **Decide** — quantify business impact; weigh guardrail metrics; make a ship/no-ship call with a written rationale

---

## Project Structure

```
ab-testing-deepdive/
├── README.md
├── CLAUDE.md                           # Project instructions for Claude Code
├── requirements.txt
├── docs/
│   └── METHODS.md                      # Decision guide: situation → method → notebook
├── data/                               # Raw data (gitignored — see Caveats)
├── notebooks/
│   ├── 01_experiment_design.ipynb      # Hypothesis, MDE, sample size, duration
│   ├── 02_sampling_randomization.ipynb # Confounders, stratified, hash-based, ANCOVA, bandits
│   ├── 03_data_validation.ipynb        # SRM, dedup, mismatches, baseline check
│   ├── 04_statistical_analysis.ipynb   # z-test, p-values, CIs, null distribution
│   ├── 05_practical_significance.ipynb # Cohen's h, CI vs MDE, decision quadrants
│   ├── 06_segment_analysis.ipynb       # Device/gender, novelty effect, Simpson's Paradox
│   ├── 07_multiple_testing.ipynb       # Bonferroni, Holm, Benjamini-Hochberg FDR
│   ├── 08_business_impact.ipynb        # Revenue CIs, expected value, decision template
│   ├── 09_industry_methods.ipynb       # CUPED, delta method, sequential testing
│   └── 10_advanced_designs.ipynb       # Switchback, interleaving, cluster randomization
├── scripts/
│   └── generate_notebooks.py           # Regenerates notebooks 02-10 from Python source
└── src/
    └── ab_stats.py                     # Reusable stats utility functions
```

Run notebooks in order. Notebooks 03–10 depend on `data/ab_data_clean.csv` produced by notebook 03.

---

## Setup

```bash
git clone https://github.com/JesJH/ab-testing-deepdive.git
cd ab-testing-deepdive
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

To regenerate any notebook from source:

```bash
python scripts/generate_notebooks.py
```

---

## Caveats

**Data is not included in the repo.** Place the following files in `data/` after cloning:

| File | Source | Description |
|---|---|---|
| `AB Testing Data.csv` | Kaggle | ~294k users, landing page conversion experiment |
| `cookie_cats.csv` | Kaggle | ~90k users, mobile game gate placement experiment |

Notebook 03 generates a synthetic dataset if the real data is not present, so all notebooks will run without it — but results will differ from the real data.

**Notebook order matters.** Notebook 03 saves `data/ab_data_clean.csv` which is used by notebooks 04–10. Run them sequentially on first use.

**This is a learning project, not production code.** Statistical implementations are written for clarity and educational commentary, not performance. For production use, prefer `scipy.stats`, `statsmodels`, or `pingouin`.
