# Generated by Django 4.0.4 on 2022-05-24 18:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_movie_imdbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='date_released',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
