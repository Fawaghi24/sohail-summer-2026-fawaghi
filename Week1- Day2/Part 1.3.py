from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "diagnostic" / "data" / "students.csv"

try:
    df=pd.read_csv(FILE_PATH)

    print(df.head(2))
    print(df.shape)
    print(df.info())
    print(df.describe())

    print(df.loc[0, "name"])
    print(df.iloc[0, 1])
    print(df.iloc[0:2, 0:2]) 

    high_gpa = df[df["gpa"] > 3.5]
    print(high_gpa)

    it_high_gpa = df[(df["major"] == "Computer Science") & (df["gpa"] > 3.5)]
    print(it_high_gpa)

    print(df["gpa"].mean())  
    print(df["credits_completed"].max())  
    print(df["major"].value_counts())  

    dept_stats = df.groupby("major").agg(
    avg_gpa=("gpa", "mean"),
    max_credits_completed=("credits_completed", "max")
    )

    sorted_stats = dept_stats.sort_values(by="avg_gpa", ascending=False)
    print(sorted_stats)


except FileNotFoundError:
    print(f"File not found at: {FILE_PATH}")
    print("Please ensure the 'students.csv' file is in the correct directory.")