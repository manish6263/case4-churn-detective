# Decisions Log - Case 4

## Assumptions I Made

1. The CMO needs an actionable retention plan, not only a high-AUC model.
2. Campaign targeting should use ranked churn risk because the business cannot contact every customer.
3. Churn drivers in observational data are not automatically causal, so recommendations need a holdout test.

## Trade-offs

| Choice | Alternative | Why I Picked This |
|---|---|---|
| Logistic regression baseline | Only tree-based model | Gives interpretable direction and a reliable sanity check. |
| Campaign threshold metrics | Default 0.5 classifier threshold | A retention campaign has a budget, so top-risk targeting is more useful. |
| EDA evidence plus model importance | Feature importance only | The brief asks for evidence, not just importance bars. |
| Risk-based segmentation | One generic churn list | Different churn reasons need different retention plays. |

## What I De-scoped And Why

- Uplift modeling - no historical treatment/control campaign data is provided.
- Production scoring API - Case 4 is an analysis brief; Case 9 covers model serving.
- Real CRM integration - outside the one-day case scope.
- Guaranteed ROI claim - current impact is a gross estimate and needs a treatment/holdout campaign test.

## What I'd Do Differently With Another Day

- Add SHAP explanations if dependency setup remains smooth.
- Build a lightweight Streamlit dashboard for non-technical exploration.
- Use real offer costs and customer lifetime value for cost-aware optimization.
- Add treatment-response data and move from churn-risk modeling to uplift modeling.
