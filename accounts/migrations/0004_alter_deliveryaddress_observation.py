# Generated by Django 3.2 on 2023-03-08 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_deliveryaddress_observation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryaddress',
            name='observation',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]