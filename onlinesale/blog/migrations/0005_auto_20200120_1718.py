# Generated by Django 3.0 on 2020-01-20 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200120_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='height_field',
            field=models.IntegerField(default=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='width_field',
            field=models.IntegerField(default=300),
        ),
    ]