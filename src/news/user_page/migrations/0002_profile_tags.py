# Generated by Django 4.2.3 on 2024-06-16 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
        ('user_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tags',
            field=models.ManyToManyField(to='item.tags'),
        ),
    ]