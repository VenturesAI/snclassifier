# Generated by Django 4.2.6 on 2023-10-30 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snclassifier_djangoapp', '0003_youtubecoment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubecoment',
            name='date',
            field=models.DateTimeField(verbose_name='date logged'),
        ),
    ]