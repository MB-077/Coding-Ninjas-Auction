from django.db import models

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
   student_name = models.CharField(max_length=100)
   student_rollno = models.CharField(max_length=10)  # Assuming roll number is a string
   team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='students')

   def __str__(self) -> str:
      return f"{self.student_name} --> {self.team}"