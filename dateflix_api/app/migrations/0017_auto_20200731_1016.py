# Generated by Django 3.0.8 on 2020-07-31 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0016_user_birthday_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="picture", name="url", field=models.URLField(max_length=300),
        ),
    ]