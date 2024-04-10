from django.db import models

# Create your models here.
class Question(models.Model):

   question_id = models.IntegerField(primary_key=True)
   question_text = models.TextField()
   answer_text = models.TextField()

   def __str__(self) -> str:
      return f"{self.question_id}"