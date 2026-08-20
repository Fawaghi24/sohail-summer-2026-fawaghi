# Day 10 — Model Notes

## Features Selected

I used 15 raw features plus one-hot encoded `position` (3 dummy columns), giving 17 features total:

`minutes`, `goals_scored`, `assists`, `clean_sheets`, `goals_conceded`, `yellow_cards`, `red_cards`, `saves`, `now_cost`, `expected_goals`, `expected_assists`, `goals_per_90`, `assists_per_90`, `minutes_share`, `position_Forward`, `position_Goalkeeper`, `position_Midfielder`.

These are all things that describe how a player actually performed on the pitch (or their cost/position), not things that are mathematically derived from `total_points` itself. They're the kind of information you'd have _before_ knowing a player's final points total.

## Columns Excluded for Leakage

| Column               | Reason for exclusion                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------------------- |
| `bonus`              | Bonus points are added directly into `total_points`, so this is literally part of the target.                  |
| `bps`                | This is the raw score used to calculate bonus points, one step removed from the target, still derived from it. |
| `points_per_game`    | This is `total_points` divided by games played the target in a different shape.                                |
| `points_per_million` | This is `total_points` divided by cost again, the target hiding inside a ratio.                                |

## Results Table

| Metric     | LinearRegression | DecisionTree |
| ---------- | ---------------- | ------------ |
| train_MAE  | 6.095            | 8.476        |
| test_MAE   | 6.194            | 14.839       |
| train_RMSE | 7.857            | 11.192       |
| test_RMSE  | 8.343            | 19.325       |
| train_R2   | 0.970            | 0.938        |
| test_R2    | 0.963            | 0.801        |

## Which Model Performed Better

**Linear Regression** won clearly on the test set (R² 0.963 vs 0.801, MAE 6.19 vs 14.84). It also shows barely any gap between train and test scores, which means it generalized well rather than memorizing the training players.

The **Decision Tree** shows signs of overfitting: its train R² (0.938) is decent, but its test R² drops to 0.801 a much bigger train/test gap than the linear model. It learned some patterns specific to the training players that didn't hold up on new ones.

## Top Features: Do the Models Agree?

- **Linear model top 3** (by |coefficient|): `goals_scored`, `minutes`/`minutes_share` (tied), `assists`
- **Tree top 3** (by importance): `minutes_share`, `goals_scored`, `clean_sheets`
  Both models agree strongly that `goals_scored` and playing time (`minutes`/`minutes_share`) are the biggest drivers of total points reassuring, since two very different algorithms landed on the same story. They disagree on the third-most-important factor (assists vs. clean sheets), which makes sense since clean sheets matter a lot for defenders/goalkeepers specifically, while assists matter more broadly.

## Worst Prediction — Phil Foden

The tree predicted 178.5 points for Phil Foden but he actually scored 230 an error of 51.5 points, the single worst miss. My guess is the model likely failed to capture how much of his points came from bonus-style attacking involvement and match-winning contributions that aren't fully reflected in raw goals/assists/minutes alone. A player who has an outstanding, high-impact season relative to his raw stat line is exactly the kind of case a simple tree with limited depth struggles to predict.
