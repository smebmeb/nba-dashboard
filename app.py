import streamlit as st
import pandas as pd
import plotly.express as px
# import os

# =========================
# LOAD DATA
# =========================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_PATH = os.path.join(BASE_DIR, "data", "knicks_spurs_playoffs_2025_26.csv")

import os

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "knicks_spurs_playoffs_2025_26.csv")

df = pd.read_csv(DATA_PATH)

df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
df = df.sort_values("GAME_DATE", ascending=False)

# =========================
# TITLE
# =========================
st.title("🏀 NBA Playoff Analytics Dashboard (Knicks vs Spurs)")

# =========================
# SIDEBAR FILTER
# =========================
players = df["PLAYER_NAME"].unique()
selected_player = st.sidebar.selectbox("Select Player", players)

player_df = df[df["PLAYER_NAME"] == selected_player]
last20 = player_df.sort_values("GAME_DATE", ascending=False).head(20)
# =========================
# METRICS (SAFE VERSION)
# =========================
st.subheader(f"📊 {selected_player} Playoff Performance")

if len(player_df) == 0:
    st.warning("No data available for this player")
    st.stop()

col1, col2, col3 = st.columns(3)

col1.metric("PPG", round(player_df["PTS"].mean(), 2))
col2.metric("RPG", round(player_df["REB"].mean(), 2))
col3.metric("APG", round(player_df["AST"].mean(), 2))

# =========================
# PRA + STOCKS (BETTING METRICS)
# =========================
player_df["PRA"] = player_df["PTS"] + player_df["REB"] + player_df["AST"]
player_df["STOCKS"] = player_df["STL"] + player_df["BLK"]

col4, col5 = st.columns(2)

col4.metric("PRA Avg", round(player_df["PRA"].mean(), 2))
col5.metric("Stocks Avg", round(player_df["STOCKS"].mean(), 2))

# =========================
# POINTS TREND
# =========================
st.subheader("📈 Points Trend")

fig = px.line(
    player_df.sort_values("GAME_DATE"),
    x="GAME_DATE",
    y="PTS",
    markers=True,
    title="Points per Game"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# LAST 5 GAMES
# =========================
st.subheader("🔥 Last 20 Games")

last5 = player_df.sort_values("GAME_DATE").tail(20)

st.dataframe(
    last5[[
        "GAME_DATE",
        "MATCHUP",
        "PTS",
        "REB",
        "AST",
        "STL",
        "BLK",
        "FG3M",
        "FGM"
    ]]
)

# =========================
# BETTING INSIGHT (SIMPLE)
# =========================
st.subheader("🎯 Simple Betting Insight")

avg_pts = player_df["PTS"].mean()

st.write(f"Average Points: **{round(avg_pts, 2)}**")

if avg_pts > 17:
    st.success("🔥 High scoring playoff performer (overs candidate)")
else:
    st.warning("⚠️ Lower scoring profile (unders candidate)")
