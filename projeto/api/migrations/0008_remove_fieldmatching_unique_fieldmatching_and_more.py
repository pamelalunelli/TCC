# Generated by Django 4.1.13 on 2024-06-14 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_customuser_user_permissions_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='fieldmatching',
            name='unique_fieldmatching',
        ),
        migrations.AlterUniqueTogether(
            name='modelodinamico',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='fieldmatching',
            name='fk_modeloDinamico_id',
        ),
        migrations.RemoveField(
            model_name='fieldmatching',
            name='fk_modeloDinamico_iduser',
        ),
        migrations.AddField(
            model_name='fieldmatching',
            name='fk_modeloDinamico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.modelodinamico'),
            preserve_default=False,
        ),
    ]