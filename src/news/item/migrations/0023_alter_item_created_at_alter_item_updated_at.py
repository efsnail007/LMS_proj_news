# Generated by Django 5.0.6 on 2024-07-06 07:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0022_alter_item_created_at_alter_item_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 6, 10, 47, 24, 166751)
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="updated_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 6, 10, 47, 24, 166788)
            ),
        ),
    ]