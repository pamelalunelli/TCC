# Generated by Django 3.1.4 on 2023-11-05 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_dadosdinamicos'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadosdinamicos',
            name='modelo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.modelodinamico'),
        ),
    ]
