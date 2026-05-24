from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "case4_telecom_churn.csv"
TOP_RISK_PATH = ROOT / "reports" / "tables" / "top_20pct_scored_customers.csv"
TABLES_DIR = ROOT / "reports" / "tables"
FIGURES_DIR = ROOT / "reports" / "figures"


def assign_primary_segment(row: pd.Series, high_charge_cutoff: float) -> str:
    if row["support_calls_3mo"] >= 3:
        return "Service-frustrated"
    if row["late_payments_6mo"] >= 2 or row["payment_method"] == "Electronic check":
        return "Payment-friction"
    if row["contract_type"] == "Month-to-month" and row["monthly_charges"] >= high_charge_cutoff:
        return "Price-sensitive"
    if row["tenure_months"] <= 6 and row["contract_type"] == "Month-to-month":
        return "New-customer onboarding"
    return "General high-risk"


def summarize_segments(df: pd.DataFrame, segment_column: str) -> pd.DataFrame:
    summary = (
        df.groupby(segment_column, observed=True)
        .agg(
            customers=("customer_id", "count"),
            churners=("actual_churned", "sum"),
            churn_rate=("actual_churned", "mean"),
            avg_churn_probability=("churn_probability", "mean"),
            avg_monthly_charge=("monthly_charges", "mean"),
            avg_tenure_months=("tenure_months", "mean"),
            avg_support_calls=("support_calls_3mo", "mean"),
            avg_late_payments=("late_payments_6mo", "mean"),
        )
        .reset_index()
        .sort_values(["churners", "churn_rate"], ascending=False)
    )
    summary["share_of_top20_pool"] = summary["customers"] / len(df)
    for column in [
        "churn_rate",
        "avg_churn_probability",
        "avg_monthly_charge",
        "avg_tenure_months",
        "avg_support_calls",
        "avg_late_payments",
        "share_of_top20_pool",
    ]:
        summary[column] = summary[column].round(4)
    return summary


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    full_df = pd.read_csv(DATA_PATH)
    top_risk = pd.read_csv(TOP_RISK_PATH)
    high_charge_cutoff = float(full_df["monthly_charges"].quantile(0.75))

    top_risk["primary_segment"] = top_risk.apply(assign_primary_segment, axis=1, high_charge_cutoff=high_charge_cutoff)
    top_risk.to_csv(TABLES_DIR / "top_20pct_scored_customers_segmented.csv", index=False)

    primary_summary = summarize_segments(top_risk, "primary_segment")
    primary_summary.to_csv(TABLES_DIR / "high_risk_segment_summary.csv", index=False)

    membership_rules = {
        "Price-sensitive": (top_risk["contract_type"] == "Month-to-month")
        & (top_risk["monthly_charges"] >= high_charge_cutoff),
        "Service-frustrated": top_risk["support_calls_3mo"] >= 3,
        "Payment-friction": (top_risk["late_payments_6mo"] >= 2)
        | (top_risk["payment_method"] == "Electronic check"),
        "New-customer onboarding": (top_risk["tenure_months"] <= 6)
        & (top_risk["contract_type"] == "Month-to-month"),
    }

    membership_rows = []
    for segment, mask in membership_rules.items():
        subset = top_risk.loc[mask]
        membership_rows.append(
            {
                "segment": segment,
                "customers": int(len(subset)),
                "churners": int(subset["actual_churned"].sum()),
                "churn_rate": round(float(subset["actual_churned"].mean()), 4) if len(subset) else 0.0,
                "share_of_top20_pool": round(float(len(subset) / len(top_risk)), 4),
                "avg_churn_probability": round(float(subset["churn_probability"].mean()), 4) if len(subset) else 0.0,
            }
        )

    membership_summary = pd.DataFrame(membership_rows).sort_values(["customers", "churn_rate"], ascending=False)
    membership_summary.to_csv(TABLES_DIR / "high_risk_segment_membership_summary.csv", index=False)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(9, 4.8))
    ax = sns.barplot(data=primary_summary, x="primary_segment", y="customers", color="#2563eb")
    ax.set_title("Top-20% Risk Customers By Primary Segment")
    ax.set_xlabel("")
    ax.set_ylabel("Customers")
    for container in ax.containers:
        ax.bar_label(container, padding=3, fontsize=9)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "high_risk_primary_segments.png", dpi=180)
    plt.close()

    print("Primary segment summary")
    print(primary_summary.to_string(index=False))
    print("\nMembership summary")
    print(membership_summary.to_string(index=False))


if __name__ == "__main__":
    main()
