# Generated by Django 5.0.6 on 2024-06-21 13:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0006_alter_comment_author_alter_comment_item_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "verbose_name": "Комменатрий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.AlterModelOptions(
            name="item",
            options={"verbose_name": "Новость", "verbose_name_plural": "Новости"},
        ),
    ]
