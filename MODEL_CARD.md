# Model Card - Case 4 Churn Model

## Intended Use

Rank telecom customers by churn risk so the retention team can prioritize campaign outreach and segment-specific offers.

## Not Intended For

- Automatic customer treatment without a holdout test.
- Causal claims about why customers churn.
- Decisions that require fairness/compliance review without additional analysis.

## Target

`churned`

## Planned Evaluation

- ROC-AUC
- PR-AUC
- precision/recall/F1
- confusion matrix
- precision and recall at the top-risk campaign threshold
- lift over random targeting

## Current Candidate Comparison

| Model | ROC-AUC | PR-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest | 0.7242 | 0.5744 | 0.6500 | 0.5125 | 0.6482 | 0.5724 |
| Logistic Regression | 0.7191 | 0.5677 | 0.6629 | 0.5256 | 0.6897 | 0.5966 |

Current selection: **Random Forest** for churn-risk ranking because it has the strongest ROC-AUC and PR-AUC. Logistic Regression is still used for interpretability because its coefficients give clearer directionality.

## Campaign Threshold Result

Using the selected Random Forest risk scores on the held-out test set:

| Targeting Rule | Customers Targeted | Churners Found | Precision | Recall | Lift vs Random |
|---|---:|---:|---:|---:|---:|
| Top 10% risk | 140 | 86 | 0.6143 | 0.1700 | 1.70x |
| Top 20% risk | 280 | 170 | 0.6071 | 0.3360 | 1.68x |
| Top 30% risk | 420 | 243 | 0.5786 | 0.4802 | 1.60x |

Recommended starting point: **top 20% risk**. It captures one-third of churners in a manageable outreach pool and performs 1.68x better than random targeting.

## Monitoring Considerations

In production, the model should be monitored for feature drift, label drift, campaign response, fairness concerns, and changes in churn base rate.
