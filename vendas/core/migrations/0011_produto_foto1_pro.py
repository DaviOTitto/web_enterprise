# Generated by Django 4.1 on 2022-10-11 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_setorpro_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='foto1_pro',
            field=models.ImageField(blank=True, default='produtos/foto.', null=True, upload_to='produtos/', verbose_name='Foto'),
        ),
    ]
