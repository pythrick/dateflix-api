# Generated by Django 3.0.8 on 2020-07-21 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_auto_20200721_0910"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="netflix_id",
            field=models.IntegerField(verbose_name="Netflix ID"),
            preserve_default=False,
        ),
    ]
