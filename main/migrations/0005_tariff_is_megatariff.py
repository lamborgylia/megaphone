# Generated by Django 5.2 on 2025-04-21 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_tariff_tv_channels'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='is_megatariff',
            field=models.BooleanField(default=False, verbose_name='МегаТариф'),
        ),
    ]
