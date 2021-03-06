# Generated by Django 4.0.4 on 2022-05-27 13:22

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_movie_imdb_id_alter_movie_vote_average'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Adult', 'Adult'), ('Animation', 'Animation'), ('Biography', 'Biography'), ('Comedy', 'Comedy'), ('Crime', 'Crime'), ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'), ('Fantasy', 'Fantasy'), ('History', 'History'), ('Horror', 'Horror'), ('Music', 'Music'), ('Musical', 'Musical'), ('Mystery', 'Mystery'), ('Romance', 'Romance'), ('Science Fiction', 'Sci-Fi'), ('Short', 'Short'), ('Sport', 'Sport'), ('Thriller', 'Thriller'), ('War', 'War'), ('Western', 'Western')], max_length=182),
        ),
        migrations.AlterField(
            model_name='profile',
            name='age_limit',
            field=models.CharField(choices=[('All', 'True'), ('Kids', 'False')], max_length=5),
        ),
    ]
