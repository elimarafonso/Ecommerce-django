# Generated by Django 3.2 on 2023-05-03 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20230502_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='codPostal',
        ),
        migrations.RemoveField(
            model_name='order',
            name='country_name',
        ),
    ]