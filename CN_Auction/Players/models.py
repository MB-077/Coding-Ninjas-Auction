from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Group(models.Model):

   group_id = models.IntegerField(primary_key=True)
   group_price = models.FloatField(default=0.0)
   alloted_team_group = models.IntegerField(default=-1)

   def __str__(self) -> str:
      return f'Group {self.group_id}'


class Individual(models.Model):

   player_id = models.IntegerField(primary_key=True)
   player_name = models.CharField(max_length=50)
   player_price = models.FloatField(default=0.0)
   group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='player', default=-1)

   def __str__(self) -> str:
      return f'{self.group} : {self.player_name}'


class Stat(models.Model):

   fielding = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
   bowling = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
   batting = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
   wicketkeeper = models.BooleanField(default=False)
   player = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name='stats')

   def __str__(self) -> str:
      return f'{self.player}'