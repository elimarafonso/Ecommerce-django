# Generated by Django 3.2 on 2023-02-08 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20230208_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='docCNPJ',
            field=models.IntegerField(unique=True, verbose_name='CNPJ'),
        ),
    ]
