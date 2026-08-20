import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from pathlib import Path

"""
app.py

Interactive Streamlit dashboard for exploring 2023-24 Premier League
player data. Lets the user filter by position, club, minutes, and
cost, then browse a sortable player table, view interactive charts,
compare two players head-to-head, and get a predicted season points
total from a Random Forest model trained on the fly.
Input: data/processed/players_clean.csv
Run with: streamlit run app.py
"""

st.set_page_config(
    page_title="Premier League Player Analytics",
    page_icon="⚽",
    layout="wide",
)

# DATA LOADING 
@st.cache_data
def load_data():
    script_dir = Path(__file__).parent
    csv_path = script_dir / "data" / "processed" / "players_clean.csv"
    df = pd.read_csv(csv_path)
    return df
 
 
df = load_data()
 
# MODEL TRAINING 
LEAKAGE_COLUMNS = ["bonus", "bps", "points_per_game", "points_per_million"]
 
MODEL_FEATURES = [
    "minutes", "goals_scored", "assists", "clean_sheets", "goals_conceded",
    "yellow_cards", "red_cards", "saves", "now_cost",
    "expected_goals", "expected_assists", "goals_per_90", "assists_per_90",
    "minutes_share", "position",
]
 
 
@st.cache_resource
def train_model(data):
    model_df = data[data["minutes"] >= 450].copy()
 
    X = model_df[MODEL_FEATURES].copy()
    X = pd.get_dummies(X, columns=["position"], drop_first=True)
    y = model_df["total_points"]
 
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
 
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
 
    return model, X_train.columns.tolist()
 
 
trained_model, model_columns = train_model(df)
 
# SIDEBAR FILTERS
st.sidebar.header("Filters")
 
all_positions = sorted(df["position"].dropna().unique().tolist())
all_clubs = sorted(df["team_name"].dropna().unique().tolist())
 
if st.sidebar.button("Reset all filters"):
    st.session_state["position_filter"] = all_positions
    st.session_state["club_filter"] = all_clubs
    st.session_state["min_minutes"] = 0
    st.session_state["max_cost"] = float(df["now_cost"].max())
 
selected_positions = st.sidebar.multiselect(
    "Position", options=all_positions, default=all_positions, key="position_filter"
)
 
selected_clubs = st.sidebar.multiselect(
    "Club", options=all_clubs, default=all_clubs, key="club_filter"
)
 
min_minutes = st.sidebar.slider(
    "Minimum minutes played",
    min_value=0,
    max_value=int(df["minutes"].max()),
    value=0,
    key="min_minutes",
)
 
max_cost = st.sidebar.slider(
    "Maximum cost (millions)",
    min_value=float(df["now_cost"].min()),
    max_value=float(df["now_cost"].max()),
    value=float(df["now_cost"].max()),
    key="max_cost",
)
 
# APPLY FILTERS
filtered_df = df[
    (df["position"].isin(selected_positions))
    & (df["team_name"].isin(selected_clubs))
    & (df["minutes"] >= min_minutes)
    & (df["now_cost"] <= max_cost)
].copy()
 
st.title("⚽ Premier League Player Analytics")
 
# EMPTY STATE HANDLING 
if filtered_df.empty:
    st.warning(
        "No players match the current filters. Try widening your "
        "selections in the sidebar (e.g. add more positions/clubs, "
        "lower the minutes minimum, or raise the cost maximum)."
    )
    st.stop()
 
# SECTION 1 - OVERVIEW
st.header("Overview")
 
col1, col2, col3, col4 = st.columns(4)
 
with col1:
    st.metric("Players shown", len(filtered_df))
 
with col2:
    st.metric("Average total points", round(filtered_df["total_points"].mean(), 1))
 
with col3:
    top_scorer = filtered_df.loc[filtered_df["total_points"].idxmax()]
    st.metric("Highest scorer", top_scorer["full_name"], f"{top_scorer['total_points']} pts")
 
with col4:
    best_value = filtered_df.loc[filtered_df["points_per_million"].idxmax()]
    st.metric(
        "Best value player",
        best_value["full_name"],
        f"{round(best_value['points_per_million'], 2)} pts/£m",
    )
 
# SECTION 2 - PLAYER EXPLORER
st.header("Player Explorer")
 
explorer_cols = [
    "full_name", "team_name", "position", "minutes", "goals_scored",
    "assists", "total_points", "now_cost", "points_per_million",
]
 
st.dataframe(filtered_df[explorer_cols], use_container_width=True)
 
csv_data = filtered_df[explorer_cols].to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered players as CSV",
    data=csv_data,
    file_name="filtered_players.csv",
    mime="text/csv",
)
 
# SECTION 3 - VISUAL ANALYSIS
st.header("Visual Analysis")
 
sns.set_theme(style="whitegrid")
 
# --- Chart A: cost vs points scatter, coloured by position ---
st.subheader("Cost vs. Points")
fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=filtered_df, x="now_cost", y="total_points", hue="position", ax=ax1
)
ax1.set_xlabel("Cost (£m)")
ax1.set_ylabel("Total points")
ax1.set_title("Higher cost does not always mean higher points")
st.pyplot(fig1)
 
