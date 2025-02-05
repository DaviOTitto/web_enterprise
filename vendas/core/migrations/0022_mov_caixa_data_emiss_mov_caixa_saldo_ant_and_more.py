# Generated by Django 4.1 on 2022-12-14 11:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_setorpro_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='mov_caixa',
            name='data_emiss',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='data de emissao'),
        ),
        migrations.AddField(
            model_name='mov_caixa',
            name='saldo_ant',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='saldo anterior'),
        ),
        migrations.AddField(
            model_name='mov_caixa',
            name='valor_baixa',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='valor da baixa '),
        ),
    ]
