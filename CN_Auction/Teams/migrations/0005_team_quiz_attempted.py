# Generated by Django 5.0.4 on 2024-04-19 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teams', '0004_remove_team_time_taken_team_points_scored_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='quiz_attempted',
            field=models.BooleanField(default=False),
        ),
    ]
