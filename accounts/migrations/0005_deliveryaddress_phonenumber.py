# Generated by Django 3.2 on 2023-03-10 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_deliveryaddress_observation'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryaddress',
            name='phoneNumber',
            field=models.CharField(default=3, max_length=15),
            preserve_default=False,
        ),
    ]
