# Day 11 — Model Evaluation

## Regression: Full Model Comparison (Cross-Validated)

| Metric     | LinearRegression | DecisionTree | RandomForest |
| ---------- | ---------------- | ------------ | ------------ |
| cv_mean_R2 | 0.962            | 0.795        | 0.916        |
| cv_std_R2  | 0.011            | 0.057        | 0.016        |
| test_MAE   | 6.194            | 14.839       | 8.839        |
| test_RMSE  | 8.343            | 19.325       | 11.788       |

The 5-fold cross-validation confirms yesterday's single-split result rather than overturning it: **Linear Regression is still the strongest model**, with the highest mean R² and importantly the lowest standard deviation across folds (0.011). A low std dev means the model performs consistently no matter which 20% of players end up in the test fold, which is exactly the stability cross-validation is meant to check for. The Decision Tree has both the worst mean R² and the highest std dev (0.057), confirming it's the least reliable of the three.

## Hyperparameter Tuning

`GridSearchCV` searched 9 combinations of `max_depth` ([5, 10, None]) and `min_samples_leaf` ([1, 3, 5]) for the Random Forest, each evaluated with 5-fold cross-validation.

**Best parameters found:** `max_depth=None, min_samples_leaf=1`
**Best cross-validated R²:** 0.922 (test set: MAE 8.839, RMSE 11.788, R² 0.926)

Interestingly, the best combination found turned out to be almost identical to scikit-learn's own defaults for these two parameters. Tuning only improved the mean CV R² from 0.916 to 0.922 a small gain. This tells me the Random Forest was already close to its ceiling on this feature set without tuning, and that the real story here is architectural: no version of the Random Forest beat plain Linear Regression on this dataset.

## Classification Results

Target: `high_performer` = 1 if `total_points` is above the 75th percentile (101.0 points) among 450+ minute players. Class balance: 75.7% not high performer, 24.3% high performer.

| Metric    | Logistic Regression | Random Forest |
| --------- | ------------------- | ------------- |
| Accuracy  | 0.926               | 0.951         |
| Precision | 0.900               | 1.000         |
| Recall    | 0.818               | 0.818         |
| F1        | 0.857               | 0.900         |

Random Forest wins outright: identical recall, but perfect precision (zero false positives) and a higher F1.

The Random Forest's confusion matrix shows **0 false positives** and **4 false negatives** out of 81 test players it never wrongly flagged someone as a high performer, but missed 4 genuine ones (Zinchenko, Senesi, Martinelli, Semenyo). All four have modest raw goals/assists relative to their minutes, suggesting they likely earned bonus points our leakage-safe feature set simply can't see.

## Precision vs. Recall — Which Matters More for Scouting?

If a club used this classifier to shortlist players to scout further, **a false positive is cheaper than a false negative**. A false positive just costs some wasted scouting hours on a player who turns out average annoying, but recoverable. A false negative means a genuinely valuable player never even gets looked at, and a rival club might sign them instead. Given that, **the model should be tuned toward recall**, even if it costs some precision missing good players is the more expensive mistake in this context.

By that standard, the current Random Forest (precision 1.000, recall 0.818) is actually tuned the wrong way for this use case it's being maximally cautious about false alarms at the cost of missing real talent. In a future iteration I'd lower the classification threshold or adjust `class_weight` to trade some precision for more recall.

## Which Model Goes in the Final Dashboard?

**Linear Regression** for the points-prediction task it's simpler, faster, more stable across folds, and outperformed both tree-based models on every regression metric. **Random Forest Classifier** for the high-performer flag despite the recall concern above, it's still the stronger of the two classifiers tested, and its zero-false-positive behavior is a reasonable, explainable default to ship, with the recall trade-off noted as a known limitation for scouting use.
