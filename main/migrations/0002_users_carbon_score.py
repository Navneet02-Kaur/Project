# Generated by Django 5.1.6 on 2025-03-09 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='carbon_score',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
