# Generated by Django 5.0.3 on 2024-05-03 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "DataBase",
            "0012_rename_number_of_generations_generationallearninginstancedatabasemodel_number_of_sucessful_generatio",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="generationinstancedatabasemodel",
            name="all_agents_fitness_results",
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name="generationinstancedatabasemodel",
            name="generation_average_fitness",
            field=models.JSONField(null=True),
        ),
    ]
