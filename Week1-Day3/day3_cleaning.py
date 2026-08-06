import ssl
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "titanic_raw.csv"
CLEAN_DATA_PATH = BASE_DIR / "data" / "titanic_clean.csv"
DATASET_URL = ( "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

ssl._create_default_https_context = ssl._create_unverified_context


def load_and_save_raw_data():
    try:
        # Ensure data directory exists
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Download and save if missing, otherwise load existing local copy
        if not DATA_PATH.exists():
            print("Downloading raw Titanic dataset...")
            df = pd.read_csv(DATASET_URL)
            df.to_csv(DATA_PATH, index=False)
            print(f"Saved to: {DATA_PATH}")
        else:
            print(f"Loading local dataset from: {DATA_PATH}")
            df = pd.read_csv(DATA_PATH)

        return df

    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def profile_raw_data(df: pd.DataFrame):
    #Part 2.2: Profile the raw data
    print("                RAW DATA DIAGNOSTIC REPORT                ")

    # 1. Shape, Column Names, and Data Types
    print("\n--- 1. SHAPE, COLUMNS & DATA TYPES ---")
    print(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
    print(df.dtypes)

    # 2. Count and Percentage of Missing Values
    print("\n--- 2. MISSING VALUES REPORT ---")
    missing_count = df.isnull().sum()
    missing_pct = (df.isnull().mean() * 100).round(2)
    missing_df = pd.DataFrame(
        {"Missing Count": missing_count, "Missing Percentage (%)": missing_pct}
    )
    print(missing_df)

    # 3. Exact Duplicate Rows
    print("\n--- 3. DUPLICATE RECORDS ---")
    exact_duplicates = df.duplicated().sum()
    print(f"Number of exact duplicate rows: {exact_duplicates}")

    # 4. Value Counts for Categorical Columns
    print("\n--- 4. CATEGORICAL COLUMNS VALUE COUNTS ---")
    categorical_cols = [
        col
        for col in df.columns
        if pd.api.types.is_object_dtype(df[col])
        or pd.api.types.is_string_dtype(df[col])
        or isinstance(df[col].dtype, pd.CategoricalDtype)
    ]

    if categorical_cols:
        for col in categorical_cols:
            print(f"\nValue counts for column '{col}':")
            print(df[col].value_counts(dropna=False))
    else:
        print("No categorical columns found.")

    # 5. Statistical Summary for Numeric Columns
    print("\n--- 5. NUMERIC COLUMNS SUMMARY  ---")
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if numeric_cols:
        print(df.describe().T)
    else:
        print("No numeric columns found.")

    print("\n")

def clean_data(df: pd.DataFrame) -> pd.DataFrame: 
    #Part 2.3: Clean the raw data
    df_clean = df.copy()

    # 1. Standardise column names (lowercase with underscores)
    df_clean.columns = ( df_clean.columns.str.lower().str.replace(" ", "_"))

    # 2. Remove duplicate rows if any exist
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)

    # 3. Clean spaces and lower the casing for text columns
    text_cols = df_clean.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df_clean[col] = df_clean[col].astype("string").str.strip().str.lower()

    # 4. Fill missing age values with group median (by passenger class and sex)
    df_clean["age"] = df_clean.groupby(["pclass", "sex"])["age"].transform(lambda group: group.fillna(group.median()) )

    # 5. Fill missing embarked values with the most common value (mode)
    most_frequent_embarked = df_clean["embarked"].mode()[0]
    df_clean["embarked"] = df_clean["embarked"].fillna(most_frequent_embarked)

    # 6. Drop the cabin column because too many values are missing 
    df_clean = df_clean.drop(columns=["cabin"])

    # 7. Convert survived and pclass into readable categories
    survived_labels = {0: "Died", 1: "Survived"}
    pclass_labels = {1: "First", 2: "Second", 3: "Third"}

    df_clean["survived"] = (
        df_clean["survived"].map(survived_labels).astype("category")
    )
    df_clean["pclass"] = (
        df_clean["pclass"].map(pclass_labels).astype("category")
    )
    return df_clean


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    #Part2.4: Engineer three new columns
    # Make a copy to avoid altering the input dataset
    df_feat = df.copy()

    # 1. Extract 'title' from the 'name' column
    # Regex looks for letters right before a dot (e.g., "mr.", "miss.")
    df_feat["title"] = df_feat["name"].str.extract(r"([a-z]+)\.", expand=False)

    # Keep common titles, group rare titles into 'other'
    common_titles = ["mr", "mrs", "miss", "master"]
    df_feat["title"] = df_feat["title"].apply(
        lambda x: x if x in common_titles else "other"
    )

    # 2. Bin 'age' into 'age_group' using pd.cut()
    # Ranges: 0-12 (child), 13-19 (teen), 20-59 (adult), 60+ (senior)
    age_bins = [0, 12, 19, 59, 100]
    age_labels = ["child", "teen", "adult", "senior"]
    df_feat["age_group"] = pd.cut(
        df_feat["age"], bins=age_bins, labels=age_labels
    )

    # 3. Calculate 'family_size' (sibsp + parch + 1 for self)
    df_feat["family_size"] = df_feat["sibsp"] + df_feat["parch"] + 1

    return df_feat

def extract_insights(df: pd.DataFrame):
    #Part 2.5: Extract and print 5 key insights from the dataset.
    print("         PART 2.5: FIVE KEY INSIGHTS      ")

    # Convert 'survived' column into a boolean (True for Survived, False for Died)
    is_survived = df["survived"] == "Survived"

    # 1. Survival rate by passenger class
    print("\n1. Survival Rate by Passenger Class:")
    pclass_survival = is_survived.groupby(df["pclass"], observed=False).mean() * 100
    for pclass, rate in pclass_survival.items():
        print(f"   - {pclass} Class: {rate:.2f}%")

    # 2. Survival rate by sex
    print("\n2. Survival Rate by Sex:")
    sex_survival = is_survived.groupby(df["sex"]).mean() * 100
    for sex, rate in sex_survival.items():
        print(f"   - {sex.title()}: {rate:.2f}%")

    # 3. Survival rate by age_group
    print("\n3. Survival Rate by Age Group:")
    age_survival = is_survived.groupby(df["age_group"], observed=False).mean() * 100
    for group, rate in age_survival.items():
        print(f"   - {group.title()}: {rate:.2f}%")

    # 4. Average fare by passenger class
    print("\n4. Average Fare by Passenger Class:")
    avg_fare = df.groupby("pclass", observed=False)["fare"].mean()
    for pclass, fare in avg_fare.items():
        print(f"   - {pclass} Class: ${fare:.2f}")

    # 5. Insight of choice: Survival rate by title
    print("\n5. Survival Rate by Passenger Title (Custom Insight):")
    title_survival = is_survived.groupby(df["title"]).mean() * 100
    for title, rate in title_survival.items():
        print(f"   - Title '{title.title()}': {rate:.2f}%")


def export_clean_data(df: pd.DataFrame):
    #Part 2.6: Export cleaned dataset to CSV.
    CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"\nSuccessfully exported clean dataset to: {CLEAN_DATA_PATH}")


if __name__ == "__main__":
    df = load_and_save_raw_data()
    if df is not None:
        profile_raw_data(df)
        df_clean = clean_data(df)
        df_feat = engineer_features(df_clean)
        extract_insights(df_feat)
        export_clean_data(df_clean)
        print("\nFirst 5 rows of cleaned data:")
        print(df_clean.head())