from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "diagnostic" / "data" / "students.csv"


def analyze_student_data():
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: Dataset file not found at {DATA_PATH}")
        return

    # 1. Shape of the dataset and info
    print("--- 1. Dataset Shape & Info ---")
    print(f"Shape (Rows, Columns): {df.shape}\n")                                   #Shape (Rows, Columns): (30, 7)
    df.info()
    print("\n\n")

    # 2. Full describe summary of numeric columns
    print("--- 2. Numerical Summary ---")
    print(df.describe())
    print("\n\n")

    # 3. Total student count & average GPA 
    print("--- 3. Total Student Count & Average GPA ---")
    total_students = len(df)
    avg_gpa = round(df["gpa"].mean(), 2)
    print(f"Total Students: {total_students}")                                  #Total Students: 30
    print(f"Average GPA: {avg_gpa}")                                            #Average GPA: 3.48     
    print("\n\n")

    # 4. Highest GPA student in each major 
    print("--- 4. Highest-GPA Student per Major ---")
    highest_gpa_idx = df.groupby("major")["gpa"].idxmax()
    highest_per_major = df.loc[highest_gpa_idx, ["major", "name", "gpa"]]
    print(highest_per_major.to_string(index=False))                                          #   major    name  gpa
                                                                                   #   Computer Science   Aisha 4.00
                                                                                     #    Cybersecurity  Fatima 3.90
                                                                                      #    Data Science Kaltham 3.92   
    print("\n\n")

    # 5. Count of students with more than 60 credits
    print("--- 5. Students with > 60 Credits ---")
    more_than_60 = (df["credits_completed"] > 60).sum()
    print(f"Count: {more_than_60}")                                                            # Count: 18
    print("\n\n")

    # 6. Average GPA per major
    print("--- 6. Average GPA per Major (Sorted) ---")
    avg_gpa_by_major = (
        df.groupby("major")["gpa"]
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )
    print(avg_gpa_by_major)                                                         #major
                                                                                    #Computer Science    3.55
                                                                                    #Data Science        3.47
                                                                                    #Cybersecurity       3.42
                                                                                    #Name: gpa, dtype: float64
    print("\n\n")

    # 7. Number of students per enrollment_year
    print("--- 7. Student Count per Enrollment Year ---")
    year_counts = df["enrollment_year"].value_counts().sort_index()
    print(year_counts)                                                          # enrollment_year
                                                                                    #2021    9
                                                                                    #2022    9
                                                                                    #2023    6
                                                                                    #2024    5
                                                                                    #2025    1
                                                                                    #Name: count, dtype: int64
    print("\n\n")

    # 8. Top 5 students overall by GPA
    print("--- 8. Top 5 Students Overall by GPA ---")
    top_5 = df.sort_values(by="gpa", ascending=False).head(5)[
        ["name", "major", "gpa"]
    ]
    print(top_5.to_string(index=False))                                     # name            major  gpa
                                                                            # Aisha Computer Science 4.00
                                                                            # Salama Computer Science 3.97
                                                                            # Kaltham     Data Science 3.92
                                                                            # Fatima    Cybersecurity 3.90
                                                                            # Sara Computer Science 3.90
    print("\n\n")

    # 9. Average credits completed split by is_active
    print("--- 9. Average Credits Completed by Active Status ---")
    avg_credits_active = (
        df.groupby("is_active")["credits_completed"].mean().round(2)
    )
    print(avg_credits_active)                                               # is_active
                                                                            # False    39.50
                                                                            # True     75.42
                                                                            # Name: credits_completed, dtype: float64
    print("\n\n")

    # 10. Count of students with GPA > average AND credits > 70
    print("--- 10. High Performers (GPA > Avg AND Credits > 70) ---")
    overall_avg_gpa = df["gpa"].mean()
    high_performers = df[
        (df["gpa"] > overall_avg_gpa) & (df["credits_completed"] > 70)
    ]
    print(f"Count: {len(high_performers)}")                                 #Count: 14


if __name__ == "__main__":
    analyze_student_data()