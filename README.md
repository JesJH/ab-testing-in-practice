# A/B Testing in Practice

An end-to-end portfolio project covering the full A/B testing lifecycle — from experiment design and statistical rigor to practical business decision-making.

## What This Covers

| Notebook | Topic |
|---|---|
| 01 | Experiment design — hypothesis, metrics, framing |
| 02 | Data validation — sample ratio mismatch, AA tests |
| 03 | Statistical analysis — z-test, t-test, p-values, confidence intervals |
| 04 | Practical significance — effect size, MDE, when to ship vs. not |
| 05 | Segment analysis — subgroup breakdowns, interaction effects |
| 06 | Multiple testing — Bonferroni and FDR correction |
| 07 | Business impact — translating lift into revenue and decisions |

## Datasets

- **Landing page conversion** (~300k users, binary conversion metric)
- **Cookie Cats mobile game** (~90k users, Day-1 / Day-7 retention)

## Setup

```bash
git clone https://github.com/JesJH/ab-testing-in-practice.git
cd ab-testing-in-practice
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Download datasets from Kaggle (see [CLAUDE.md](CLAUDE.md) for links) and place them in the `data/` directory.

## Key Takeaways

- Statistical significance does not mean practical significance
- Underpowered tests are as misleading as significant ones
- Segment effects can mask or reverse aggregate results (Simpson's Paradox)
- Every test result should be framed as a business decision, not just a p-value
