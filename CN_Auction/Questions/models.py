from django.db import models

# Create your models here.
class Question(models.Model):

   question_id = models.IntegerField(primary_key=True)
   question_text = models.TextField(blank=True)
   option_1 = models.TextField(blank=True)
   option_2 = models.TextField(blank=True)
   option_3 = models.TextField(blank=True)
   option_4 = models.TextField(blank=True)
   correct_option = models.TextField(default=0)


   def __str__(self) -> str:
      return f"{self.question_id}"