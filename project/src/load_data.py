import urllib.request
from pathlib import Path
import pandas as pd

"""
load_data.py

Downloads the raw Fantasy Premier League player and team CSVs for the
2023-24 season and saves them locally to data/raw/. Skips downloading
if the files already exist, so the pipeline stays fast on repeat runs.
"""


# Define URLs
PLAYERS_URL = "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2023-24/players_raw.csv"
TEAMS_URL = "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2023-24/teams.csv"

# Set file paths using pathlib
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def download_file(url: str, destination: Path) -> None:
    """
    Download a file from a URL and save it locally, unless it already exists.

    Parameters:
        url (str): the web address of the file to download
        destination (Path): the local file path to save it to

    Returns:
        None
    """
    if destination.exists():
        print(f"File already exists: {destination.name}")
        return

    print(f"Downloading {destination.name}...")
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"Successfully downloaded {destination.name}")
    except Exception as e:
        print(f"Error downloading {destination.name}: {e}")
        raise


def acquire_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Download (if needed) and load the players and teams datasets.

    Creates the data/raw/ folder if it doesn't exist, downloads both
    CSVs, then loads them into DataFrames and prints a shape summary.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: the players dataframe and
        the teams dataframe, in that order
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    players_path = RAW_DATA_DIR / "players_raw.csv"
    teams_path = RAW_DATA_DIR / "teams.csv"

    # Download raw datasets
    download_file(PLAYERS_URL, players_path)
    download_file(TEAMS_URL, teams_path)

    # Load datasets
    df_players = pd.read_csv(players_path)
    df_teams = pd.read_csv(teams_path)

    print("\n    Data Acquisition Summary    ")
    print(f"Players Dataset Shape: {df_players.shape}")
    print(f"Teams Dataset Shape:   {df_teams.shape}")

    return df_players, df_teams


if __name__ == "__main__":
    acquire_data()