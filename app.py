from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
FIGURES = ROOT / "reports" / "figures"
TABLES = ROOT / "reports" / "tables"
BRIEF_PATH = ROOT / "reports" / "churn_retention_brief.md"


st.set_page_config(page_title="Churn Detective", page_icon="📉", layout="wide")


@st.cache_data
def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data
def read_json(path: Path) -> dict:
    return pd.read_json(path, typ="series").to_dict()


st.title("Churn Detective")
st.caption("Telecom retention brief for CMO campaign planning")

summary = read_csv(TABLES / "data_audit_summary.csv").set_index("metric")["value"].to_dict()
thresholds = read_csv(TABLES / "campaign_threshold_evaluation.csv")
segments = read_csv(TABLES / "high_risk_segment_membership_summary.csv")
model_comparison = read_csv(TABLES / "model_candidate_comparison.csv")
impact = read_json(TABLES / "campaign_impact_estimate.json")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers", f"{int(summary['rows']):,}")
col2.metric("Base churn", f"{summary['churn_rate']:.2%}")
col3.metric("Top-20% precision", "60.71%")
col4.metric("Lift vs random", "1.68x")

st.divider()

st.header("1. What drives churn?")
st.write(
    "The strongest observed churn gaps come from short tenure, month-to-month contracts, "
    "repeated support calls, payment friction, electronic checks, and high monthly charges."
)

driver_a, driver_b = st.columns(2)
with driver_a:
    st.image(str(FIGURES / "churn_by_contract_type.png"), use_container_width=True)
    st.image(str(FIGURES / "churn_by_support_calls.png"), use_container_width=True)
with driver_b:
    st.image(str(FIGURES / "churn_by_tenure_bucket.png"), use_container_width=True)
    st.image(str(FIGURES / "churn_by_payment_method.png"), use_container_width=True)

with st.expander("Driver summary table"):
    st.dataframe(read_csv(TABLES / "churn_driver_summary.csv"), use_container_width=True)

st.header("2. Who should the CMO target?")
st.write(
    "The selected starting point is the top 20% highest-risk customers. This keeps outreach manageable "
    "while finding one-third of churners in the held-out test set."
)
st.dataframe(thresholds, use_container_width=True)

targeted = int(impact["targeted_customers"])
churners = int(impact["churners_found"])
saved_low = impact["expected_saved_customers_low"]
saved_high = impact["expected_saved_customers_high"]
revenue_low = impact["gross_revenue_saved_low"]
revenue_high = impact["gross_revenue_saved_high"]

st.success(
    f"Top-20% targeting reaches {targeted} customers and finds {churners} churners. "
    f"With a 10-15% save-rate assumption, this is {saved_low}-{saved_high} saved customers "
    f"and ${revenue_low:,.0f}-${revenue_high:,.0f} gross six-month revenue before offer costs."
)

st.header("3. Which segments need different plays?")
st.write("Segments can overlap, so campaign rules should use segment tags and priority ordering.")
st.dataframe(segments, use_container_width=True)
st.image(str(FIGURES / "high_risk_primary_segments.png"), use_container_width=True)

st.header("4. What should we offer?")
plays = pd.DataFrame(
    [
        {
            "Segment": "Payment-friction",
            "Signal": "67.38% churn",
            "Play": "Autopay incentive + billing support",
        },
        {
            "Segment": "Service-frustrated",
            "Signal": "60.68% churn",
            "Play": "Priority callback + tech support trial",
        },
        {
            "Segment": "Price-sensitive",
            "Signal": "62.22% churn",
            "Play": "Price lock + contract upgrade",
        },
    ]
)
st.dataframe(plays, hide_index=True, use_container_width=True)

st.header("5. How do we prove it works?")
flow_cols = st.columns([1.1, 1.1, 1.4, 1.1])
flow_cols[0].info("Top-risk customers")
flow_cols[1].info("Random split")
flow_cols[2].success("Treatment offer\n\nHoldout group")
flow_cols[3].info("60-day comparison")
st.write(
    "Run a 60-day treatment versus holdout test by segment. Scale only the plays that reduce churn "
    "and produce positive net value after offer costs."
)

st.header("Model performance")
st.dataframe(model_comparison, use_container_width=True)
st.caption(
    "Random Forest is selected for risk ranking because it has the highest ROC-AUC and PR-AUC. "
    "Logistic Regression remains useful for directional interpretation."
)

with st.expander("Read the full retention brief"):
    st.markdown(BRIEF_PATH.read_text(encoding="utf-8"))
