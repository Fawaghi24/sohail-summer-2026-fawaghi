"""
model.py

Trains and evaluates predictive models on the cleaned player dataset.
Regression: compares Linear Regression, Decision Tree, and a
GridSearchCV-tuned Random Forest (5-fold CV) to predict total_points.
Classification: trains Logistic Regression and Random Forest models
to flag "high performer" players (top 25% by points), then runs
error analysis on the false positives/negatives.
Input:  data/processed/players_clean.csv
Output: charts/day11_confusion_matrix.png
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
)
import matplotlib.pyplot as plt
import seaborn as sns


def test_mae_rmse(pipeline, X_te, y_te):
    """
    Compute MAE and RMSE for a fitted pipeline on a test set.

    Parameters:
        pipeline (Pipeline): a fitted scikit-learn pipeline
        X_te (pd.DataFrame): test features
        y_te (pd.Series): true test target values

    Returns:
        tuple[float, float]: (MAE, RMSE)
    """
    preds = pipeline.predict(X_te)
    mae = mean_absolute_error(y_te, preds)
    rmse = np.sqrt(mean_squared_error(y_te, preds))
    return mae, rmse


def print_classification_results(name, pipeline, X_te, y_te):
    """
    Print accuracy, precision, recall, F1, confusion matrix, and the
    full classification report for a fitted classifier.

    Parameters:
        name (str): label to print above the results (e.g. model name)
        pipeline (Pipeline): a fitted scikit-learn classifier pipeline
        X_te (pd.DataFrame): test features
        y_te (pd.Series): true test labels

    Returns:
        np.ndarray: the predicted labels for the test set
    """
    preds = pipeline.predict(X_te)
    print(f"\n    {name}    ")
    print(f"Accuracy : {accuracy_score(y_te, preds):.3f}")
    print(f"Precision: {precision_score(y_te, preds):.3f}")
    print(f"Recall   : {recall_score(y_te, preds):.3f}")
    print(f"F1 score : {f1_score(y_te, preds):.3f}")
    print("Confusion matrix (rows=actual, cols=predicted):")
    print(confusion_matrix(y_te, preds))
    print("\nFull classification report:")
    print(classification_report(y_te, preds))
    return preds


def main():
    """
    Train and evaluate three regression models (Linear, Decision Tree,
    tuned Random Forest) to predict total_points, then train two
    classifiers (Logistic Regression, Random Forest) to flag high
    performers, and run error analysis on the classifier's mistakes.

    Loads data/processed/players_clean.csv, filters to players with
    450+ minutes, and saves a confusion matrix heatmap to charts/.

    Returns:
        None
    """
    script_dir = Path(__file__).parent  
    csv_path = script_dir.parent / "data" / "processed" / "players_clean.csv"  
    charts_dir = script_dir.parent / "charts"  

    df = pd.read_csv(csv_path)
    print("Loaded data. Shape:", df.shape)

    df = df[df["minutes"] >= 450].copy()
    print("After filtering to players with >= 450 minutes:", df.shape)

    target_col = "total_points"

    feature_columns = [
        "minutes",
        "goals_scored",
        "assists",
        "clean_sheets",
        "goals_conceded",
        "yellow_cards",
        "red_cards",
        "saves",
        "now_cost",
        "expected_goals",
        "expected_assists",
        "goals_per_90",
        "assists_per_90",
        "minutes_share",
        "position",
    ]

    X = df[feature_columns].copy()
    y = df[target_col].copy()

    X = pd.get_dummies(X, columns=["position"], drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("\nShapes after split:")
    print("X_train:", X_train.shape)
    print("X_test :", X_test.shape)

    # --- Regression: Linear, Tree, and Random Forest, cross-validated ---

    linear_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression()),
    ])

    tree_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", DecisionTreeRegressor(max_depth=5, random_state=42)),
    ])

    linear_cv_scores = cross_val_score(linear_pipeline, X, y, cv=5, scoring="r2")
    tree_cv_scores = cross_val_score(tree_pipeline, X, y, cv=5, scoring="r2")

    print("\n--- 5-FOLD CROSS-VALIDATION (mean R2 +/- std) ---")
    print(f"LinearRegression : mean R2 = {linear_cv_scores.mean():.3f}  std = {linear_cv_scores.std():.3f}")
    print(f"DecisionTree     : mean R2 = {tree_cv_scores.mean():.3f}  std = {tree_cv_scores.std():.3f}")
    print("Linear fold scores:", np.round(linear_cv_scores, 3))
    print("Tree fold scores  :", np.round(tree_cv_scores, 3))

    forest_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(n_estimators=100, random_state=42)),
    ])

    forest_cv_scores = cross_val_score(forest_pipeline, X, y, cv=5, scoring="r2")
    print(f"\nRandomForest     : mean R2 = {forest_cv_scores.mean():.3f}  std = {forest_cv_scores.std():.3f}")

    linear_pipeline.fit(X_train, y_train)
    tree_pipeline.fit(X_train, y_train)
    forest_pipeline.fit(X_train, y_train)

    linear_test_mae, linear_test_rmse = test_mae_rmse(linear_pipeline, X_test, y_test)
    tree_test_mae, tree_test_rmse = test_mae_rmse(tree_pipeline, X_test, y_test)
    forest_test_mae, forest_test_rmse = test_mae_rmse(forest_pipeline, X_test, y_test)

    # --- One comparison table for all three models ---

    comparison = pd.DataFrame({
        "LinearRegression": {
            "cv_mean_R2": linear_cv_scores.mean(),
            "cv_std_R2": linear_cv_scores.std(),
            "test_MAE": linear_test_mae,
            "test_RMSE": linear_test_rmse,
        },
        "DecisionTree": {
            "cv_mean_R2": tree_cv_scores.mean(),
            "cv_std_R2": tree_cv_scores.std(),
            "test_MAE": tree_test_mae,
            "test_RMSE": tree_test_rmse,
        },
        "RandomForest": {
            "cv_mean_R2": forest_cv_scores.mean(),
            "cv_std_R2": forest_cv_scores.std(),
            "test_MAE": forest_test_mae,
            "test_RMSE": forest_test_rmse,
        },
    })

    print("\n--- FULL MODEL COMPARISON (cross-validated) ---")
    print(comparison.round(3))

    # --- Tune the Random Forest with GridSearchCV ---

    param_grid = {
        "model__max_depth": [5, 10, None],
        "model__min_samples_leaf": [1, 3, 5],
    }

    grid_search = GridSearchCV(
        forest_pipeline,
        param_grid=param_grid,
        cv=5,
        scoring="r2",
    )

    grid_search.fit(X_train, y_train)

    print("\n--- GRIDSEARCHCV RESULTS (RandomForest) ---")
    print("Best parameters:", grid_search.best_params_)
    print(f"Best cross-validated R2: {grid_search.best_score_:.3f}")

    best_forest_pipeline = grid_search.best_estimator_
    tuned_test_mae, tuned_test_rmse = test_mae_rmse(best_forest_pipeline, X_test, y_test)
    tuned_test_r2 = r2_score(y_test, best_forest_pipeline.predict(X_test))

    print(f"Tuned RandomForest on held-out test set -> MAE: {tuned_test_mae:.3f}  RMSE: {tuned_test_rmse:.3f}  R2: {tuned_test_r2:.3f}")

    # --- Feature importances from the tuned forest ---

    tuned_forest_model = best_forest_pipeline.named_steps["model"]

    tuned_importance_df = pd.DataFrame({
        "feature": X.columns,
        "importance": tuned_forest_model.feature_importances_,
    }).sort_values("importance", ascending=False)

    print("\n--- TUNED RANDOM FOREST FEATURE IMPORTANCES ---")
    print(tuned_importance_df.to_string(index=False))

    # --- Part B: build a classification model ---

    points_75th_percentile = df["total_points"].quantile(0.75)
    print(f"\n75th percentile of total_points (450+ min players): {points_75th_percentile:.1f}")

    df["high_performer"] = (df["total_points"] > points_75th_percentile).astype(int)

    class_balance = df["high_performer"].value_counts(normalize=True) * 100
    print("\nClass balance (% of players):")
    print(class_balance.round(1))

    y_class = df["high_performer"]

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        X, y_class, test_size=0.2, random_state=42
    )

    logreg_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000)),
    ])

    rf_clf_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(n_estimators=100, random_state=42)),
    ])

    logreg_pipeline.fit(X_train_c, y_train_c)
    rf_clf_pipeline.fit(X_train_c, y_train_c)

    logreg_preds = print_classification_results("Logistic Regression", logreg_pipeline, X_test_c, y_test_c)
    rf_clf_preds = print_classification_results("Random Forest Classifier", rf_clf_pipeline, X_test_c, y_test_c)

    best_clf_name = "RandomForestClassifier"
    best_clf_preds = rf_clf_preds

    cm = confusion_matrix(y_test_c, best_clf_preds)

    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Not High Performer", "High Performer"],
                yticklabels=["Not High Performer", "High Performer"],
                ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion Matrix - {best_clf_name}")
    plt.tight_layout()

    charts_dir.mkdir(exist_ok=True)
    confusion_matrix_path = charts_dir / "day11_confusion_matrix.png"
    plt.savefig(confusion_matrix_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved confusion matrix heatmap to {confusion_matrix_path}")

    # --- Part C: error analysis ---

    results_c = X_test_c.copy()
    results_c["full_name"] = df.loc[X_test_c.index, "full_name"].values
    results_c["actual"] = y_test_c.values
    results_c["predicted"] = best_clf_preds

    # False positives
    false_positives = results_c[(results_c["predicted"] == 1) & (results_c["actual"] == 0)]

    # False negatives: genuine high performers the model missed.
    false_negatives = results_c[(results_c["predicted"] == 0) & (results_c["actual"] == 1)]

    cols_to_show = ["full_name", "minutes", "goals_scored", "assists", "now_cost", "minutes_share"]

    print(f"\n--- FALSE POSITIVES ({len(false_positives)} players) ---")
    print("Model predicted 'high performer' but they were not:")
    print(false_positives[cols_to_show].to_string(index=False))

    print(f"\n--- FALSE NEGATIVES ({len(false_negatives)} players) ---")
    print("Genuine high performers the model missed:")
    print(false_negatives[cols_to_show].to_string(index=False))


if __name__ == "__main__":
    main()