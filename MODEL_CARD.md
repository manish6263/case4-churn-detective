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

## Monitoring Considerations

In production, the model should be monitored for feature drift, label drift, campaign response, fairness concerns, and changes in churn base rate.
