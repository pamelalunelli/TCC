import csv
import json
from typing import TextIO
import time
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .forms import CSVUploadForm
from .models import *
from .serializers import CustomUserSerializer
from django.http import HttpResponse
from django.apps import apps
from django.db import connection
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from .models import FieldMatching
from io import BytesIO
import base64
from django.template.loader import render_to_string
from collections import defaultdict
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from fpdf import FPDF

CustomUser = get_user_model()

'''def detectDelimiter(csvFile: TextIO) -> str:
    dialect = csv.Sniffer().sniff(csvFile.read(1024))
    return dialect.delimiter'''

@transaction.atomic
@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                arquivo_csv = form.cleaned_data['csv_arq']
                nome_arquivo = arquivo_csv.name

                arquivo_formatado = arquivo_csv.read().decode('utf-8').splitlines()
                
                cabecalho = arquivo_formatado[0]
                campos = cabecalho.split(',')

                dados_csv = []

                tabela_nome = f"input_{int(time.time())}"

                modelo_dinamico = ModeloDinamico.objects.create(nome=nome_arquivo)
                id = modelo_dinamico.id

                createTable(tabela_nome, campos, dados_csv, id)

                modelo_dinamico.data = json.dumps(dados_csv)
                modelo_dinamico.save()

                response_data = {'id': id, 'fields': campos, 'tableName': tabela_nome}
                print("response_data")
                print(response_data)
                print(f"CSV processado com sucesso! ID: {id}")

                return JsonResponse(response_data)
            except Exception as e:
                print(f"Erro ao processar: {e}")
                return JsonResponse({'error': 'Erro interno ao processar a solicitação'}, status=500)
        else:
            print("Formulário inválido:", form.errors)
            return JsonResponse({'error': 'Formulário inválido'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

def createTable(tabela_nome, campos_renomeados, dados_csv, iduserdata):
    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {tabela_nome}")

        sql_cria_tabela = f"""
        CREATE TABLE {tabela_nome} (
            id serial PRIMARY KEY,
            iduserdata integer,
            {', '.join([campo + ' VARCHAR(255)' for campo in campos_renomeados])}
        )
        """
        print("SQL Criar Tabela:", sql_cria_tabela)
        cursor.execute(sql_cria_tabela)

        sql_insere_tabela = f"""
        INSERT INTO {tabela_nome} (iduserdata, {', '.join(campos_renomeados)})
        VALUES (%s, {', '.join(['%s' for _ in campos_renomeados])})
        """

        values = [[iduserdata] + [linha.get(campo, None) for campo in campos_renomeados] for linha in dados_csv]

        print("Valores a serem inseridos:", values)
        cursor.executemany(sql_insere_tabela, values)

def userData(request, id):

    modelo_dinamico = get_object_or_404(ModeloDinamico, id=id)

    try:
        objectsJson = json.loads(modelo_dinamico.data)
    except json.JSONDecodeError:
        objectsJson = []

    if objectsJson and isinstance(objectsJson, list):
        first_object = objectsJson[0] if objectsJson else {}
        fieldsName = list(first_object.keys())
    else:
        fieldsName = []

    return JsonResponse(fieldsName, safe=False)

def defaultDataTable(request):

    excludedTables = ['FieldMatching', 'ModeloDinamico', 'CustomUser', 'AdminUser']

    models = apps.get_app_config('api').get_models()
    
    tables = []

    for model in models:
        if model._meta.app_label == 'api' and not model._meta.abstract and model._meta.object_name not in excludedTables:
            modelName = model._meta.object_name
            fields = [field.name for field in model._meta.get_fields() if field.concrete]

            table = {
                'name': modelName,
                'fields': fields,
            }
            tables.append(table)

    return JsonResponse(tables, safe=False)

@csrf_exempt
def processForm (request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            iduserdata = data.pop('userDataId', None)  

            inputFieldTestList = []
            for tableNameTest, fieldsData in data.items():
                for referenceFieldTest, inputFieldTest in fieldsData.items():
                    FieldMatching.objects.create(
                        inputField=inputFieldTest,
                        referenceField=referenceFieldTest,
                        tableName=tableNameTest,
                        iduserdata=iduserdata
                    )
                    inputFieldTestList.append(inputFieldTest)
            
            response = generateReport(iduserdata)

            pdf_content_base64 = base64.b64encode(response.content).decode('utf-8')

            return HttpResponse(render_to_string('open_pdf_window.html', {'pdf_content_base64': pdf_content_base64}), status=200)

        except Exception as e:
            return HttpResponse("Ocorreu um erro ao processar os dados: " + str(e), status=500)

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generateReport(iduserdata):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    fieldMatchings = FieldMatching.objects.filter(iduserdata=iduserdata)

    tableData = {}
    tableConformity = {}

    for fieldMatching in fieldMatchings:
        if fieldMatching.tableName not in tableData:
            tableData[fieldMatching.tableName] = []
            tableConformity[fieldMatching.tableName] = {'conform': 0, 'nonconform': 0}

        tableData[fieldMatching.tableName].append(fieldMatching)
        if fieldMatching.referenceField and fieldMatching.inputField:
            tableConformity[fieldMatching.tableName]['conform'] += 1
        else:
            tableConformity[fieldMatching.tableName]['nonconform'] += 1

    buffer = response

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Definindo estilos
    sampleStyles = getSampleStyleSheet()
    boldStyle = ParagraphStyle(name='Bold', parent=sampleStyles["Normal"])
    boldStyle.fontName = 'Helvetica-Bold'
    sampleStyles.add(boldStyle)

    # Adicionando títulos
    elements.append(Paragraph("Relatório de Conformidade", sampleStyles["Title"]))
    elements.append(Paragraph("Comparação entre Modelo de", sampleStyles["Heading3"]))
    elements.append(Paragraph("Referência e Arquivo de entrada", sampleStyles["Heading3"]))

    for tableName, matches in tableData.items():
        elements.append(Paragraph(f'<b>{tableName}</b>', sampleStyles["Heading2"]))

        data = [['Campo de Referência', 'Campo de Entrada', 'Conformidade']]
        for match in matches:
            referenceField = match.referenceField
            inputField = match.inputField
            conformity = 'Conforme' if referenceField and inputField else 'Não Conforme'
            data.append([referenceField, inputField, conformity])

        table = Table(data, colWidths=[180, 180, 90], hAlign='LEFT')
        table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                                   ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                                   ('LINEABOVE', (0, 1), (-1, -1), 1, colors.black),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)

        totalFields = len(matches)
        totalConformFields = tableConformity[tableName]['conform']
        conformityPercentage = (totalConformFields / totalFields) * 100
        conformityPercentage = round(conformityPercentage, 2)

        elements.append(Paragraph(f'Percentual de conformidade: {conformityPercentage}%', sampleStyles["Normal"]))

    overallConformityPercentage = (sum(tc['conform'] for tc in tableConformity.values()) / sum(len(td) for td in tableData.values())) * 100
    overallConformityPercentage = round(overallConformityPercentage, 2)
    elements.append(Paragraph(f'<b>Percentual geral de conformidade: {overallConformityPercentage}%</b>', sampleStyles["Bold"]))

    elements.append(Paragraph("<br/><br/>", sampleStyles["Normal"]))

    doc.build(elements)

    pdfContent = buffer.getvalue()
    buffer.close()

    response.write(pdfContent)

    return response

def userHistory(request):
    return JsonResponse(list(ModeloDinamico.objects.values()), safe=False)

@csrf_exempt 
@require_http_methods(["DELETE"])
def userHistoryDelete(request, id):
    try:
        ModeloDinamico.objects.get(pk=id).delete()
        return JsonResponse({'mensagem': 'Objeto excluído com sucesso.'})
    except ModeloDinamico.DoesNotExist:
        return JsonResponse({'erro': 'O objeto não foi encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["PATCH"])
def userHistoryEdit(request, id):
    try:
        object = ModeloDinamico.objects.get(pk=id)
        data = json.loads(request.body.decode('utf-8'))
        newName = data.get('nome', None)
        
        if newName is not None:
            object.nome = newName
            object.save()

            return JsonResponse({'mensagem': 'Campo editado com sucesso.'})
        else:
            return JsonResponse({'erro': 'O novo nome não foi fornecido.'}, status=400)

    except ModeloDinamico.DoesNotExist:
        return JsonResponse({'erro': 'O objeto não foi encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        user_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'user_info': user_info}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CheckAvailabilityView(CreateAPIView):
    def get(self, request):
        emails = CustomUser.objects.values_list('email', flat=True)
        usernames = CustomUser.objects.values_list('username', flat=True)

        return Response({'emails': emails, 'usernames': usernames}, status=status.HTTP_200_OK)