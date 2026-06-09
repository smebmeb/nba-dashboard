import os
import pandas as pd
from nba_api.stats.endpoints import playergamelog

# =====================
# SETUP
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# =====================
# PLAYERS
# =====================
players = {
    # Knicks
    "Jalen Brunson": 1628973,
    "Karl-Anthony Towns": 1626157,
    "Mikal Bridges": 1628969,
    "OG Anunoby": 1628384,
    "Josh Hart": 1628404,
    "Julius Randle": 203944,
    "Donte DiVincenzo": 1628978,
    "Mitchell Robinson": 1629011,
    "Miles McBride": 1630540,

    # Spurs
    "Victor Wembanyama": 1641705,
    "De'Aaron Fox": 1628368,
    "Stephon Castle": 1631114,
    "Devin Vassell": 1630170,
    "Keldon Johnson": 1629640,
    "Jeremy Sochan": 1631110,
    "Julian Champagnie": 1630577,
    "Harrison Barnes": 203084
}

# =====================
# COLLECT PLAYOFF DATA
# =====================
all_data = []

for player_name, player_id in players.items():

    print(f"Loading {player_name}...")

    try:

        gamelog = playergamelog.PlayerGameLog(
            player_id=player_id,
            season="2025-26",
            season_type_all_star="Playoffs"
        )

        df = gamelog.get_data_frames()[0]

        if len(df) == 0:
            print(f"No playoff data found for {player_name}")
            continue

        df["PLAYER_NAME"] = player_name

        keep_cols = [
            "PLAYER_NAME",
            "GAME_DATE",
            "MATCHUP",
            "WL",
            "PTS",
            "AST",
            "REB",
            "BLK",
            "STL",
            "FG3M",
            "FGM",
            "MIN"
        ]

        df = df[keep_cols]

        all_data.append(df)

    except Exception as e:
        print(f"Error loading {player_name}: {e}")

# =====================
# COMBINE
# =====================
final_df = pd.concat(all_data, ignore_index=True)

final_df["GAME_DATE"] = pd.to_datetime(final_df["GAME_DATE"])

final_df = final_df.sort_values(
    ["GAME_DATE", "PLAYER_NAME"],
    ascending=[False, True]
)

# =====================
# SAVE
# =====================
output_file = os.path.join(
    DATA_DIR,
    "knicks_spurs_playoffs_2025_26.csv"
)

final_df.to_csv(output_file, index=False)

print("\nDONE")
print("Rows:", len(final_df))
print("Latest Game:", final_df["GAME_DATE"].max())
print("Saved:", output_file)