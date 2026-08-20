import pandas as pd
import numpy as np
from pathlib import Path

# DATA LOADING
def load_data():
    fname = "titanic_clean.csv"

    expected = Path(__file__).parent.parent / "week1" / "data" / fname
    if expected.exists():
        print(f"Data loaded successfully from: {expected}\n")
        return pd.read_csv(expected)

    for p in Path.cwd().rglob(fname):
        print(f"Data found in workspace at: {p}\n")
        return pd.read_csv(p)

    for p in Path(__file__).parent.parent.rglob(fname):
        print(f"Data found near script at: {p}\n")
        return pd.read_csv(p)

    try:
        print("Attempting to load by plain filename in CWD...")
        return pd.read_csv(fname)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find '{fname}'. Searched: {expected}, working directory, and script parents."
        )

def prepare_data(df):
    df_clean = df.copy()

    # 1. Family Size
    if "family_size" not in df_clean.columns:
        if "sibsp" in df_clean.columns and "parch" in df_clean.columns:
            df_clean["family_size"] = df_clean["sibsp"] + df_clean["parch"] + 1
        else:
            df_clean["family_size"] = 1

    # 2. Age Group 
    if "age_group" not in df_clean.columns and "age" in df_clean.columns:
        bins = [-1, 12, 18, 35, 60, 120]
        labels = ["Child", "Teen", "Young Adult", "Adult", "Senior"]
        df_clean["age_group"] = pd.cut(df_clean["age"], bins=bins, labels=labels)

    # 3. Numeric Survival Column 
    if "survived_num" not in df_clean.columns and "survived" in df_clean.columns:
        def _survived_to_int(val):
            if pd.isna(val):
                return 0
            s = str(val).strip().lower()
            if s in ("survived", "1", "true", "yes", "y"):
                return 1
            if s in ("died", "dead", "0", "false", "no", "n"):
                return 0
            try:
                return int(float(s))
            except Exception:
                return 0

        df_clean["survived_num"] = df_clean["survived"].apply(_survived_to_int)

    return df_clean


# 1. UNIVARIATE ANALYSIS
def univariate_analysis(df):

    print("\n")
    print("         1. UNIVARIATE ANALYSIS           ")
    print("\n")

    features = ["age", "fare", "family_size"]

    for col in features:
        if col not in df.columns:
            continue

        print(f"\n--- Feature: {col.upper()} ---")
        series = df[col].dropna()

        # Basic statistics
        mean_val = series.mean()
        median_val = series.median()
        mode_val = series.mode()[0] if not series.mode().empty else np.nan
        std_val = series.std()
        min_val = series.min()
        max_val = series.max()

        # Quartiles & IQR
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        # Outlier count using standard IQR rule
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_count = ((series < lower_bound) | (series > upper_bound)).sum()

        # Skewness calculation
        skew_val = series.skew()
        if skew_val > 0.5:
            skew_desc = "Right-skewed (Positive skew)"
        elif skew_val < -0.5:
            skew_desc = "Left-skewed (Negative skew)"
        else:
            skew_desc = "Roughly symmetric"

        print(f"Mean: {mean_val:.2f}")
        print(f"Median: {median_val:.2f}")
        print(f"Mode: {mode_val}")
        print(f"Std Dev: {std_val:.2f}")
        print(f"Min: {min_val} | Max: {max_val}")
        print(f"Q1: {q1:.2f} | Q3: {q3:.2f} | IQR: {iqr:.2f}")
        print(f"Skewness: {skew_val:.3f} -> {skew_desc}")
        print(f"Outlier Count (IQR Rule): {outlier_count}")



# 2. BIVARIATE ANALYSIS
def bivariate_analysis(df):
    print("\n")
    print("         2. BIVARIATE ANALYSIS            ")
    print("\n")

    # 1. Pearson Correlation Matrix
    print("\n--- Pearson Correlation Matrix ---")
    corr_matrix = df.corr(numeric_only=True)
    print(corr_matrix.round(3))

    # 2. Top 3 Strongest Correlations with Survived
    target_col = "survived_num" if "survived_num" in df.columns else "survived"
    if target_col in corr_matrix.columns:
        print(f"\n--- Top 3 Strongest Correlations with {target_col} ---")
        surv_corr = corr_matrix[target_col].drop(target_col)
        top_3 = surv_corr.abs().nlargest(3)
        for col in top_3.index:
            print(f"- {col}: {surv_corr[col]:+.3f}")

    # 3. Pivot Table: Survival Rate by Class and Sex
    if "pclass" in df.columns and "sex" in df.columns:
        print("\n--- Pivot Table: Survival Rate by Class and Sex ---")
        pivot = df.pivot_table(
            index="pclass", columns="sex", values=target_col, aggfunc="mean"
        )
        print((pivot * 100).round(2).astype(str) + "%")

    # 4. Crosstab: Age Group vs Survived (Counts and Row Percentages)
    if "age_group" in df.columns and "survived" in df.columns:
        print("\n--- Crosstab: Age Group vs Survived (Counts) ---")
        ct_counts = pd.crosstab(df["age_group"], df["survived"], margins=True)
        print(ct_counts)

        print("\n--- Crosstab: Age Group vs Survived (Row Percentages %) ---")
        ct_pct = (
            pd.crosstab(df["age_group"], df["survived"], normalize="index") * 100
        )
        print(ct_pct.round(2).astype(str) + "%")


# 3. MULTIVARIATE ANALYSIS

def multivariate_analysis(df):
    print("\n")
    print("         3. MULTIVARIATE ANALYSIS         ")
    print("\n")

    target_col = "survived_num" if "survived_num" in df.columns else "survived"

    # 1. Groupby pclass & sex: Mean Age, Mean Fare, Survival Rate in one table
    if all(col in df.columns for col in ["pclass", "sex", "age", "fare"]):
        print("\n--- Summary Table: Mean Age, Fare, & Survival Rate by Class & Sex ---")
        multi_grp = df.groupby(["pclass", "sex"]).agg(
            mean_age=("age", "mean"),
            mean_fare=("fare", "mean"),
            survival_rate=(target_col, "mean"),
        )
        # Format survival rate as percentage for output readability
        multi_grp["survival_rate"] = (multi_grp["survival_rate"] * 100).round(2).astype(str) + "%"
        multi_grp["mean_age"] = multi_grp["mean_age"].round(2)
        multi_grp["mean_fare"] = multi_grp["mean_fare"].round(2)
        print(multi_grp)

    # 2. Top 10 Highest-Fare Passengers
    print("\n--- Top 10 Highest-Fare Passengers ---")
    display_cols = [c for c in ["name", "pclass", "fare", "survived"] if c in df.columns]
    top_10 = df.nlargest(10, "fare")[display_cols]
    print(top_10.to_string(index=False))


if __name__ == "__main__":
    raw_data = load_data()
    titanic_df = prepare_data(raw_data)

    univariate_analysis(titanic_df)
    bivariate_analysis(titanic_df)
    multivariate_analysis(titanic_df)