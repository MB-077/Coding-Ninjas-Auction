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
   player_role = models.CharField(max_length=50, default='Player')
   player_team = models.CharField(max_length=50, default='None')
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
      "PLAYER": str,
      "ROLE": str,
      "PRICE": float,
      "TEAM": str,
      "IsWicketKeeper": bool,
      "BowlingRating": int,
      "BattingRating": int,
      "FieldingRating": int,
      "GROUP_ID": int,
      "PLAYER_ID": int  # Add PLAYER_ID column to your CSV
   }
   
   df = pd.read_csv(r'Players\data.csv', dtype=dtype_dict)  # Load CSV

   print("\nEntering Data...\nIt May Take a Few Minutes...")

   # Create groups
   for g in df['GROUP_ID'].unique():
      Group.objects.create(group_id=g)

   for i in range(len(df)):
      # Extract player information from the DataFrame
      player_id = df.at[i, "PLAYER_ID"]
      player_name = df.at[i, "PLAYER"]
      player_price = df.at[i, "PRICE"]
      group_id = df.at[i, "GROUP_ID"]

      # Update Group Points and Price
      player_stats = df.at[i, "BowlingRating"] + df.at[i, "BattingRating"] + df.at[i, "FieldingRating"]
      group = Group.objects.get(group_id=group_id)
      group.group_points += player_stats
      group.group_price += player_price
      group.save()

      # Create Individual and Stat instances
      individual = Individual.objects.create(
         player_id=player_id,  # Assigning the provided player_id
         player_name=player_name,
         player_price=player_price,
         player_role=df.at[i, "ROLE"],
         player_team=df.at[i, "TEAM"],
         group=group
      )
      Stat.objects.create(
         fielding=df.at[i, "FieldingRating"],
         bowling=df.at[i, "BowlingRating"],
         batting=df.at[i, "BattingRating"],
         wicketkeeper=df.at[i, "IsWicketKeeper"],
         player=individual
      )

   print("\nDone...\nData Has Been Entered :)")