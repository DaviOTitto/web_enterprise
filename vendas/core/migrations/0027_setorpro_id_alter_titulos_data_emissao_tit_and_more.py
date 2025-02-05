# Generated by Django 4.1 on 2023-01-24 12:22

from django.db import migrations, models
import django.utils.timezone
import io


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_alter_titulos_options_setorpro_id_titulos_issqn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titulos',
            name='data_emissao_tit',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='data de emissao'),
        ),
        migrations.AlterField(
            model_name='titulos',
            name='data_venc_tit',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='data de vencimento'),
        ),
        migrations.AlterField(
            model_name='titulos',
            name='oper_inclu',
            field=models.IntegerField(null=True, verbose_name='codigo de inclusao'),
        ),
    ]
