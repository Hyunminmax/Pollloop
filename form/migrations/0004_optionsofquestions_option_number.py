# Generated by Django 5.1.4 on 2024-12-31 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("form", "0003_respondent_is_complete"),
    ]

    operations = [
        migrations.AddField(
            model_name="optionsofquestions",
            name="option_number",
            field=models.CharField(default=0, max_length=2),
        ),
    ]