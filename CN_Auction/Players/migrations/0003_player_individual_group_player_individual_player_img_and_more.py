# Generated by Django 5.0.4 on 2024-04-10 17:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0002_rename_player_groups_player_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='player_individual',
            name='group',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='player', to='Players.player_group'),
        ),
        migrations.AddField(
            model_name='player_individual',
            name='player_img',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.CreateModel(
            name='Player_Stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fielding', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('bowling', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('batting', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='Players.player_individual')),
            ],
        ),
    ]