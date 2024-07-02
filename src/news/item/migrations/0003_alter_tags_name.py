# Generated by Django 5.0.6 on 2024-06-21 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0002_alter_tags_name"),
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
                    ("Other", "Другое"),
                ],
                default="Другое",
                max_length=100,
            ),
        ),
    ]