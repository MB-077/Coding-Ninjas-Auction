# Generated by Django 5.0.4 on 2024-04-17 03:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0013_alter_group_alloted_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='Players.group'),
        ),
    ]
