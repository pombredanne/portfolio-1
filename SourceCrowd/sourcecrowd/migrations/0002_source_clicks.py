# Generated by Django 3.2.8 on 2022-03-16 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sourcecrowd', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
    ]
