# Generated by Django 4.2.3 on 2023-07-11 11:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="choices", to="common.quiz"
            ),
        ),
        migrations.AlterField(
            model_name="choice",
            name="votes",
            field=models.IntegerField(default=0),
        ),
    ]
