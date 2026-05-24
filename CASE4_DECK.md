# Case 4 Deck - Churn Detective

Use this as the source for a 5-slide CMO deck. Keep the final deck visual and concise: one idea per slide, real charts from `reports/figures/`, and no model jargon unless it supports a business decision.

---

## Slide 1 - The Churn Problem

**Title:** Churn Is A Targeting Problem

**On-slide text:**

Base churn is 36.16%. The goal is to focus retention spend on customers most likely to leave.

**Visual:**

`reports/figures/base_churn_distribution.png`

**Speaker notes:**

The CMO does not need a generic churn score for every customer. She needs to know where retention spend should go first. The dataset has 7,000 customers and a 36.16% churn rate, so random outreach would waste budget.

---

## Slide 2 - What Drives Churn

**Title:** The Clearest Risk Signals

**On-slide text:**

Short tenure, month-to-month contracts, repeated support calls, payment friction, and electronic checks show the strongest churn gaps.

**Visual:**

Use one main chart:

`reports/figures/churn_by_contract_type.png`

Optional small supporting charts:

`reports/figures/churn_by_tenure_bucket.png`  
`reports/figures/churn_by_support_calls.png`

**Speaker notes:**

Month-to-month customers churn at 46.75%, compared with 22.62% for two-year customers. New customers and customers with repeated support calls are also high risk. This is evidence from observed churn rates, not just model feature importance.

---

## Slide 3 - Who To Target

**Title:** Start With The Top 20%

**On-slide text:**

Top-20% risk targeting finds 170 churners in 280 customers, with 60.71% precision and 1.68x lift.

**Visual:**

Create a compact table from:

`reports/tables/campaign_threshold_evaluation.csv`

Use only the top-20% row in the slide:

| Targeted | Churners found | Precision | Lift |
|---:|---:|---:|---:|
| 280 | 170 | 60.71% | 1.68x |

**Speaker notes:**

Instead of using a default 0.5 threshold, I ranked customers by churn probability. The top-20% threshold gives a practical campaign size and captures one-third of churners with 1.68x lift over random targeting.

---

## Slide 4 - What To Offer

**Title:** Three Segment-Specific Plays

**On-slide text:**

Payment fix. Service rescue. Price lock. Different churn reasons need different actions.

**Visual:**

Use a three-column table:

| Segment | Signal | Play |
|---|---|---|
| Payment-friction | 67.38% churn | Autopay incentive + billing support |
| Service-frustrated | 60.68% churn | Priority callback + tech support trial |
| Price-sensitive | 62.22% churn | Price lock + contract upgrade |

**Speaker notes:**

The key is not to give everyone the same discount. Payment-friction customers need billing help. Service-frustrated customers need issue resolution. Price-sensitive month-to-month customers need a price-lock or contract upgrade offer.

---

## Slide 5 - Measurement And Risks

**Title:** Prove Lift Before Scaling

**On-slide text:**

Run a 60-day treatment vs holdout test by segment. Scale only plays with positive net value.

**Visual:**

Use a simple measurement flow:

Top-risk customers -> random split -> treatment / holdout -> compare 60-day churn and net revenue

**Speaker notes:**

The model predicts churn risk, not offer responsiveness. So I would not call this guaranteed ROI. I would run a holdout test, track churn reduction, offer acceptance, support-call changes, autopay conversion, and net revenue saved after offer costs.

---

## Final Deck Checklist

- Export as `deck.pdf`.
- Use real charts from `reports/figures/`.
- Keep body text under 25 words per slide where possible.
- Put business recommendations before model details.
- Mention limitations honestly on Slide 5.
