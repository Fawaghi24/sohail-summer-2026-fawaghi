import pandas as pd
from pathlib import Path

"""
analysis.py

Performs the exploratory data analysis (EDA) on the cleaned player
dataset: a league overview, positional breakdown, club-level summary,
value-for-money ranking, and an expected-goals accuracy check.
Ranking-based sections use only players with 900+ minutes, to avoid
small-sample-size noise skewing the results.
Input: data/processed/players_clean.csv
"""

MINUTES_THRESHOLD = 900
 
def load_data():
    """
    Load the cleaned player dataset from data/processed/players_clean.csv.

    Returns:
        pd.DataFrame: the cleaned player data

    Raises:
        FileNotFoundError: if the cleaned CSV doesn't exist yet
    """
     
    project_folder = Path(__file__).parent.parent
    csv_path = project_folder / "data" / "processed" / "players_clean.csv"
 
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} players from {csv_path}\n")
        return df
    except FileNotFoundError:
        print(f"Could not find the file at {csv_path}.")
        print("Make sure you ran clean_data.py first (Day 7).")
        raise
 
 
def league_overview(df):
    """
    Print a high-level league summary: player counts by position and
    club, the distribution of total points, and the top 10 scorers.

    Parameters:
        df (pd.DataFrame): the full (unfiltered) player dataset

    Returns:
        None
    """

    print("\n")
    print("1. LEAGUE OVERVIEW")
    print("\n")
 
    print(f"\nTotal players in dataset: {len(df)}")
 
    print("\nPlayers by position:")
    print(df["position"].value_counts())
 
    print("\nPlayers by club:")
    print(df["team_name"].value_counts())
 
    print("\nDistribution of total points:")
    print(f"  Mean:     {df['total_points'].mean():.2f}")
    print(f"  Median:   {df['total_points'].median():.2f}")
    print(f"  Skewness: {df['total_points'].skew():.2f}")
 
 
    print("\nTop 10 highest-scoring players overall:")
    top_10_overall = df.sort_values("total_points", ascending=False).head(10)
    print(top_10_overall[["full_name", "position", "team_name", "total_points"]])
 
 
def positional_analysis(df, df_filtered):
    """
    Print positional averages, the top 5 players per position by goal
    involvements per 90, and each player's percentile rank within
    their own position by total points.

    Parameters:
        df (pd.DataFrame): the full player dataset, used for the
            position-level averages
        df_filtered (pd.DataFrame): players with 900+ minutes only,
            used for the ranking-based sections

    Returns:
        pd.DataFrame: df_filtered, with a new points_percentile_in_position
        column added
    """
 
    print("\n")
    print("2. POSITIONAL ANALYSIS")
    print(f"(Rankings below use only players with {MINUTES_THRESHOLD}+ minutes)")
    print("\n")
 
    print("\nAverage goals/90, assists/90 and total points, by position:")
    position_summary = df.groupby("position").agg(
        avg_goals_per_90=("goals_per_90", "mean"),
        avg_assists_per_90=("assists_per_90", "mean"),
        avg_total_points=("total_points", "mean"),
    )
    print(position_summary.round(2))
 
    # Top 5 players in each position by goal_involvements_per_90.
    print(f"\nTop 5 players per position by goal involvements per 90 "
          f"(min {MINUTES_THRESHOLD} minutes):")
    for position in df_filtered["position"].unique():
        print(f"\n  -- {position} --")
        players_in_position = df_filtered[df_filtered["position"] == position]
        top_5 = players_in_position.sort_values(
            "goal_involvements_per_90", ascending=False
        ).head(5)
        print(top_5[["full_name", "team_name", "goal_involvements_per_90"]]
              .to_string(index=False))
 

    df_filtered = df_filtered.copy() 
    df_filtered["points_percentile_in_position"] = (
        df_filtered.groupby("position")["total_points"]
        .rank(pct=True) * 100
    )
    print("\nSample of players with their percentile rank within their position:")
    print(df_filtered[["full_name", "position", "total_points",
                        "points_percentile_in_position"]]
          .sort_values("points_percentile_in_position", ascending=False)
          .head(10)
          .round(1)
          .to_string(index=False))
 
    return df_filtered  
 
 
