# Generated by Django 4.2.1 on 2023-05-18 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_eventtask_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtask',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
    ]