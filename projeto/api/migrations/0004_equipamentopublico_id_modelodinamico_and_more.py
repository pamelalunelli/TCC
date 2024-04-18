# Generated by Django 4.1.13 on 2024-03-09 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_proprietario_data_nasc_alter_rrr_data_inicio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipamentopublico',
            name='id_modeloDinamico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.modelodinamico'),
        ),
        migrations.AddField(
            model_name='geometria',
            name='id_modeloDinamico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.modelodinamico'),
        ),
        migrations.AddField(
            model_name='proprietario',
            name='id_modeloDinamico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.modelodinamico'),
        ),
        migrations.DeleteModel(
            name='Imovel',
        ),
        migrations.DeleteModel(
            name='RRR',
        ),
    ]