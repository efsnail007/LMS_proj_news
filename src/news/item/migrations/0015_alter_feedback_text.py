# Generated by Django 5.0.6 on 2024-06-26 21:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0014_alter_feedback_options_feedback_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="text",
            field=models.TextField(null=True),
        ),
    ]