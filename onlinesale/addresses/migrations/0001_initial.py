# Generated by Django 3.0 on 2020-01-18 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_to_name', models.CharField(max_length=120)),
                ('address_line_1', models.CharField(max_length=120)),
                ('address_line_2', models.CharField(blank=True, default='-', max_length=120, null=True)),
                ('city', models.CharField(max_length=120)),
                ('country', models.CharField(default='India', max_length=120)),
                ('state', models.CharField(max_length=120)),
                ('pin_code', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
