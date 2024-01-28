# Generated by Django 5.0.1 on 2024-01-25 19:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="hashed_password",
            field=models.CharField(default=django.utils.timezone.now, max_length=60),
            preserve_default=False,
        ),
    ]
