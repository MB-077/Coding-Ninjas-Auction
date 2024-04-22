import os
import pandas as pd

from Teams.models import Team, Student
from CN_Auction.settings import BASE_DIR

def process_team_data():
    # Load the data
    # adjust path accordingly
    Teams_DataFrame = pd.read_csv(os.path.join(BASE_DIR, "Scripts", "csv", "TestTeamData.csv"))
    team_ids = []

    # Create the teams:
    print("[ INFO ] Creating Teams ...")
    for i in range(len(Teams_DataFrame)):
        team = Team.objects.create(
            team_id=i,
            team_name=Teams_DataFrame["Team Name"][i]
        )

        # print(f'[ DEBUG ] Created: {Teams_DataFrame["Team Name"][i]} | Team ID: {team.team_id}')
        team_ids.append(team.team_id)

    print("[ INFO ] Adding members to the teams ...")
    for i in range(len(Teams_DataFrame)):
    
        # Process the the members of the team
        member_names = [name.strip() for name in Teams_DataFrame["Team Members Name  (separate By using Comas)"][i].split(",")]
        member_rollno = [rollno for rollno in Teams_DataFrame["Team Members Roll Numbers   (separate By using Comas)"][i].split(",")]

        if len(member_names) != len(member_rollno):
            print(f"[ FAIL ] Data inconsistent for TEAM: {Teams_DataFrame['Team Name'][i]}. Unable to add members for this team ...")
            continue
        
        # Get the team
        # print(f"[ DEBUG ] Team ID: {team_ids[i]}")
        team = Team.objects.filter(team_id=team_ids[i]).first()
        # print(f"[ DEBUG ] Team Object: {team}")

        # Creating Student for person who submitted the form
        student_form_submit = Student.objects.create(
            student_name=Teams_DataFrame["Name"][i],
            student_rollno=Teams_DataFrame["Roll Number"][i],
            team=team
        )

        # student_form_submit.team = team

        form_submitter_name = Teams_DataFrame["Name"][i].lower().replace(" ", "")

        for j in range(len(member_names)):
            # Check if form submitter name is mentioned again and skip it if it is
            if member_names[j].lower().replace(" ", "") == form_submitter_name:
                continue

            student_member = Student.objects.create(
                student_name=member_names[j],
                student_rollno=member_rollno[j],
                team=team
            )

        
        print(f"[  OK  ] Added members for team: {Teams_DataFrame['Team Name'][i]} ...")

if __name__ == "__main__":
    process_team_data()