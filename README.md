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

## Planned Deliverables

- Notebook with EDA, modeling, interpretation, segmentation, limitations, and 60-day measurement plan.
- 5-slide CMO deck.
- `DECISIONS.md` with assumptions and trade-offs.
- Submission package with README, DECISIONS, deck PDF, repo link, and demo video link.

## Stack

- pandas/numpy: data audit and feature analysis.
- scikit-learn: churn modeling, metrics, and permutation importance.
- matplotlib/seaborn: evidence charts for the CMO deck.
- Jupyter: required notebook workflow.
