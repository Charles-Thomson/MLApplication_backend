# Generated by Django 5.0.3 on 2024-05-07 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "DataBase",
            "0017_remove_instancealphabraindatabasemodel_instance_relation_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="alphabraininstancedatabasemodel",
            name="instance_relation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="instance_relation",
                to="DataBase.generationallearninginstancedatabasemodel",
            ),
        ),
    ]
