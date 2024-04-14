from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class CampoMatch(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    nome_campo_entrada = models.CharField(max_length=255) 
    nome_campo_referencia = models.CharField(max_length=255)
    modelo_referencia = models.CharField(max_length=255)
    data_matching = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'nome_campo_entrada']
        
class BR_CaracteristicasEdificacao(models.Model):
    status = models.IntegerField(null=True)
    tipologia = models.IntegerField(null=True)
    elevador = models.BooleanField()
    posicao = models.IntegerField(null=True)
    conservacao = models.IntegerField(null=True)
    orientacao = models.IntegerField(null=True)
    esquadria = models.IntegerField(null=True)
    estrutura = models.IntegerField(null=True)
    acabamento = models.IntegerField(null=True)
    utilizacao = models.IntegerField(null=True)
    utilizacaoSecundaria = models.IntegerField(null=True)
    condicao = models.IntegerField(null=True)

class BR_ImovelCadastral(models.Model):
    matriculaImobiliaria_IC = models.IntegerField(null=True)
    inscricaoImobiliaria = models.IntegerField(null=True)
    idCadastro_IC = models.IntegerField(null=True)
    areaTerreno = models.FloatField()
    tipoImovel = models.IntegerField(null=True)

class BR_ImovelCondominio(models.Model):
    areaTotalTerreno = models.FloatField()
    areaTotalTerreno_privativa = models.FloatField()
    areaTotalTerreno_comum = models.FloatField()
    areaTotalConstruida = models.FloatField()
    areaTotalConstruida_privada = models.FloatField()
    areaTotalConstruida_comum = models.FloatField()
    numCasas = models.IntegerField(null=True)
    numTorres = models.IntegerField(null=True)
    totalUnidadesPrivativas = models.IntegerField(null=True)

class BR_ImovelLegal(models.Model):
    cod_ORIP = models.IntegerField(null=True)
    matricula = models.IntegerField(null=True) 
    descricaoImovel = models.CharField(max_length=1000, null=True, blank=True)
    classesUsoSoloReg = models.IntegerField(null=True)
    inscricaoImob = models.IntegerField(null=True)
    idCadastro_IL = models.IntegerField(null=True)
    dataAbertura = models.DateField()
    matriculaOrigem = models.IntegerField(null=True) 
    matriculaNova = models.IntegerField(null=True) 
    valorImovel = models.FloatField()

class BR_Logradouro(models.Model):
    tipoLogradouro_Log = models.IntegerField(null=True) 
    nomeAnterior = models.CharField(max_length=100, null=True, blank=True)
    nomeLogradouro_Log = models.CharField(max_length=100, null=True, blank=True)
    cep_Log = models.IntegerField(null=True) 
    atoCriacao = models.CharField(max_length=100, null=True, blank=True)
    dataCriacao = models.DateField()

class BR_Parcela(models.Model):
    idLote = models.IntegerField(null=True) 
    limitacao = models.IntegerField(null=True) 
    tipoTopografia = models.IntegerField(null=True) 
    numVagasCobertas = models.IntegerField(null=True) 
    situacao = models.IntegerField(null=True) 
    adequacaoOcupacao = models.IntegerField(null=True) 
    nivelamento = models.IntegerField(null=True) 

class Endereco(models.Model):
    tipoLogradour_End = models.IntegerField(null=True) 
    nomeLogradouro_End = models.CharField(max_length=100, null=True, blank=True)
    numero = models.IntegerField(null=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cep_End =  models.IntegerField(null=True)

class ModeloDinamico(models.Model):
    nome = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField()

class EquipamentoPublico(models.Model):
    id_equipamento = models.AutoField(primary_key=True)
    id_modeloDinamico = models.ForeignKey(ModeloDinamico, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=20, null=True, blank=True)

class Geometria(models.Model):
    id_geom = models.AutoField(primary_key=True)
    id_modeloDinamico = models.ForeignKey(ModeloDinamico, on_delete=models.CASCADE, null=True, blank=True)
    centroide = models.CharField(max_length=20, null=True, blank=True)
    area = models.CharField(max_length=20, null=True, blank=True)

class Proprietario(models.Model):
    id_proprietario = models.AutoField(primary_key=True)
    id_modeloDinamico = models.ForeignKey(ModeloDinamico, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=20, null=True, blank=True)
    data_nasc = models.CharField(max_length=20, null=True, blank=True)
    cpf = models.CharField(max_length=20, null=True, blank=True)

class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=90)
    password = models.CharField(max_length=90)

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        verbose_name=_('user permissions'),
        blank=True,
    )
