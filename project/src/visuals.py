import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

"""
visuals.py

Generates 8 charts from the cleaned player dataset: a points
distribution, positional/club comparisons, a cost-vs-points value
chart, an expected-vs-actual goals chart, a top-15 ranking, a
correlation heatmap, and a 2x2 summary dashboard. Chart titles are
written as findings rather than plain descriptions.
Input:  data/processed/players_clean.csv
Output: charts/*.png (8 files)
"""

MINUTES_THRESHOLD = 900
 
sns.set_theme(style="whitegrid")
 
def load_data():
    """Load the cleaned player dataset. Returns: pd.DataFrame."""

    project_folder = Path(__file__).parent.parent
    csv_path = project_folder / "data" / "processed" / "players_clean.csv"
 
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} players from {csv_path}")
        return df
    except FileNotFoundError:
        print(f"Could not find {csv_path}. Run clean_data.py first.")
        raise
 
 
def get_charts_folder():
    """Create (if needed) and return the path to project/charts/. Returns: Path."""

    charts_folder = Path(__file__).parent.parent / "charts"
    charts_folder.mkdir(exist_ok=True)
    return charts_folder
 
 
def save_chart(fig, filename, charts_folder):
    """Save a matplotlib figure to the charts folder at 150 dpi and close it.
    Parameters: fig (Figure), filename (str), charts_folder (Path). Returns: None."""

    path = charts_folder / filename
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  Saved: {path.name}")
    plt.close(fig)  
 
 
def chart_1_points_distribution(df, charts_folder):
    """Save a histogram+KDE of total points across all players.
    Parameters: df (pd.DataFrame), charts_folder (Path). Returns: None."""

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["total_points"], kde=True, ax=ax, color="steelblue")
 
    mean_points = df["total_points"].mean()
    ax.set_title(
        f"Most players score under {round(mean_points)} points; "
        f"a small group of stars pull the average up",
        fontsize=11,
    )
    ax.set_xlabel("Total points (season)")
    ax.set_ylabel("Number of players")
    save_chart(fig, "01_points_distribution.png", charts_folder)
 
 
def chart_2_points_per_90_by_position(df, charts_folder):
    """Save a box plot of points-per-90 grouped by position.
    Parameters: df (pd.DataFrame), charts_folder (Path). Returns: None."""

    df = df.copy()
    df["points_per_90"] = df.apply(
        lambda row: (row["total_points"] / (row["minutes"] / 90))
        if row["minutes"] > 0 else None,
        axis=1,
    )
 
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="position", y="points_per_90", ax=ax)

    ax.set_title(
        "Points efficiency varies by position; forwards score most points per 90 minutes",
        fontsize=11,
    )
    ax.set_xlabel("Position")
    ax.set_ylabel("Points per 90 minutes")
    save_chart(fig, "02_points_per_90_by_position.png", charts_folder)
 
 
def chart_3_total_points_by_club(df, charts_folder):
    """Save a bar chart of total points summed by club, sorted descending.
    Parameters: df (pd.DataFrame), charts_folder (Path). Returns: None."""

    club_totals = (
        df.groupby("team_name")["total_points"]
        .sum()
        .sort_values(ascending=False)
    )
 
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=club_totals.values, y=club_totals.index, ax=ax, color="seagreen")
 
    top_club = club_totals.index[0]
    ax.set_title(f"{top_club} squad scored the most total points in the league", fontsize=11)
    ax.set_xlabel("Total points (all players combined)")
    ax.set_ylabel("Club")
    save_chart(fig, "03_total_points_by_club.png", charts_folder)
 
 
def chart_4_cost_vs_points(df_filtered, charts_folder):
    """Save a scatter plot of cost vs total points, coloured by position.
    Parameters: df_filtered (pd.DataFrame, 900+ min players), charts_folder (Path). Returns: None."""

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=df_filtered, x="now_cost", y="total_points",
        hue="position", ax=ax, alpha=0.7,
    )

    ax.set_title(
        "Higher-cost players generally score more points, but value varies by position",
        fontsize=11,
    )
    ax.set_xlabel("Cost (£ millions)")
    ax.set_ylabel("Total points (season)")
    ax.legend(title="Position")
    save_chart(fig, "04_cost_vs_points.png", charts_folder)
 
 
def chart_5_expected_vs_actual_goals(df_filtered, charts_folder):
    """Save a scatter plot of expected vs actual goals with a diagonal reference line.
    Parameters: df_filtered (pd.DataFrame, 900+ min players), charts_folder (Path). Returns: None."""

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=df_filtered, x="expected_goals", y="goals_scored",
        ax=ax, alpha=0.6, color="darkorange",
    )
 
    max_value = max(df_filtered["expected_goals"].max(),
                     df_filtered["goals_scored"].max())
    ax.plot([0, max_value], [0, max_value], linestyle="--", color="gray",
            label="Perfect prediction (actual = expected)")
 
    ax.set_title(
        "Most players score close to their expected goals; a few "
        "strikers consistently beat the model",
        fontsize=11,
    )
    ax.set_xlabel("Expected goals (xG)")
    ax.set_ylabel("Actual goals scored")
    ax.legend()
    save_chart(fig, "05_expected_vs_actual_goals.png", charts_folder)
 
 
