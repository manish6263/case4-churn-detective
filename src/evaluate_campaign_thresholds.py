import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "case4_telecom_churn.csv"
MODEL_PATH = ROOT / "models" / "selected_churn_model.joblib"
TABLES_DIR = ROOT / "reports" / "tables"

TARGET = "churned"
ID_COLUMNS = ["customer_id"]
THRESHOLDS = [0.10, 0.20, 0.30]


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=[TARGET] + ID_COLUMNS)
    y = df[TARGET]

    _, X_test, _, y_test, _, customer_ids_test = train_test_split(
        X,
        y,
        df["customer_id"],
        test_size=0.2,
        stratify=y,
        random_state=42,
    )

    model = joblib.load(MODEL_PATH)
    scored = X_test.copy()
    scored["customer_id"] = customer_ids_test.values
    scored["actual_churned"] = y_test.values
    scored["churn_probability"] = model.predict_proba(X_test)[:, 1]
    scored = scored.sort_values("churn_probability", ascending=False).reset_index(drop=True)
    scored["risk_rank"] = scored.index + 1

    base_churn_rate = float(y_test.mean())
    total_churners = int(y_test.sum())

    rows = []
    for threshold in THRESHOLDS:
        target_count = int(round(len(scored) * threshold))
        targeted = scored.head(target_count)
        churners_found = int(targeted["actual_churned"].sum())
        precision = churners_found / target_count
        recall = churners_found / total_churners
        lift = precision / base_churn_rate
        avg_monthly_charge = float(targeted["monthly_charges"].mean())

        rows.append(
            {
                "target_top_pct": int(threshold * 100),
                "targeted_customers": target_count,
                "churners_found": churners_found,
                "precision_at_threshold": round(precision, 4),
                "recall_at_threshold": round(recall, 4),
                "lift_vs_random": round(lift, 2),
                "avg_monthly_charge_targeted": round(avg_monthly_charge, 2),
            }
        )

    threshold_table = pd.DataFrame(rows)
    threshold_table.to_csv(TABLES_DIR / "campaign_threshold_evaluation.csv", index=False)
    scored.head(int(round(len(scored) * 0.20))).to_csv(TABLES_DIR / "top_20pct_scored_customers.csv", index=False)

    selected = threshold_table.loc[threshold_table["target_top_pct"] == 20].iloc[0].to_dict()
    expected = {
        "selected_threshold": "top_20_percent",
        "assumed_save_rate_low": 0.10,
        "assumed_save_rate_high": 0.15,
        "assumed_retention_months": 6,
        "targeted_customers": int(selected["targeted_customers"]),
        "churners_found": int(selected["churners_found"]),
        "expected_saved_customers_low": round(selected["churners_found"] * 0.10, 1),
        "expected_saved_customers_high": round(selected["churners_found"] * 0.15, 1),
        "avg_monthly_charge_targeted": selected["avg_monthly_charge_targeted"],
        "gross_revenue_saved_low": round(selected["churners_found"] * 0.10 * selected["avg_monthly_charge_targeted"] * 6, 2),
        "gross_revenue_saved_high": round(selected["churners_found"] * 0.15 * selected["avg_monthly_charge_targeted"] * 6, 2),
        "note": "Gross estimate before offer costs. Use holdout test to measure true incremental lift.",
    }
    with (TABLES_DIR / "campaign_impact_estimate.json").open("w", encoding="utf-8") as file:
        json.dump(expected, file, indent=2)

    print(threshold_table.to_string(index=False))
    print("\nTop 20% impact estimate")
    print(json.dumps(expected, indent=2))


if __name__ == "__main__":
    main()
