# Generated by Django 4.1.13 on 2024-06-14 23:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api', '0006_alter_customuser_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='modelodinamico',
            name='iduser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='modelos_dinamicos', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]