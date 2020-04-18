# Generated by Django 3.0 on 2020-01-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='actors/actresses')),
                ('bio', models.CharField(default=False, max_length=10000)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('birthDate', models.DateField()),
                ('deathDate', models.DateField(null=True)),
            ],
        ),
    ]
