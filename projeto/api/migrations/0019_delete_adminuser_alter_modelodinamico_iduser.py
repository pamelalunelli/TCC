# Generated by Django 4.1.13 on 2024-04-24 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_adminuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdminUser',
        ),
        migrations.AlterField(
            model_name='modelodinamico',
            name='iduser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
