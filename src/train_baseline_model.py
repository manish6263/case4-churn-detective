import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
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


def build_pipeline(numeric_features: list[str], categorical_features: list[str]) -> Pipeline:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
        ]
    )


def get_feature_names(model: Pipeline, numeric_features: list[str]) -> list[str]:
    preprocessor = model.named_steps["preprocessor"]
    categorical_names = (
        preprocessor.named_transformers_["cat"]
        .named_steps["onehot"]
        .get_feature_names_out(preprocessor.transformers_[1][2])
        .tolist()
    )
    return numeric_features + categorical_names


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

    model = build_pipeline(numeric_features, categorical_features)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "model": "logistic_regression_baseline",
        "test_rows": int(len(y_test)),
        "base_churn_rate_test": round(float(y_test.mean()), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "pr_auc": round(float(average_precision_score(y_test, y_proba)), 4),
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred)), 4),
        "recall": round(float(recall_score(y_test, y_pred)), 4),
        "f1": round(float(f1_score(y_test, y_pred)), 4),
    }

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    confusion = pd.DataFrame(
        [
            {"actual": "retained", "predicted_retained": int(tn), "predicted_churned": int(fp)},
            {"actual": "churned", "predicted_retained": int(fn), "predicted_churned": int(tp)},
        ]
    )

    feature_names = get_feature_names(model, numeric_features)
    coefficients = model.named_steps["model"].coef_[0]
    coefficient_table = pd.DataFrame({"feature": feature_names, "coefficient": coefficients})
    coefficient_table["abs_coefficient"] = coefficient_table["coefficient"].abs()
    coefficient_table = coefficient_table.sort_values("abs_coefficient", ascending=False)

    with (TABLES_DIR / "baseline_model_metrics.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)
    confusion.to_csv(TABLES_DIR / "baseline_confusion_matrix.csv", index=False)
    coefficient_table.to_csv(TABLES_DIR / "baseline_logistic_coefficients.csv", index=False)
    coefficient_table.head(20).to_csv(TABLES_DIR / "baseline_top_coefficients.csv", index=False)
    joblib.dump(model, MODELS_DIR / "baseline_logistic_model.joblib")

    print(json.dumps(metrics, indent=2))
    print("\nTop coefficients")
    print(coefficient_table.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
