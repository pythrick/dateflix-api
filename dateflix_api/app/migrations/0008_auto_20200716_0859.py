# Generated by Django 3.0.8 on 2020-07-16 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_auto_20200710_0956"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="description"),
        ),
    ]
