# Generated by Django 3.0 on 2020-01-20 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='', width_field='width_field'),
        ),
        migrations.AddField(
            model_name='post',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
    ]
