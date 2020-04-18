# Generated by Django 3.0 on 2020-01-24 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0004_auto_20200119_0035'),
        ('products', '0002_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='actors',
            field=models.ManyToManyField(blank=True, to='actors.Actor'),
        ),
        migrations.AddField(
            model_name='product',
            name='trailer_link',
            field=models.URLField(default='fjdnjvgnfjvn', max_length=700),
            preserve_default=False,
        ),
    ]