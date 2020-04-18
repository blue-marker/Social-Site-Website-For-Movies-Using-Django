# Generated by Django 3.0 on 2020-01-25 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200122_1108'),
        ('products', '0005_auto_20200125_1142'),
        ('profiles', '0002_profile_about_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='blogs',
            field=models.ManyToManyField(blank=True, to='blog.Post'),
        ),
        migrations.CreateModel(
            name='ProfileRatings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_ratings', to='products.Product')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_ratings', to='profiles.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='product',
            field=models.ManyToManyField(blank=True, through='profiles.ProfileRatings', to='products.Product'),
        ),
    ]