from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Teams.models import Team

# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.core.exceptions import ValidationError

# @receiver(pre_save, sender='Players.Group')
# def check_purse_value(sender, instance, **kwargs):
#     if instance.alloted_team and instance.group_price:
#         group_price = float(instance.group_price)
#         purse_value = float(instance.alloted_team.purse_value)
#         if group_price > purse_value:
#             raise ValidationError("Group price cannot exceed the purse value of the assigned team.")

# Create your models here.

class Group(models.Model):

   group_id = models.IntegerField(primary_key=True)
   group_price = models.FloatField(default=0.0)
   group_points = models.IntegerField(default=0) 
   alloted_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='groups', null=True, blank=True, db_column='team_id')
   
   def __str__(self) -> str:
      return f'Group {self.group_id}'


class Individual(models.Model):

   player_id = models.IntegerField(primary_key=True)
   player_name = models.CharField(max_length=50)
   player_price = models.FloatField(default=0.0)
   group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='players')
   
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
   
   