def club_analysis(df):
    """
    Print club-level totals: points per club, most/least expensive
    squads, and the club with the highest combined goal involvements.

    Parameters:
        df (pd.DataFrame): the full (unfiltered) player dataset

    Returns:
        None
    """
    print("\n")
    print("3. CLUB ANALYSIS")
    print("\n")
 
    print("\nTotal points and average points per player, by club (ranked):")
    club_points = df.groupby("team_name").agg(
        total_points=("total_points", "sum"),
        avg_points_per_player=("total_points", "mean"),
    ).sort_values("total_points", ascending=False)
    print(club_points.round(2))
 
    print("\nMost expensive squad (by total now_cost):")
    club_cost = df.groupby("team_name")["now_cost"].sum().sort_values(ascending=False)
    print(f"  {club_cost.index[0]}: £{club_cost.iloc[0]:.1f}m")
 
    print("Cheapest squad (by total now_cost):")
    print(f"  {club_cost.index[-1]}: £{club_cost.iloc[-1]:.1f}m")
 
    print("\nClub with the highest combined goal involvements:")
    club_involvements = df.groupby("team_name")["goal_involvements"].sum() \
        .sort_values(ascending=False)
    print(f"  {club_involvements.index[0]}: {club_involvements.iloc[0]} "
          f"goal involvements")
 
 
def value_analysis(df_filtered):
    """
    Print the top 10 players by points per million spent, the top 10
    highest-cost players, and how much overlap exists between the two
    lists (i.e. whether expensive players are also good value).

    Parameters:
        df_filtered (pd.DataFrame): players with 900+ minutes only

    Returns:
        None
    """
 
    print("\n")
    print("4. VALUE ANALYSIS")
    print(f"(min {MINUTES_THRESHOLD} minutes)")
    print("\n")
 
    print("\nTop 10 players by points per million:")
    top_value = df_filtered.sort_values(
        "points_per_million", ascending=False
    ).head(10)
    print(top_value[["full_name", "team_name", "now_cost",
                      "total_points", "points_per_million"]]
          .to_string(index=False))
 
    print("\nTop 10 highest-cost players:")
    top_cost = df_filtered.sort_values("now_cost", ascending=False).head(10)
    print(top_cost[["full_name", "team_name", "now_cost",
                     "total_points"]].to_string(index=False))
 
    value_names = set(top_value["full_name"])
    cost_names = set(top_cost["full_name"])
    overlap = value_names.intersection(cost_names)
 
    print(f"\nOverlap between 'best value' and 'most expensive' lists: "
          f"{len(overlap)} player(s)")
    if overlap:
        print(f"  Players in both lists: {', '.join(overlap)}")
    else:
        print("  No overlap - the most expensive players are NOT the best value.")
 
 
def expected_goals_analysis(df_filtered):
    """
    Print the biggest over- and under-performers relative to expected
    goals, and the overall correlation between expected and actual
    goals scored.

    Parameters:
        df_filtered (pd.DataFrame): players with 900+ minutes only

    Returns:
        None
    """
   
    print("\n")
    print("5. EXPECTED GOALS ANALYSIS")
    print(f"(min {MINUTES_THRESHOLD} minutes)")
    print("\n")
 
    print("\nTop 10 overperformers (scoring more than expected):")
    overperformers = df_filtered.sort_values(
        "xg_difference", ascending=False
    ).head(10)
    print(overperformers[["full_name", "team_name", "expected_goals",
                           "goals_scored", "xg_difference"]]
          .to_string(index=False))
 
    print("\nTop 10 underperformers (scoring less than expected):")
    underperformers = df_filtered.sort_values(
        "xg_difference", ascending=True
    ).head(10)
    print(underperformers[["full_name", "team_name", "expected_goals",
                            "goals_scored", "xg_difference"]]
          .to_string(index=False))
 
    correlation = df_filtered["expected_goals"].corr(df_filtered["goals_scored"])
    print(f"\nCorrelation between expected_goals and goals_scored: "
          f"{correlation:.2f}")
 
 
def main():
    """
    Run the full EDA pipeline: load the data, apply the minutes
    filter, then run each analysis section in order.

    Returns:
        None
    """
   
    df = load_data()
 
    df_filtered = df[df["minutes"] >= MINUTES_THRESHOLD].copy()
    print(f"Players with {MINUTES_THRESHOLD}+ minutes (used for all "
          f"rankings): {len(df_filtered)} out of {len(df)}\n")
 
    league_overview(df)
    positional_analysis(df, df_filtered)
    club_analysis(df)
    value_analysis(df_filtered)
    expected_goals_analysis(df_filtered)
 
    print("\n")
    print("Analysis complete.")
    print("\n")
 
 
if __name__ == "__main__":
    main()
