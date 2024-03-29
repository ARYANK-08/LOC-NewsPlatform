# Generated by Django 5.0.3 on 2024-03-09 12:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="likes",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="comment",
            name="likes",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="question",
            name="likes",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="reply",
            name="likes",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
