# Generated by Django 3.2 on 2023-05-09 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20230509_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslocation',
            name='ip_public',
            field=models.CharField(blank=True, default='serverlocal', max_length=20, verbose_name='IP'),
        ),
    ]
