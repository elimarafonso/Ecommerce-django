# Generated by Django 3.2 on 2023-05-09 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_accesslocation_ip_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslocation',
            name='ip_public',
            field=models.CharField(blank=True, max_length=20, verbose_name='IP'),
        ),
    ]