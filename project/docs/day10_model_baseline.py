import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
 

df = pd.read_csv("project/data/processed/players_clean.csv")
 
print("Loaded data. Shape:", df.shape)
 
df = df[df["minutes"] >= 450].copy()
 
print("After filtering to players with >= 450 minutes:", df.shape)
 
target_col = "total_points"
leakage_columns = ["bonus", "bps", "points_per_game", "points_per_million"]
 
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
 
print("\nFeatures after one-hot encoding:")
print(X.columns.tolist())
 
null_counts = X.isna().sum()
print("\nNull counts per feature (should all be 0):")
print(null_counts[null_counts > 0] if null_counts.sum() > 0 else "None - clean!")
 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
 
print("\nShapes after split:")
print("X_train:", X_train.shape)
print("X_test :", X_test.shape)
print("y_train:", y_train.shape)
print("y_test :", y_test.shape)
 
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit + transform on train
X_test_scaled = scaler.transform(X_test)          # ONLY transform on test
 
linear_model = LinearRegression()
linear_model.fit(X_train_scaled, y_train)
 
tree_model = DecisionTreeRegressor(max_depth=5, random_state=42)
tree_model.fit(X_train_scaled, y_train)
 
def evaluate(model, X_tr, y_tr, X_te, y_te):
    train_pred = model.predict(X_tr)
    test_pred = model.predict(X_te)
 
    results = {
        "train_MAE": mean_absolute_error(y_tr, train_pred),
        "test_MAE": mean_absolute_error(y_te, test_pred),
        "train_RMSE": np.sqrt(mean_squared_error(y_tr, train_pred)),
        "test_RMSE": np.sqrt(mean_squared_error(y_te, test_pred)),
        "train_R2": r2_score(y_tr, train_pred),
        "test_R2": r2_score(y_te, test_pred),
    }
    return results
 
linear_results = evaluate(linear_model, X_train_scaled, y_train, X_test_scaled, y_test)
tree_results = evaluate(tree_model, X_train_scaled, y_train, X_test_scaled, y_test)
 
comparison = pd.DataFrame(
    {"LinearRegression": linear_results, "DecisionTree": tree_results}
)
 
print("\n   MODEL COMPARISON TABLE    ")
print(comparison.round(3))
 

coef_df = pd.DataFrame({
    "feature": X.columns,
    "coefficient": linear_model.coef_
})
coef_df["abs_coefficient"] = coef_df["coefficient"].abs()
coef_df = coef_df.sort_values("abs_coefficient", ascending=False)
 
print("\n    LINEAR MODEL COEFFICIENTS (sorted by importance)     ")
print(coef_df[["feature", "coefficient"]].to_string(index=False))
 
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": tree_model.feature_importances_
}).sort_values("importance", ascending=False)
 
print("\n    DECISION TREE FEATURE IMPORTANCES    ")
print(importance_df.to_string(index=False))
 

test_predictions = tree_model.predict(X_test_scaled)
 
errors_df = pd.DataFrame({
    "full_name": df.loc[X_test.index, "full_name"].values,
    "actual_points": y_test.values,
    "predicted_points": test_predictions,
})
errors_df["abs_error"] = (errors_df["actual_points"] - errors_df["predicted_points"]).abs()
errors_df = errors_df.sort_values("abs_error", ascending=False)
 
print("\n    TOP 5 WORST PREDICTIONS (Decision Tree)    ")
print(errors_df.head(5).to_string(index=False))
 