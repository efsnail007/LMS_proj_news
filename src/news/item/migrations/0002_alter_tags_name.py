# Generated by Django 5.0.6 on 2024-06-21 08:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tags",
            name="name",
            field=models.CharField(
                choices=[
                    ("Music", "Музыка"),
                    ("Cinema", "Кино"),
                    ("Sport", "Спорт"),
                    ("Politics", "Политика"),
                    ("Art", "Искусство"),
                    ("Cooking", "Кулинария"),
                    ("Pets", "Питомцы"),
                    ("Health", "Здоровье"),
                    ("Education", "Образование"),
                ],
                max_length=100,
            ),
        ),
    ]
