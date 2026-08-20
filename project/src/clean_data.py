import numpy as np
import pandas as pd
from pathlib import Path

"""
clean_data.py

Cleans the raw FPL player data: selects the 20 relevant columns, merges
in club names from the teams data, converts cost to millions, fixes
numeric types, and engineers 8 new performance features (per-90 rates,
value ratios, and expected-vs-actual differences).
Input:  data/raw/players_raw.csv, data/raw/teams.csv
Output: data/processed/players_clean.csv
"""

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# 20 Chosen Columns from DATA_DICTIONARY.md
SELECTED_COLUMNS = [
    "id",
    "first_name",
    "second_name",
    "web_name",
    "element_type",
    "team",
    "now_cost",
    "minutes",
    "goals_scored",
    "assists",
    "expected_goals",
    "expected_assists",
    "clean_sheets",
    "goals_conceded",
    "expected_goals_conceded",
    "saves",
    "bonus",
    "total_points",
    "yellow_cards",
    "red_cards",
]

# Mapping rules
POSITION_MAP = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}


def load_raw_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the raw players and teams CSVs from data/raw/.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: the players dataframe and
        the teams dataframe, in that order
    """

    players_df = pd.read_csv(RAW_DIR / "players_raw.csv")
    teams_df = pd.read_csv(RAW_DIR / "teams.csv")
    return players_df, teams_df


def clean_and_transform(
    players_df: pd.DataFrame, teams_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Clean the raw player data and engineer new performance features.

    Selects the 20 relevant columns, builds a full_name and readable
    position label, merges in each player's club name, fixes numeric
    types, and adds 8 engineered features (per-90 stats, value ratios,
    and expected-vs-actual goal/assist differences).

    Parameters:
        players_df (pd.DataFrame): raw player data
        teams_df (pd.DataFrame): raw team/club data

    Returns:
        pd.DataFrame: the cleaned, feature-engineered player data
    """

    # 1. Select 20 chosen columns
    df = players_df[SELECTED_COLUMNS].copy()

    # 2. Combine full_name
    df["full_name"] = df["first_name"] + " " + df["second_name"]

    # 3. Map element_type to readable position names
    df["position"] = df["element_type"].map(POSITION_MAP)

    # 4. Merge players with teams to attach club name & verify merge integrity
    rows_before = len(df)
    df = pd.merge(
        df,
        teams_df[["id", "name"]],
        left_on="team",
        right_on="id",
        how="left",
        suffixes=("", "_team"),
    )
    df = df.rename(columns={"name": "team_name"}).drop(columns=["id_team"])

    # Verification: row count must remain unchanged and team_name cannot be null
    assert len(df) == rows_before, (
        f"Row count changed during merge! Before: {rows_before}, After: {len(df)}"
    )
    assert df["team_name"].isna().sum() == 0, (
        "Unmatched club IDs found after merge!"
    )

    # 5. Convert now_cost to millions
    df["cost_millions"] = df["now_cost"] / 10.0

    # 6. Convert numeric columns stored as text safely
    expected_cols = ["expected_goals", "expected_assists", "expected_goals_conceded"]
    for col in expected_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 7. Handle missing values
    df[expected_cols] = df[expected_cols].fillna(0.0)

    # 8. Add minutes_played_flag
    df["minutes_played_flag"] = np.where(df["minutes"] < 450, "Low Sample", "Sufficient Sample")


    # 2.4 Engineer Eight New Features 

    # Safe 90s denominator
    nineties = np.where(df["minutes"] > 0, df["minutes"] / 90.0, np.nan)

    # 1. goals_per_90
    df["goals_per_90"] = np.where(
        df["minutes"] > 0, df["goals_scored"] / nineties, 0.0
    )

    # 2. assists_per_90
    df["assists_per_90"] = np.where(
        df["minutes"] > 0, df["assists"] / nineties, 0.0
    )

    # 3. goal_involvements (goals + assists)
    df["goal_involvements"] = df["goals_scored"] + df["assists"]

    # 4. goal_involvements_per_90
    df["goal_involvements_per_90"] = np.where(
        df["minutes"] > 0, df["goal_involvements"] / nineties, 0.0
    )

    # 5. points_per_million 
    df["points_per_million"] = np.where(
        df["cost_millions"] > 0, df["total_points"] / df["cost_millions"], 0.0
    )

    # 6. xg_difference (actual goals minus expected goals)
    df["xg_difference"] = df["goals_scored"] - df["expected_goals"]

    # 7. xa_difference (actual assists minus expected assists)
    df["xa_difference"] = df["assists"] - df["expected_assists"]

    # 8. minutes_share (minutes played as % of max possible season minutes 3420)
    max_season_minutes = 38 * 90  # 3420 minutes
    df["minutes_share"] = (df["minutes"] / max_season_minutes) * 100.0

    return df


def export_and_verify(df: pd.DataFrame) -> None:
    """
    Save the cleaned dataset to CSV and print a verification report.

    Writes the cleaned data to data/processed/players_clean.csv, then
    prints the final shape, total null count, and a comparison of the
    top 5 players by goal involvements per 90 with and without a
    minimum-minutes filter (to show why sample size matters).

    Parameters:
        df (pd.DataFrame): the cleaned player data to export

    Returns:
        None
    """
    
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / "players_clean.csv"
    df.to_csv(out_path, index=False)

    print("\n                 VERIFICATION BLOCK               ")
    print(f"Processed Dataset Shape: {df.shape}")
    print(f"Total Null Values across Dataset: {df.isna().sum().sum()}")

    # Sample Size Comparison Requirement:
    # 1. Top 5 WITHOUT minutes filter
    top5_unfiltered = df.sort_values(
        by="goal_involvements_per_90", ascending=False
    )[["web_name", "team_name", "minutes", "goal_involvements", "goal_involvements_per_90"]].head(5)

    print("\n   Top 5 Players by Goal Involvements per 90 (UNFILTERED - includes Low Sample)    ")
    print(top5_unfiltered.to_string(index=False))

    # 2. Top 5 WITH 900+ minutes filter
    filtered_df = df[df["minutes"] >= 900]
    top5_filtered = filtered_df.sort_values(
        by="goal_involvements_per_90", ascending=False
    )[["web_name", "team_name", "minutes", "goal_involvements", "goal_involvements_per_90"]].head(5)

    print("\n    Top 5 Players by Goal Involvements per 90 (FILTERED: Minutes >= 900)    ")
    print(top5_filtered.to_string(index=False))
    print("\n")


if __name__ == "__main__":
    raw_players, raw_teams = load_raw_data()
    clean_df = clean_and_transform(raw_players, raw_teams)
    export_and_verify(clean_df)