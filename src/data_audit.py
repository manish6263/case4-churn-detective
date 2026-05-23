from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "case4_telecom_churn.csv"
TABLES_DIR = ROOT / "reports" / "tables"
FIGURES_DIR = ROOT / "reports" / "figures"


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    column_summary = pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(df[col].dtype) for col in df.columns],
            "missing_count": [int(df[col].isna().sum()) for col in df.columns],
            "missing_rate": [round(float(df[col].isna().mean()), 4) for col in df.columns],
            "unique_count": [int(df[col].nunique(dropna=True)) for col in df.columns],
        }
    )
    column_summary.to_csv(TABLES_DIR / "data_audit_columns.csv", index=False)

    dataset_summary = pd.DataFrame(
        [
            {"metric": "rows", "value": len(df)},
            {"metric": "columns", "value": df.shape[1]},
            {"metric": "duplicate_customer_ids", "value": int(df["customer_id"].duplicated().sum())},
            {"metric": "churn_rate", "value": round(float(df["churned"].mean()), 4)},
            {"metric": "churned_customers", "value": int(df["churned"].sum())},
            {"metric": "retained_customers", "value": int((1 - df["churned"]).sum())},
            {"metric": "tenure_mean_months", "value": round(float(df["tenure_months"].mean()), 2)},
            {"metric": "tenure_median_months", "value": round(float(df["tenure_months"].median()), 2)},
            {"metric": "monthly_charges_mean", "value": round(float(df["monthly_charges"].mean()), 2)},
            {"metric": "monthly_charges_min", "value": round(float(df["monthly_charges"].min()), 2)},
            {"metric": "monthly_charges_max", "value": round(float(df["monthly_charges"].max()), 2)},
        ]
    )
    dataset_summary.to_csv(TABLES_DIR / "data_audit_summary.csv", index=False)

    churn_counts = (
        df["churned"]
        .map({0: "Retained", 1: "Churned"})
        .value_counts()
        .rename_axis("status")
        .reset_index(name="customers")
    )
    churn_counts.to_csv(TABLES_DIR / "base_churn_counts.csv", index=False)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(7, 4.5))
    ax = sns.barplot(data=churn_counts, x="status", y="customers", hue="status", palette=["#2563eb", "#dc2626"], legend=False)
    ax.set_title("Base Churn Distribution")
    ax.set_xlabel("")
    ax.set_ylabel("Customers")

    total = len(df)
    for container in ax.containers:
        ax.bar_label(
            container,
            labels=[f"{int(v.get_height()):,}\n{v.get_height() / total:.1%}" for v in container],
            padding=4,
            fontsize=10,
        )

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "base_churn_distribution.png", dpi=180)
    plt.close()

    print("Data audit complete")
    print(dataset_summary.to_string(index=False))


if __name__ == "__main__":
    main()
