# Generated by Django 4.1.13 on 2024-05-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_modelodinamico_isconcluded'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldmatching',
            name='matchingTableName',
            field=models.CharField(max_length=255, null=True),
        ),
    ]