# Generated by Django 3.0.8 on 2020-07-21 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013_movie_tmdb_score"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie", name="active", field=models.BooleanField(default=True),
        ),
    ]
