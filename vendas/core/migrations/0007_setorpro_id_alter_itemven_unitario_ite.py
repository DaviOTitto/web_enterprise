# Generated by Django 4.1 on 2022-10-06 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_setorpro_id_alter_itemven_unitario_ite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemven',
            name='unitario_ite',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=7, verbose_name='Valor unitário'),
        ),
    ]
