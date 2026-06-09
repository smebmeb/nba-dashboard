import os
import pandas as pd
from nba_api.stats.endpoints import leaguegamelog

# -----------------------------
# SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# FETCH LEAGUE GAMES (SOURCE OF TRUTH)
# -----------------------------
print("Loading league games...")

league_df = leaguegamelog.LeagueGameLog(
    season="2025-26"
).get_data_frames()[0]

# -----------------------------
# CLEAN DATA
# -----------------------------
league_df["GAME_DATE"] = pd.to_datetime(league_df["GAME_DATE"])

league_df = league_df.sort_values("GAME_DATE", ascending=False)

# Keep only useful columns
league_df = league_df[[
    "GAME_DATE",
    "TEAM_NAME",
    "MATCHUP",
    "WL",
    "PTS",
    "FG_PCT",
    "FT_PCT",
    "FG3_PCT"
]]

# -----------------------------
# SAVE DATA
# -----------------------------
file_path = os.path.join(DATA_DIR, "league_games_2025_26.csv")
league_df.to_csv(file_path, index=False)

print("DONE ✅")
print("Saved to:", file_path)
print("Latest game date:", league_df["GAME_DATE"].max())
print("Rows:", len(league_df))