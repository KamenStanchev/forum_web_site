# Generated by Django 4.1.2 on 2022-10-14 15:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_articlecomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='data_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='articlecomment',
            name='content',
            field=models.TextField(max_length=300),
        ),
    ]