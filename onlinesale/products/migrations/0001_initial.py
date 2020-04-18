# Generated by Django 3.0 on 2020-01-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('imdb', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('release_date', models.DateField()),
                ('director', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products')),
                ('price', models.DecimalField(decimal_places=2, default=10, max_digits=10)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('description', models.TextField(null=True)),
                ('active', models.BooleanField(default=True)),
                ('createdDate', models.DateField(auto_now_add=True)),
                ('updatedDate', models.DateField(auto_now=True)),
            ],
        ),
    ]