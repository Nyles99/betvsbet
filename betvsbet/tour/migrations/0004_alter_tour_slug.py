# Generated by Django 4.2.1 on 2024-12-04 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0003_alter_tour_options_tour_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