def chart_6_top_15_goal_involvements(df_filtered, charts_folder):
    """Save a horizontal bar chart of the top 15 players by goal involvements per 90.
    Parameters: df_filtered (pd.DataFrame, 900+ min players), charts_folder (Path). Returns: None."""

    top_15 = df_filtered.sort_values(
        "goal_involvements_per_90", ascending=False
    ).head(15)
 
    fig, ax = plt.subplots(figsize=(8, 7))
    sns.barplot(
        data=top_15, x="goal_involvements_per_90", y="full_name",
        ax=ax, color="mediumpurple",
    )
 
    ax.set_title(
        f"{top_15.iloc[0]['full_name']} leads the league in goal "
        f"involvements per 90 minutes",
        fontsize=11,
    )
    ax.set_xlabel("Goal involvements per 90 minutes")
    ax.set_ylabel("Player")
    save_chart(fig, "06_top_15_goal_involvements.png", charts_folder)
 
 
def chart_7_correlation_heatmap(df, charts_folder):
    """Save an annotated correlation heatmap of the engineered numeric features.
    Parameters: df (pd.DataFrame), charts_folder (Path). Returns: None."""

    engineered_columns = [
        "goals_per_90", "assists_per_90", "goal_involvements",
        "goal_involvements_per_90", "points_per_million",
        "xg_difference", "xa_difference", "minutes_share",
    ]
    correlation_matrix = df[engineered_columns].corr()
 
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(
        correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm",
        center=0, ax=ax,
    )
 
    ax.set_title(
        "Goal involvements and goals-per-90 are strongly correlated, "
        "as expected",
        fontsize=11,
    )
    save_chart(fig, "07_correlation_heatmap.png", charts_folder)
 
 
def chart_8_dashboard(df, df_filtered, charts_folder):
    """Save a 2x2 dashboard combining 4 key charts into one summary image.
    Parameters: df (pd.DataFrame), df_filtered (pd.DataFrame, 900+ min players), charts_folder (Path). Returns: None."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
 
    # Top-left: points distribution
    sns.histplot(df["total_points"], kde=True, ax=axes[0, 0], color="steelblue")
    axes[0, 0].set_title("Points distribution across the league", fontsize=10)
    axes[0, 0].set_xlabel("Total points")
    axes[0, 0].set_ylabel("Number of players")
 
    # Top-right: total points by club
    club_totals = df.groupby("team_name")["total_points"].sum() \
        .sort_values(ascending=False).head(10)
    sns.barplot(x=club_totals.values, y=club_totals.index,
                ax=axes[0, 1], color="seagreen")
    axes[0, 1].set_title("Top 10 clubs by total points", fontsize=10)
    axes[0, 1].set_xlabel("Total points")
    axes[0, 1].set_ylabel("Club")
 
    # Bottom-left: cost vs points
    sns.scatterplot(data=df_filtered, x="now_cost", y="total_points",
                     hue="position", ax=axes[1, 0], alpha=0.7)
    axes[1, 0].set_title("Cost vs points (value chart)", fontsize=10)
    axes[1, 0].set_xlabel("Cost (£m)")
    axes[1, 0].set_ylabel("Total points")
 
    # Bottom-right: top 15 goal involvements per 90
    top_15 = df_filtered.sort_values(
        "goal_involvements_per_90", ascending=False
    ).head(15)
    sns.barplot(data=top_15, x="goal_involvements_per_90", y="full_name",
                ax=axes[1, 1], color="mediumpurple")
    axes[1, 1].set_title("Top 15 by goal involvements/90", fontsize=10)
    axes[1, 1].set_xlabel("Goal involvements per 90")
    axes[1, 1].set_ylabel("")
 
    fig.suptitle("Premier League 2023-24 - Season Dashboard", fontsize=14)
    plt.tight_layout()  
    save_chart(fig, "08_dashboard.png", charts_folder)
 
 
def main():
    """Run the full chart-generation pipeline: load data, apply the minutes filter, then generate and save all 8 charts. Returns: None."""
    df = load_data()
    df_filtered = df[df["minutes"] >= MINUTES_THRESHOLD].copy()
    print(f"Using {len(df_filtered)} players with {MINUTES_THRESHOLD}+ "
          f"minutes for ranking-based charts.\n")
 
    charts_folder = get_charts_folder()
 
    print("Creating charts...")
    chart_1_points_distribution(df, charts_folder)
    chart_2_points_per_90_by_position(df, charts_folder)
    chart_3_total_points_by_club(df, charts_folder)
    chart_4_cost_vs_points(df_filtered, charts_folder)
    chart_5_expected_vs_actual_goals(df_filtered, charts_folder)
    chart_6_top_15_goal_involvements(df_filtered, charts_folder)
    chart_7_correlation_heatmap(df, charts_folder)
    chart_8_dashboard(df, df_filtered, charts_folder)
 
    print("\nAll 8 charts saved successfully.")
 
 
if __name__ == "__main__":
    main()
 