# Generated by Django 3.2 on 2023-03-13 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_deliveryaddress_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryaddress',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]