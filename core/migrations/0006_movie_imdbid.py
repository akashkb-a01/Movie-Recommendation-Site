# Generated by Django 4.0.4 on 2022-05-24 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_movie_imdbid_movie_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdbid',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
