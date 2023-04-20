# Generated by Django 3.2 on 2023-04-20 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_orderproduct_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'Novo'), ('Accepted', 'Aceito'), ('Completed', 'Concluído'), ('Cancelled', 'Cancelado')], default='New', max_length=10, verbose_name='Status'),
        ),
    ]
