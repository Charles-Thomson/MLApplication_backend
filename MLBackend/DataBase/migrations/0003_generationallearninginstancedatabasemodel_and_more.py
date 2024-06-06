# Generated by Django 5.0.3 on 2024-03-15 02:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBase', '0002_generationallearninginstance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenerationalLearningInstanceDataBaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_id', models.CharField(max_length=20)),
                ('number_of_generations', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='generationallearninginstanceenvironment',
            name='relation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='instance_environment', to='DataBase.generationallearninginstancedatabasemodel'),
        ),
        migrations.AlterField(
            model_name='generationinstance',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generation_instance', to='DataBase.generationallearninginstancedatabasemodel'),
        ),
        migrations.AlterField(
            model_name='instancealpha',
            name='relation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='instance_alpha', to='DataBase.generationallearninginstancedatabasemodel'),
        ),
        migrations.DeleteModel(
            name='GenerationalLearningInstance',
        ),
    ]
