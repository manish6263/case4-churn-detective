# Case 4: Churn Detective - Telecom Retention Brief

CMO-ready churn analysis that combines honest model performance, evidence-backed churn drivers, actionable churner segments, three retention plays, limitations/risks, and a 60-day success measurement plan.

## What This Is

This project turns the provided telecom churn dataset into a retention brief for a CMO. The goal is not only to predict churn, but to explain why customers churn, who should be targeted first, what offer each segment should receive, and how campaign success should be measured.

## Dataset

The provided dataset is stored at:

```text
data/case4_telecom_churn.csv
```

It contains 7,000 customers, 20 input features, and the binary target column `churned`.

## How To Run Locally

```bash
git clone https://github.com/manish6263/case4-churn-detective.git
cd case4-churn-detective
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

Open:

```text
notebooks/case4_churn_analysis.ipynb
```

This notebook is the main review entry point. It summarizes the data audit, driver evidence, model comparison, campaign threshold, customer segments, retention plays, limitations, and 60-day measurement plan.

## Planned Deliverables

- Notebook with EDA, modeling, interpretation, segmentation, limitations, and 60-day measurement plan: `notebooks/case4_churn_analysis.ipynb`.
- 5-slide CMO deck.
- CMO retention brief: `reports/churn_retention_brief.md`.
- `DECISIONS.md` with assumptions and trade-offs.
- Submission package with README, DECISIONS, deck PDF, repo link, and demo video link.

## Reproduce Report Assets

Run the data audit:

```bash
python src/data_audit.py
```

This writes audit tables to `reports/tables/` and the base churn chart to `reports/figures/`.

Run churn-driver EDA:

```bash
python src/churn_driver_eda.py
```

This writes churn-rate evidence tables and driver charts to `reports/tables/` and `reports/figures/`.

Train the interpretable baseline model:

```bash
python src/train_baseline_model.py
```

This writes baseline metrics, confusion matrix, coefficients, and the model artifact to `reports/tables/` and `models/`.

Compare model candidates:

```bash
python src/compare_model_candidates.py
```

This compares Logistic Regression with Random Forest. The current selected model is Random Forest for risk ranking because it has the best ROC-AUC and PR-AUC, while Logistic Regression remains useful for directional interpretation.

Evaluate campaign targeting thresholds:

```bash
python src/evaluate_campaign_thresholds.py
```

At the current top-20% risk threshold, the model targets 280 customers in the test set and captures 170 actual churners, giving 60.71% precision and 1.68x lift over random targeting.

Segment top-risk customers:

```bash
python src/make_segments.py
```

The top-risk pool is split into primary segments for campaign planning. The largest primary group is service-frustrated customers, while membership analysis shows payment-friction and new-customer onboarding risks are common and often overlap with other risks.

Read the CMO-facing retention brief:

```text
reports/churn_retention_brief.md
```

It summarizes who to target, what to offer, expected impact, limitations, and the 60-day measurement plan.

## Stack

- pandas/numpy: data audit and feature analysis.
- scikit-learn: churn modeling, metrics, and permutation importance.
- matplotlib/seaborn: evidence charts for the CMO deck.
- Jupyter: required notebook workflow.
