import os
import random
import pandas as pd

from Players.models import Individual, Stat, Group
from CN_Auction.settings import BASE_DIR

CSV_DATA_FILE = os.path.join(BASE_DIR, "Scripts", "processed_csv", "random_IPL_Players.csv")

# UNFINISHED
def execute_process() -> int:
    # Loading the data
    print(f"[ INFO ] Reading {CSV_DATA_FILE} ...")
    IPL_DataFrame = pd.read_csv(CSV_DATA_FILE)

    # Create the groups
    print(f"[ INFO ] Creating Groups: IDs 1 -> 60 ...")
    groups = [Group.objects.create(group_id=i) for i in range(1, 60)]

    # Create the players
    print(f"[ INFO ] Creating Individual (player) instances and Stat instances ...")
    for i in range(len(IPL_DataFrame)):

        assigned_group_id = random.randint(1, 60)
        assigned_group = Group.objects.get(pk=assigned_group_id)

        player_instance = Individual.objects.create(
            player_id=i+1,
            player_name=IPL_DataFrame["PLAYER"][i],
            player_price=IPL_DataFrame["PRICE"][i],
            group=assigned_group
        )

        stat_instance = Stat.objects.create(
            fielding=IPL_DataFrame["FieldingRating"][i],
            bowling=IPL_DataFrame["BowlingRating"][i],
            batting=IPL_DataFrame["BattingRating"][i],
            wicketkeeper=bool(IPL_DataFrame["IsWicketKeeper"][i]),
            player=player_instance
        )

        if len(assigned_group.individual_set.all()) >= 4:
            groups.remove(assigned_group)

    print("[ INFO ] Process finished.")
    return 0