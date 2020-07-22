# Generated by Django 3.0.8 on 2020-07-21 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_movie_netflix_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie", old_name="url", new_name="netflix_url",
        ),
        migrations.RemoveField(model_name="movie", name="netflix_id",),
        migrations.AddField(
            model_name="movie",
            name="imdb_score",
            field=models.DecimalField(
                decimal_places=1, max_digits=3, verbose_name="IMDB Score"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="movie",
            name="justwatch_id",
            field=models.IntegerField(verbose_name="JustWatch ID"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="movie",
            name="tmdb_id",
            field=models.IntegerField(verbose_name="TMDB ID"),
            preserve_default=False,
        ),
    ]
