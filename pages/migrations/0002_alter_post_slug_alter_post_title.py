# Generated by Django 4.2.3 on 2023-07-11 13:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.CharField(blank=True, max_length=70),
        ),
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(max_length=55),
        ),
    ]
