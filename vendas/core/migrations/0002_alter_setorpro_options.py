# Generated by Django 4.1 on 2022-09-06 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='setorpro',
            options={'ordering': ['num_setor'], 'verbose_name': 'setorpro'},
        ),
    ]