# --- Chart B: top N players by a user-chosen metric ---
st.subheader("Top Players by Metric")
metric_options = ["total_points", "goals_scored", "assists", "goal_involvements_per_90", "points_per_million"]
chosen_metric = st.selectbox("Choose a metric", options=metric_options)
top_n = st.slider("How many players to show", min_value=5, max_value=25, value=10)
 
top_players = filtered_df.nlargest(top_n, chosen_metric)
 
fig2, ax2 = plt.subplots(figsize=(8, max(4, top_n * 0.35)))
sns.barplot(data=top_players, x=chosen_metric, y="full_name", ax=ax2, color="steelblue")
ax2.set_xlabel(chosen_metric)
ax2.set_ylabel("")
ax2.set_title(f"Top {top_n} players by {chosen_metric}")
st.pyplot(fig2)
 
# --- Chart C: positional comparison on a user-chosen metric ---
st.subheader("Positional Comparison")
position_metric = st.selectbox(
    "Compare positions by", options=metric_options, key="position_metric"
)
position_avg = (
    filtered_df.groupby("position")[position_metric].mean().sort_values(ascending=False)
)
 
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.barplot(x=position_avg.index, y=position_avg.values, ax=ax3, color="darkorange")
ax3.set_xlabel("Position")
ax3.set_ylabel(f"Average {position_metric}")
ax3.set_title(f"Average {position_metric} by position")
st.pyplot(fig3)
 
# SECTION 4 - PLAYER COMPARISON
st.header("Player Comparison")
 
player_names = sorted(filtered_df["full_name"].unique().tolist())
 
comp_col1, comp_col2 = st.columns(2)
with comp_col1:
    player_a_name = st.selectbox("Player A", options=player_names, index=0)
with comp_col2:
    player_b_name = st.selectbox(
        "Player B", options=player_names, index=min(1, len(player_names) - 1)
    )
 
player_a = filtered_df[filtered_df["full_name"] == player_a_name].iloc[0]
player_b = filtered_df[filtered_df["full_name"] == player_b_name].iloc[0]
 
compare_stats = ["total_points", "goals_scored", "assists", "minutes", "now_cost", "points_per_million"]
 
display_col1, display_col2 = st.columns(2)
 
with display_col1:
    st.subheader(player_a_name)
    for stat in compare_stats:
        leader = "🟢" if player_a[stat] >= player_b[stat] else ""
        st.write(f"**{stat}**: {player_a[stat]} {leader}")
 
with display_col2:
    st.subheader(player_b_name)
    for stat in compare_stats:
        leader = "🟢" if player_b[stat] >= player_a[stat] else ""
        st.write(f"**{stat}**: {player_b[stat]} {leader}")
 
# SECTION 5 - PREDICTION
st.header("Predict Total Points")
 
st.caption(
    "⚠️ This is an estimate from a single-season model, not a forecast. "
    "Real performance depends on many factors the model has never seen."
)
 
pred_col1, pred_col2, pred_col3 = st.columns(3)
 
with pred_col1:
    input_minutes = st.number_input("Minutes played", min_value=0, max_value=3420, value=1800)
    input_goals = st.number_input("Goals scored", min_value=0, max_value=40, value=5)
    input_assists = st.number_input("Assists", min_value=0, max_value=30, value=5)
 
with pred_col2:
    input_position = st.selectbox("Position", options=all_positions, key="pred_position")
    input_cost = st.number_input("Cost (£m)", min_value=3.5, max_value=15.0, value=6.0, step=0.1)
    input_xg = st.number_input("Expected goals (xG)", min_value=0.0, max_value=40.0, value=4.0, step=0.1)
 
with pred_col3:
    input_xa = st.number_input("Expected assists (xA)", min_value=0.0, max_value=30.0, value=4.0, step=0.1)
    input_ict = st.number_input("ICT index", min_value=0.0, max_value=400.0, value=100.0, step=1.0)
    input_selected = st.number_input("Selected by (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
 
if st.button("Predict total points"):
    input_row = pd.DataFrame([{
        "minutes": input_minutes,
        "goals_scored": input_goals,
        "assists": input_assists,
        "clean_sheets": 0,
        "goals_conceded": 0,
        "own_goals": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "saves": 0,
        "influence": 0,
        "creativity": 0,
        "threat": 0,
        "ict_index": input_ict,
        "selected_by_percent": input_selected,
        "now_cost": input_cost,
        "expected_goals": input_xg,
        "expected_assists": input_xa,
        "goals_per_90": (input_goals / input_minutes * 90) if input_minutes > 0 else 0,
        "assists_per_90": (input_assists / input_minutes * 90) if input_minutes > 0 else 0,
        "minutes_share": input_minutes / 3420,
        "position": input_position,
    }])
 
    input_encoded = pd.get_dummies(input_row, columns=["position"], drop_first=True)
 
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
 
    prediction = trained_model.predict(input_encoded)[0]
    st.success(f"Predicted total points: **{round(prediction, 1)}**")
 
# FOOTER
st.markdown("---")
st.caption(
    "Data source: Fantasy Premier League (vaastav/Fantasy-Premier-League), 2023-24 season. "
    "Built during the Sohail Smart Solutions Summer Training Programme 2026."
)
 