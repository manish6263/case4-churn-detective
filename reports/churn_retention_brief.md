# Churn Retention Brief

## Executive Summary

The churn model should be used as a **campaign prioritization tool**, not as an automatic decision system. At a top-20% risk threshold, the model targets 280 held-out customers and captures 170 actual churners, giving **60.71% precision** and **1.68x lift** over random targeting.

The clearest churn signals are short tenure, month-to-month contracts, repeated support calls, repeated late payments, electronic-check payment, and higher monthly charges.

## Who To Target First

Use the top-20% risk pool as the starting campaign audience.

| Metric | Value |
|---|---:|
| Customers targeted | 280 |
| Actual churners captured | 170 |
| Precision | 60.71% |
| Recall | 33.60% |
| Lift vs random targeting | 1.68x |
| Average monthly charge | $74.99 |

## High-Risk Segments

Segments can overlap, so the campaign should use segment tags rather than a single hard label.

| Segment | Customers | Churners | Churn Rate | Why It Matters |
|---|---:|---:|---:|---|
| Payment-friction | 141 | 95 | 67.38% | Late payments and electronic checks suggest preventable billing friction. |
| New-customer onboarding | 127 | 85 | 66.93% | Early-tenure customers are not yet locked in and churn quickly. |
| Service-frustrated | 117 | 71 | 60.68% | Repeated support calls suggest unresolved service pain. |
| Price-sensitive | 90 | 56 | 62.22% | High charges plus flexible contracts indicate price pressure. |

## Three Retention Plays

### 1. Payment Friction Fix

**Target segment:** payment-friction customers in the top-risk pool.

**Offer:** autopay setup incentive, billing reminders, and one-time late-fee waiver after successful autopay enrollment.

**Why this play:** payment-friction customers have a 67.38% churn rate in the top-risk pool. This is the largest overlapping risk segment and is operationally easy to target.

**Expected impact:** if the campaign saves 10-15% of the 95 likely churners in this segment, it saves about 10-14 customers before offer costs.

**Measurement:** autopay enrollment, late-payment reduction, 60-day churn versus holdout, and net revenue saved.

### 2. Service Rescue

**Target segment:** customers with repeated support calls in the top-risk pool.

**Offer:** priority callback, named issue owner, escalation SLA, and short free tech-support trial.

**Why this play:** service-frustrated customers have a 60.68% churn rate. Their problem is not necessarily price; a generic discount may miss the real cause.

**Expected impact:** if the campaign saves 10-15% of the 71 likely churners in this segment, it saves about 7-11 customers before offer costs.

**Measurement:** issue resolution within 7 days, repeat support calls, customer satisfaction after intervention, and 60-day churn versus holdout.

### 3. Price-Lock / Contract Upgrade

**Target segment:** price-sensitive high-risk customers, especially month-to-month customers with high monthly charges.

**Offer:** 3-month price lock, annual-contract discount, or plan-rightsizing review.

**Why this play:** month-to-month customers churn at 46.75% overall, and high-charge customers show elevated churn. This play should be targeted, not given to all high-charge customers.

**Expected impact:** if the campaign saves 10-15% of the 56 likely churners in this segment, it saves about 6-8 customers before offer costs.

**Measurement:** offer acceptance, contract conversion, monthly recurring revenue retained, discount cost, and 60-day churn versus holdout.

## Rough Overall Impact

At the top-20% threshold:

- likely churners captured: 170
- assumed save rate: 10-15%
- expected saved customers: 17.0-25.5
- average monthly charge in target pool: $74.99
- gross six-month revenue saved: $7,648.98-$11,473.47 before offer costs

This is not an ROI guarantee. The true incremental value must be measured with a treatment/holdout design.

## 60-Day Measurement Plan

1. Rank customers by churn probability and select the top-risk eligible pool.
2. Randomly split eligible customers into treatment and holdout groups within each segment.
3. Apply segment-specific offers only to the treatment group.
4. Track offer acceptance, 60-day churn, support-call changes, late-payment changes, and revenue retained.
5. Compare treatment versus holdout by segment.
6. Scale only the plays with positive net value after offer costs.

Primary success metric:

```text
60-day churn reduction in treatment group vs holdout group
```

Secondary metrics:

- net revenue saved
- offer acceptance rate
- support-call reduction
- autopay conversion
- contract upgrade rate

## Limitations And Risks

- This is observational data; churn drivers are not automatically causal.
- The model predicts churn risk, not whether a customer will respond to a specific offer.
- Discounts may waste margin on customers who would have stayed anyway.
- High-risk segments overlap, so campaign rules need priority ordering.
- Customer behavior may change next quarter, so the model and thresholds need monitoring.
- Some features may proxy for sensitive or regulated attributes; campaign policy should be reviewed before launch.
- The current impact estimate is gross revenue before offer costs.
