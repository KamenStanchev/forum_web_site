# Generated by Django 4.1.2 on 2022-10-14 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_postarticle'),
    ]

    operations = [
        migrations.AddField(
            model_name='postarticle',
            name='topic',
            field=models.CharField(choices=[('sport', 'sport'), ('wok', 'wok'), ('football', 'football'), ('scool', 'scool'), ('cars', 'cars'), ('food', 'food'), ('leisure', 'leisure'), ('celebrity', 'celebrity'), ('fashion', 'fashion'), ('world', 'world'), ('climate', 'climate'), ('travel', 'travel'), ('history', 'history'), ('formula 1', 'formula 1'), ('finance', 'finance'), ('culture', 'culture'), ('theater', 'theater'), ('cinema', 'cinema'), ('shoping', 'shoping'), ("holiday's", "holiday's")], default='NO TOPIC', max_length=30),
        ),
    ]
