from django.db import models
import pandas as pd

# Create your models here.
class Team(models.Model):
   team_id = models.IntegerField(primary_key=True)
   team_name = models.CharField(max_length=40, null=False)
   correct_answers = models.IntegerField(default=0)  # Incremental Logic in VIEWS [To be Implemented]
   purse_value = models.FloatField(default=40)  # Calculation Logic in VIEWS [To be Implemented]
   points_scored = models.IntegerField(default=0)  

   def __str__(self):
      return self.team_name


class Student(models.Model):
    student_name = models.CharField(max_length=100, null=True)
    student_rollno = models.CharField(max_length=10, null=True)  # Assuming roll number is a string
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"Name: {self.student_name} | Roll No: {self.student_rollno} | Team: {self.team.team_name}"
   

def process_team_data():
   dtype_dict = {
      "TEAM_ID": int,
      "TEAM_NAME": str,
      "CORRECT_ANSWERS": int,
      "PURSE_VALUE": int,
      "NUMBER_OF_MEMBERS": int,
      "TEAM_MEMBERS": str,
      "TEAM_MEMBERS_ROLL_NUMBERS": str,
   }

   # Load the data
   df = pd.read_csv(r'Teams/Team_Data.csv', dtype=dtype_dict)  # Update path to your CSV

   print("\nProcessing Team Data...\n")

   for g in df['TEAM_ID'].unique():
      Team.objects.create(team_id=g)
      
   # Process the data
   for i in range(len(df)):
      # Extract player information from the DataFrame
      team_id = df.at[i, "TEAM_ID"]
      team_name = df.at[i, "TEAM_NAME"]
      correct_answers = df.at[i, "CORRECT_ANSWERS"]
      purse_value = df.at[i, "PURSE_VALUE"]
      
      # Update Team attributes
      team = Team.objects.get(team_id=team_id)
      team.team_name = team_name
      team.correct_answers = correct_answers
      team.purse_value = purse_value
      team.save()
         
      # Update Students and Individuals related to the Team
      member_names = [name.strip() for name in df['TEAM_MEMBERS'][i].split(",")]
      member_rollnos = [rollno.strip() for rollno in df['TEAM_MEMBERS_ROLL_NUMBERS'][i].split(",")]

      for j in range(len(member_names)):
          # Check if the student with the given roll number already exists for this team
         student, created = Student.objects.get_or_create(student_rollno=member_rollnos[j], team=team)
         # Update or set the student's name
         student.student_name = member_names[j]
         student.save()

      print(f"[  OK  ] Updated data for team: {df['TEAM_NAME'][i]} ...")

   print("\nData Processing Completed Successfully!")
