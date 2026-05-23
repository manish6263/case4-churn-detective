from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "case4_telecom_churn.csv"
TABLES_DIR = ROOT / "reports" / "tables"
FIGURES_DIR = ROOT / "reports" / "figures"


def churn_rate_table(df: pd.DataFrame, column: str) -> pd.DataFrame:
    grouped = (
        df.groupby(column, observed=True)
        .agg(customers=("churned", "size"), churners=("churned", "sum"), churn_rate=("churned", "mean"))
        .reset_index()
        .sort_values("churn_rate", ascending=False)
    )
    grouped["churn_rate"] = grouped["churn_rate"].round(4)
    grouped["share_of_customers"] = (grouped["customers"] / len(df)).round(4)
    return grouped


def save_churn_bar(table: pd.DataFrame, x_col: str, title: str, filename: str, rotate: bool = False) -> None:
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8.5, 4.8))
    ax = sns.barplot(data=table, x=x_col, y="churn_rate", color="#2563eb")
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel("Churn rate")
    ax.set_ylim(0, max(0.1, table["churn_rate"].max() * 1.25))
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")

    for container in ax.containers:
        ax.bar_label(container, labels=[f"{bar.get_height():.1%}" for bar in container], padding=3, fontsize=9)

    if rotate:
        plt.xticks(rotation=25, ha="right")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=180)
    plt.close()


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    df["tenure_bucket"] = pd.cut(
        df["tenure_months"],
        bins=[-1, 6, 12, 24, 48, 72],
        labels=["0-6", "7-12", "13-24", "25-48", "49-72"],
    )
    df["monthly_charge_bucket"] = pd.qcut(
        df["monthly_charges"],
        q=4,
        labels=["Q1 lowest", "Q2", "Q3", "Q4 highest"],
    )
    df["support_calls_bucket"] = pd.cut(
        df["support_calls_3mo"],
        bins=[-1, 0, 2, 5, 15],
        labels=["0", "1-2", "3-5", "6+"],
    )
    df["late_payments_bucket"] = pd.cut(
        df["late_payments_6mo"],
        bins=[-1, 0, 1, 6],
        labels=["0", "1", "2+"],
    )

    analyses = [
        ("contract_type", "Churn Rate By Contract Type", "churn_by_contract_type.png", False),
        ("tenure_bucket", "Churn Rate By Tenure", "churn_by_tenure_bucket.png", False),
        ("monthly_charge_bucket", "Churn Rate By Monthly Charge Quartile", "churn_by_monthly_charge_bucket.png", False),
        ("support_calls_bucket", "Churn Rate By Support Calls", "churn_by_support_calls.png", False),
        ("late_payments_bucket", "Churn Rate By Late Payments", "churn_by_late_payments.png", False),
        ("tech_support", "Churn Rate By Tech Support", "churn_by_tech_support.png", True),
        ("payment_method", "Churn Rate By Payment Method", "churn_by_payment_method.png", True),
    ]

    summary_rows = []
    for column, title, figure_name, rotate in analyses:
        table = churn_rate_table(df, column)
        table.to_csv(TABLES_DIR / f"churn_by_{column}.csv", index=False)
        save_churn_bar(table, column, title, figure_name, rotate=rotate)

        top = table.iloc[0]
        bottom = table.iloc[-1]
        summary_rows.append(
            {
                "driver": column,
                "highest_risk_group": top[column],
                "highest_churn_rate": top["churn_rate"],
                "lowest_risk_group": bottom[column],
                "lowest_churn_rate": bottom["churn_rate"],
                "risk_gap_pct_points": round((top["churn_rate"] - bottom["churn_rate"]) * 100, 2),
            }
        )

    driver_summary = pd.DataFrame(summary_rows).sort_values("risk_gap_pct_points", ascending=False)
    driver_summary.to_csv(TABLES_DIR / "churn_driver_summary.csv", index=False)

    print("Churn-driver EDA complete")
    print(driver_summary.to_string(index=False))


if __name__ == "__main__":
    main()
