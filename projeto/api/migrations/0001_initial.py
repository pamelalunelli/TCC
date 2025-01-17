# Generated by Django 4.1.13 on 2024-05-06 23:57

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BR_CaracteristicasEdificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(null=True)),
                ('tipologia', models.IntegerField(null=True)),
                ('elevador', models.BooleanField()),
                ('posicao', models.IntegerField(null=True)),
                ('conservacao', models.IntegerField(null=True)),
                ('orientacao', models.IntegerField(null=True)),
                ('esquadria', models.IntegerField(null=True)),
                ('estrutura', models.IntegerField(null=True)),
                ('acabamento', models.IntegerField(null=True)),
                ('utilizacao', models.IntegerField(null=True)),
                ('utilizacaoSecundaria', models.IntegerField(null=True)),
                ('condicao', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BR_ImovelCadastral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matriculaImobiliaria_IC', models.IntegerField(null=True)),
                ('inscricaoImobiliaria', models.IntegerField(null=True)),
                ('idCadastro_IC', models.IntegerField(null=True)),
                ('areaTerreno', models.FloatField()),
                ('tipoImovel', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BR_ImovelCondominio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('areaTotalTerreno', models.FloatField()),
                ('areaTotalTerreno_privativa', models.FloatField()),
                ('areaTotalTerreno_comum', models.FloatField()),
                ('areaTotalConstruida', models.FloatField()),
                ('areaTotalConstruida_privada', models.FloatField()),
                ('areaTotalConstruida_comum', models.FloatField()),
                ('numCasas', models.IntegerField(null=True)),
                ('numTorres', models.IntegerField(null=True)),
                ('totalUnidadesPrivativas', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BR_ImovelLegal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_ORIP', models.IntegerField(null=True)),
                ('matricula', models.IntegerField(null=True)),
                ('descricaoImovel', models.CharField(blank=True, max_length=1000, null=True)),
                ('classesUsoSoloReg', models.IntegerField(null=True)),
                ('inscricaoImob', models.IntegerField(null=True)),
                ('idCadastro_IL', models.IntegerField(null=True)),
                ('dataAbertura', models.DateField()),
                ('matriculaOrigem', models.IntegerField(null=True)),
                ('matriculaNova', models.IntegerField(null=True)),
                ('valorImovel', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='BR_Logradouro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoLogradouro_Log', models.IntegerField(null=True)),
                ('nomeAnterior', models.CharField(blank=True, max_length=100, null=True)),
                ('nomeLogradouro_Log', models.CharField(blank=True, max_length=100, null=True)),
                ('cep_Log', models.IntegerField(null=True)),
                ('atoCriacao', models.CharField(blank=True, max_length=100, null=True)),
                ('dataCriacao', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='BR_Parcela',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idLote', models.IntegerField(null=True)),
                ('limitacao', models.IntegerField(null=True)),
                ('tipoTopografia', models.IntegerField(null=True)),
                ('numVagasCobertas', models.IntegerField(null=True)),
                ('situacao', models.IntegerField(null=True)),
                ('adequacaoOcupacao', models.IntegerField(null=True)),
                ('nivelamento', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoLogradour_End', models.IntegerField(null=True)),
                ('nomeLogradouro_End', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.IntegerField(null=True)),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('bairro', models.CharField(blank=True, max_length=50, null=True)),
                ('cidade', models.CharField(blank=True, max_length=50, null=True)),
                ('estado', models.CharField(blank=True, max_length=50, null=True)),
                ('cep_End', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FieldMatching',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iduserdata', models.IntegerField()),
                ('inputField', models.CharField(max_length=255)),
                ('referenceField', models.CharField(max_length=255)),
                ('tableName', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModeloDinamico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iduser', models.IntegerField(null=True)),
                ('nome', models.CharField(max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('dataCSV', models.TextField()),
                ('dataJSON', models.TextField()),
                ('matchingTableName', models.CharField(max_length=255, null=True)),
                ('isConcluded', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
