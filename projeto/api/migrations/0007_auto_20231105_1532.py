# Generated by Django 3.1.4 on 2023-11-05 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_dynamictable_dynamictabledata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dynamictabledata',
            name='table',
        ),
        migrations.DeleteModel(
            name='DynamicTable',
        ),
        migrations.DeleteModel(
            name='DynamicTableData',
        ),
    ]