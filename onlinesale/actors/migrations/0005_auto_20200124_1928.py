# Generated by Django 3.0 on 2020-01-24 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0004_auto_20200119_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='deathDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
