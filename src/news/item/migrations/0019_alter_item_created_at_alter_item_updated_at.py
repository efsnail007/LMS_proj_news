# Generated by Django 5.0.6 on 2024-07-05 16:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0018_alter_addition_options_alter_item_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 5, 19, 46, 35, 607917)
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="updated_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 5, 19, 46, 35, 607942)
            ),
        ),
    ]