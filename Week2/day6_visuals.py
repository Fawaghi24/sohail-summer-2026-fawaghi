import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

if __name__ == "__main__":
    # Create charts directory if it does not exist
    output_dir = "week2/charts"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Load the cleaned dataset
    try:
        df = pd.read_csv("../Week1-Day3/data/titanic_clean.csv")
    except FileNotFoundError:
        df = pd.read_csv("Week1-Day3/data/titanic_clean.csv")

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # 2. Add age_group column if not already in dataframe
    if "age_group" not in df.columns:
        bins = [0, 12, 18, 35, 60, 120]
        labels = ["Child", "Teen", "Young Adult", "Adult", "Senior"]
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)

    # Chart 1: Age distribution histogram with KDE
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="age", kde=True, bins=30, color="teal")
    plt.title("Most Passengers Were Young Adults Aged 20 to 30")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/1_age_distribution_hist_kde.png", dpi=150)
    plt.close()

    # Chart 2: Fare boxplot grouped by pclass
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="pclass", y="fare", palette="Set2")
    plt.title("First-Class Fares Contain Extreme High-Value Outliers Above $500")
    plt.xlabel("Passenger Class")
    plt.ylabel("Fare")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/2_fare_boxplot_by_pclass.png", dpi=150)
    plt.close()

    # Chart 3: Survival rate by Sex and Pclass
    plt.figure(figsize=(8, 5))

    # Convert survived to numeric for calculating mean survival rate
    if df["survived"].dtype == "object" or isinstance(df["survived"].dtype, object):
        try:
            df["survived_num"] = (
                df["survived"].str.lower() == "survived"
            ).astype(int)
        except AttributeError:
            df["survived_num"] = df["survived"].astype(int)
    else:
        df["survived_num"] = df["survived"].astype(int)

    sns.barplot(
        data=df, x="pclass", y="survived_num", hue="sex", palette="viridis", ci=None
    )
    plt.title("First-Class Females Achieved Near-Universal Survival (~96%)")
    plt.xlabel("Passenger Class")
    plt.ylabel("Survival Rate")
    plt.legend(title="Sex")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/3_survival_rate_sex_pclass.png", dpi=150)
    plt.close()

    # Chart 4: Correlation heatmap of numeric columns
    plt.figure(figsize=(8, 6))
    numeric_df = df.select_dtypes(include=["number"])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Fare and Passenger Class Hold Strongest Negative Correlation (-0.55)")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/4_correlation_heatmap.png", dpi=150)
    plt.close()

    # Chart 5: Count plot of age_group with survived hue
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="age_group", hue="survived", palette="Set1")
    plt.title("Children Were the Only Age Group Where Survival Outnumbered Casualties")
    plt.xlabel("Age Group")
    plt.ylabel("Count")
    plt.legend(title="Survived")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/5_age_group_survived_countplot.png", dpi=150)
    plt.close()

    # Chart 6: Scatter plot of age vs fare
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df, x="age", y="fare", hue="survived", palette="Dark2", alpha=0.7
    )
    plt.title("Higher Fares Significantly Correlate with Increased Survival Rates")
    plt.xlabel("Age")
    plt.ylabel("Fare")
    plt.legend(title="Survived")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/6_age_vs_fare_scatterplot.png", dpi=150)
    plt.close()

    # Chart 7: Violin plot of age by pclass
    plt.figure(figsize=(8, 5))
    sns.violinplot(data=df, x="pclass", y="age", palette="Pastel1")
    plt.title("First-Class Passengers SKEW Significantly Older Than Third-Class")
    plt.xlabel("Passenger Class")
    plt.ylabel("Age")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/7_age_violinplot_by_pclass.png", dpi=150)
    plt.close()

    # Chart 8: 2x2 Subplot Dashboard
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Top Left: Age Histogram
    sns.histplot(data=df, x="age", kde=True, ax=axes[0, 0], color="teal")
    axes[0, 0].set_title("Age Distribution")

    # Top Right: Boxplot Fare by Pclass
    sns.boxplot(data=df, x="pclass", y="fare", ax=axes[0, 1], palette="Set2")
    axes[0, 1].set_title("Fare by Class")

    # Bottom Left: Survival Rate by Sex and Class
    sns.barplot(
        data=df,
        x="pclass",
        y="survived_num",
        hue="sex",
        ax=axes[1, 0],
        palette="viridis",
        ci=None,
    )
    axes[1, 0].set_title("Survival Rate by Sex and Class")

    # Bottom Right: Scatter plot Age vs Fare
    sns.scatterplot(
        data=df,
        x="age",
        y="fare",
        hue="survived",
        ax=axes[1, 1],
        palette="Dark2",
    )
    axes[1, 1].set_title("Age vs Fare")

    fig.suptitle("Titanic Exploratory Data Analysis Dashboard", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/8_titanic_eda_dashboard_2x2.png", dpi=150)
    plt.close()

    print("All charts created and saved in week2/charts/ folder successfully!")