# Generated by Django 5.0.3 on 2024-03-15 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBase', '0005_rename_agentinstance_agentinstancedatabasemodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generationinstancedatabasemodel',
            name='number_of_agents',
            field=models.IntegerField(),
        ),
    ]
