from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Teams.models import Team
import pandas as pd
import random
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
   has_wicketkeeper = models.BooleanField(default=False)
   
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

def enter_data():
   dtype_dict = {
      "PLAYER" : str,
      "ROLE" : str,
      "PRICE" : float,
      "TEAM" : str,
      "IsWicketKeeper" : bool,
      "BowlingRating" : int,
      "BattingRating" : int,
      "FieldingRating" : int
   }
   
   df = pd.read_csv(r'Players\data.csv', dtype=dtype_dict) # Players\data.csv

   non_wk_groups = list(range(1, 60))
   available_groups = list(range(1, 60))

   print("\nEntering Data...\nIt May Take a Few Minutes...")

   for g in range(1, 60):
      Group.objects.create(group_id=g)

   for i in range(len(df)):
      if df.at[i, "IsWicketKeeper"]:
         group = random.choice(non_wk_groups)
         Group.objects.filter(pk=group).update(has_wicketkeeper=True)
         if group in non_wk_groups:
            non_wk_groups.remove(group)
      else :
         group = random.choice(available_groups)

      # Updates Group Points
      player_stats = df.at[i, "BowlingRating"] + df.at[i, "BattingRating"] + df.at[i, "FieldingRating"]
      player_price = df.at[i, "PRICE"]

      groupPoints = Group.objects.get(pk=group).group_points
      groupPrice  = Group.objects.get(pk=group).group_price
      
      Group.objects.filter(pk=group).update(group_points=f'{groupPoints+player_stats}')
      Group.objects.filter(pk=group).update(group_price=f'{groupPrice+player_price}')


      
      Individual.objects.create(player_id=i, player_name=df.at[i, "PLAYER"],
                                 player_price=player_price, group=Group.objects.get(pk=group))
      Stat.objects.create(fielding=df.at[i, "FieldingRating"], bowling=df.at[i, "BowlingRating"],
                           batting=df.at[i, "BattingRating"], wicketkeeper=df.at[i, "IsWicketKeeper"],
                           player=Individual.objects.get(pk=i))

      if Individual.objects.filter(group_id=f'{group}').count() >= 4:
         if group in available_groups:
            available_groups.remove(group)
         if group in non_wk_groups:
            non_wk_groups.remove(group)
      
   print("\nDone...\nData Has Been Entered :)")
      # --------------------------------------------------------------------------

def check():
   wks = Stat.objects.filter(wicketkeeper='True')
   groups = {22: 0, 20: 0, 15: 0, 1: 0, 55: 0, 40: 0, 9: 0, 27: 0, 5: 0, 10: 0, 38: 0, 17: 0, 7: 0, 11: 0} # {0: 0, 6: 0, 10: 0, 11: 0, 14: 0, 18: 0, 21: 0, 32: 0, 36: 0, 44: 0, 46: 0, 1: 0, 22: 0}
   for wk in wks:
      # groups[wk.player.group.group_id] = 0
      groups[wk.player.group.group_id] += 1
   print(groups)