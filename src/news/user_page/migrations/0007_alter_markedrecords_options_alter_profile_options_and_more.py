# Generated by Django 5.0.6 on 2024-07-08 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user_page", "0006_remove_subscriptions_subscription_profiles_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="markedrecords",
            options={
                "verbose_name": "Отмеченные записи",
                "verbose_name_plural": "Отмеченные записи",
            },
        ),
        migrations.AlterModelOptions(
            name="profile",
            options={"verbose_name": "Профиль", "verbose_name_plural": "Профили"},
        ),
        migrations.AlterModelOptions(
            name="subscriptions",
            options={"verbose_name": "Подписки", "verbose_name_plural": "Подписки"},
        ),
    ]
