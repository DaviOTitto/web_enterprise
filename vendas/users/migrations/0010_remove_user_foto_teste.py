# Generated by Django 4.1 on 2022-12-02 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_foto_teste'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='foto_teste',
        ),
    ]
