# Generated by Django 4.1 on 2022-08-17 12:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_historico_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
