# Generated by Django 5.2 on 2025-05-20 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="voter",
            name="has_voted",
            field=models.BooleanField(default=False),
        ),
    ]
