import pandas as pd
import os
import warnings
# from Players.models import Individual

warnings.filterwarnings("ignore")

# One time operations
def calculate_bowling_rating(row) -> float:
    try:
        W = float(row['Wkts'])
        E = 1 / float(row['Econ'])
        S = 1 / float(row['SR'])
        P = float(row['4w']) + float(row['5w'])
    except ValueError:
        return 0

    W = row['Wkts']
    E = 1 / row['Econ']
    S = 1 / row['SR']
    P = row['4w'] + row['5w']
    
    # Define weights for each factor
    W_weight = 0.4
    E_weight = 0.3
    S_weight = 0.2
    P_weight = 0.1
    
    # Calculate overall rating
    rating = ((W * W_weight + E * E_weight + S * S_weight + P * P_weight) /
              (W_weight + E_weight + S_weight + P_weight)) * 10
    
    # Ensure rating is between 1 and 10
    return max(1, min(rating, 10))

def calculate_batting_rating(row) -> float:
    try:
        R = float(row['Runs'])
        A = float(row['Avg'])
        S = float(row['SR'])
        C = float(row['100']) + float(row['50'])  # Combining centuries and half-centuries
        B = float(row['4s']) + float(row['6s'])    # Combining fours and sixes
        N = float(row['NO'])               # Number of times not out
    except ValueError:
        return 0 

    # R = row['Runs']
    # A = row['Avg']
    # S = row['SR']
    # C = row['100'] + row['50']  # Combining centuries and half-centuries
    # B = row['4s'] + row['6s']    # Combining fours and sixes
    # N = row['NO']               # Number of times not out
    
    # Define weights for each factor
    R_weight = 0.2
    A_weight = 0.15
    S_weight = 0.15
    C_weight = 0.2
    B_weight = 0.2
    N_weight = 0.1

    # print("[ DEBUG ] Params:",R,A,S,C,B,N)
    
    # Calculate overall rating
    rating = ((R * R_weight + A * A_weight + S * S_weight + C * C_weight + B * B_weight + N * N_weight) /
              (R_weight + A_weight + S_weight + C_weight + B_weight + N_weight))
    
    # Ensure rating is between 1 and 10
    # return max(1, min(rating, 10))
    print("[DEBUG] Rating Bat:", rating)
    return max(min(rating, 10), 1)

def process_ipl_players_csv() -> None:
    IPL_DataFrame = pd.read_csv(os.path.join("csv", "IPL_Players.csv"))
    IPL_DataFrame["IsWicketKeeper"] = None
    IPL_DataFrame["BowlingRating"] = None
    IPL_DataFrame["BattingRating"] = None

    Batting_df = pd.read_csv(os.path.join("csv","BATTING STATS - IPL_2022.csv"))
    Batting_df = Batting_df.replace('-', '0', regex=True)
    Batting_df = Batting_df.replace('\*', '', regex=True)
    Batting_df = Batting_df.dropna()
    Batting_df["Rating"] = Batting_df.apply(calculate_batting_rating, axis=1)

    Bowling_df = pd.read_csv(os.path.join("csv","BOWLING STATS - IPL_2022.csv"))
    Bowling_df = Bowling_df.replace('-', '0', regex=True)
    Bowling_df = Bowling_df.replace('\*', '', regex=True)
    Bowling_df = Bowling_df.dropna()
    Bowling_df["Rating"] = Bowling_df.apply(calculate_bowling_rating, axis=1)

    # print(Batting_df["Rating"].values)
    # return None
    # print(Bowling_df)

    for i in range(len(Batting_df)):
        Batting_df["Player"][i] = Batting_df["Player"][i].upper()

    for i in range(len(Bowling_df)):
        Bowling_df["Player"][i] = Bowling_df["Player"][i].upper()

    for i in range(len(IPL_DataFrame)):

        IPL_DataFrame["PLAYER"][i] = IPL_DataFrame["PLAYER"][i].upper()


        # Whether player exists in Batting_df
        batting_row = Batting_df.loc[Batting_df["Player"] == IPL_DataFrame["PLAYER"][i]]
        if not batting_row.empty:
            # print(batting_row)
            IPL_DataFrame["BattingRating"][i] = batting_row['Rating'].values
            # print(batting_row['Rating'])
        else:
            IPL_DataFrame["BattingRating"][i] = 0

        # Whether player exists in Bowling_df
        bowling_row = Bowling_df.loc[Bowling_df["Player"] == IPL_DataFrame["PLAYER"][i]]
        if not bowling_row.empty:
            IPL_DataFrame["BowlingRating"][i] = bowling_row['Rating'].values
        else:
            IPL_DataFrame["BowlingRating"][i] = 0

        if IPL_DataFrame["ROLE"][i] == "Wicket-keeper":
            IPL_DataFrame["IsWicketKeeper"][i] = 1
        else:
            IPL_DataFrame["IsWicketKeeper"][i] = 0

        if "crore" in IPL_DataFrame["PRICE"][i]:
            IPL_DataFrame["PRICE"][i] = float(IPL_DataFrame["PRICE"][i].split(" ")[0])
            continue

        if "lakh" in IPL_DataFrame["PRICE"][i]:
            IPL_DataFrame["PRICE"][i] = float(IPL_DataFrame["PRICE"][i].split(" ")[0])*0.01
            continue
    
    IPL_DataFrame.to_csv(os.path.join("processed_csv", "withBatBowlv2_IPL_Players.csv"), index=False)
    print(IPL_DataFrame)

if __name__ == "__main__":
    process_ipl_players_csv()
