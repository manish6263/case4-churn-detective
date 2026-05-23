import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "case4_telecom_churn.csv"
MODELS_DIR = ROOT / "models"
TABLES_DIR = ROOT / "reports" / "tables"

TARGET = "churned"
ID_COLUMNS = ["customer_id"]


def build_preprocessor(numeric_features: list[str], categorical_features: list[str], scale_numeric: bool) -> ColumnTransformer:
    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", Pipeline(steps=numeric_steps), numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )


def build_candidates(numeric_features: list[str], categorical_features: list[str]) -> dict[str, Pipeline]:
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(numeric_features, categorical_features, scale_numeric=True)),
                ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(numeric_features, categorical_features, scale_numeric=False)),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=200,
                        min_samples_leaf=20,
                        class_weight="balanced",
                        random_state=42,
                        n_jobs=1,
                    ),
                ),
            ]
        ),
    }


def evaluate(name: str, model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict[str, float | str | int]:
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    return {
        "model": name,
        "test_rows": int(len(y_test)),
        "base_churn_rate_test": round(float(y_test.mean()), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "pr_auc": round(float(average_precision_score(y_test, y_proba)), 4),
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred)), 4),
        "recall": round(float(recall_score(y_test, y_pred)), 4),
        "f1": round(float(f1_score(y_test, y_pred)), 4),
    }


def main() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=[TARGET] + ID_COLUMNS)
    y = df[TARGET]

    numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=["number"]).columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )

    rows = []
    fitted_models = {}
    for name, model in build_candidates(numeric_features, categorical_features).items():
        model.fit(X_train, y_train)
        rows.append(evaluate(name, model, X_test, y_test))
        fitted_models[name] = model

    comparison = pd.DataFrame(rows).sort_values(["roc_auc", "pr_auc"], ascending=False)
    winner_name = str(comparison.iloc[0]["model"])
    winner = fitted_models[winner_name]

    comparison.to_csv(TABLES_DIR / "model_candidate_comparison.csv", index=False)
    with (TABLES_DIR / "selected_model.json").open("w", encoding="utf-8") as file:
        json.dump(
            {
                "selected_model": winner_name,
                "selection_reason": "Highest ROC-AUC, with PR-AUC used as a secondary check.",
                "metrics": comparison.iloc[0].to_dict(),
            },
            file,
            indent=2,
        )
    joblib.dump(winner, MODELS_DIR / "selected_churn_model.joblib")

    print(comparison.to_string(index=False))
    print(f"\nSelected model: {winner_name}")


if __name__ == "__main__":
    main()
