# Generated by Django 4.1.13 on 2024-04-14 02:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_nome_campo_entrada_campomatch_inputfield_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campomatch',
            name='tableName',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
