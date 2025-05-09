# Generated by Django 5.2 on 2025-04-23 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_region_options_alter_town_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariff',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tariffs', to='main.region', verbose_name='Регион'),
        ),
        migrations.AlterField(
            model_name='tariff',
            name='town',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tariffs', to='main.town', verbose_name='Город'),
        ),
    ]
