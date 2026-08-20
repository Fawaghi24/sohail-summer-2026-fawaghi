# Data Dictionary — Premier League 2023–24 Analytics Dataset

This document details the 20 primary features selected from the raw Fantasy Premier League dataset (`players_raw.csv`) for the performance and financial analysis pipeline in `clean_data.py`.

## Feature Mapping & Decoding Notes

- **Positions (`element_type`)**: `1` = Goalkeeper, `2` = Defender, `3` = Midfielder, `4` = Forward.
- **Teams (`team`)**: Foreign key matching the `id` column in `teams.csv`, used to attach the real club name.
- **Cost Normalization (`now_cost`)**: Stored in tenths of a million (e.g., `55` = £5.5m). Divided by `10` in `clean_data.py` to produce `cost_millions`.

---

## Core Selected Features (20 Columns)

| Column Name               | Data Type | Description                                      | Selection Rationale                                                                                                                                                        |
| :------------------------ | :-------- | :----------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                      | Integer   | Unique identifier for each player                | Primary key used for indexing and joining player records.                                                                                                                  |
| `first_name`              | String    | Player's first name                              | Combined with `second_name` to build the `full_name` column used throughout the analysis and dashboard.                                                                    |
| `second_name`             | String    | Player's surname                                 | Combined with `first_name` to build `full_name`.                                                                                                                           |
| `web_name`                | String    | Player's shorter display name (e.g., "Saka")     | Used in tables where a compact name is preferred over the full name.                                                                                                       |
| `element_type`            | Integer   | Position ID (1: GK, 2: DEF, 3: MID, 4: FWD)      | Mapped to a readable `position` label; essential for filtering and position-specific comparisons.                                                                          |
| `team`                    | Integer   | Team ID (foreign key matching `teams.csv`)       | Required to merge in the actual club name (`team_name`).                                                                                                                   |
| `now_cost`                | Integer   | Price stored in tenths of £m (e.g., 55 = £5.5m)  | Converted to `cost_millions`; core input for the value analysis and points-per-million feature.                                                                            |
| `minutes`                 | Integer   | Total minutes played across the season           | Core variable for per-90 normalisation, the minutes-played sample-size flag, and the 900-minute ranking filter.                                                            |
| `goals_scored`            | Integer   | Total goals scored                               | Primary attacking output metric; used to build `goals_per_90` and `xg_difference`.                                                                                         |
| `assists`                 | Integer   | Total assists provided                           | Primary playmaking output metric; used to build `assists_per_90` and `xa_difference`.                                                                                      |
| `expected_goals`          | Float     | Expected Goals (xG) based on shot quality        | Measures underlying chance quality; compared against actual goals to detect over/underperformance.                                                                         |
| `expected_assists`        | Float     | Expected Assists (xA) based on key pass quality  | Same logic as xG, applied to assists.                                                                                                                                      |
| `clean_sheets`            | Integer   | Matches where the player's team conceded 0 goals | Primary defensive performance indicator, especially relevant for defenders and goalkeepers.                                                                                |
| `goals_conceded`          | Integer   | Goals conceded while the player was on the pitch | Additional defensive-effectiveness signal used as a model feature.                                                                                                         |
| `expected_goals_conceded` | Float     | Expected goals conceded, based on shots faced    | Selected as a raw column but not used directly in the current feature set; kept for potential future defensive analysis.                                                   |
| `saves`                   | Integer   | Shots saved (goalkeepers)                        | Core workload/effectiveness metric for goalkeepers specifically.                                                                                                           |
| `bonus`                   | Integer   | Official FPL bonus points awarded                | **Excluded from the predictive model as a leakage column** (see `model.py`) since it is added directly into `total_points`. Retained in the cleaned dataset for reference. |
| `total_points`            | Integer   | Total FPL points accumulated over the season     | The primary target variable for the regression model and the basis for all ranking analyses.                                                                               |
| `yellow_cards`            | Integer   | Total yellow cards received                      | Discipline/availability signal; included as a minor model feature.                                                                                                         |
| `red_cards`               | Integer   | Total red cards received                         | Discipline/availability signal; included as a minor model feature.                                                                                                         |
