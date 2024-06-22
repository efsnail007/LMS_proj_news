# Generated by Django 4.2.3 on 2024-06-21 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
        ('user_page', '0003_subscriptions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkedRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(choices=[('Like', 'Лайк'), ('Repost', 'Репост'), ('Comment', 'Комментарий')], max_length=50)),
                ('text', models.TextField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_page.profile')),
            ],
        ),
    ]