import json
from django.apps import apps
from django.db import connection
from django.http import HttpResponse, JsonResponse
import textdistance as td
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator
from datetime import datetime

@csrf_exempt
def createMatchingTable(request):
    if request.method == 'POST':
        try:
            bodyUnicode = request.body.decode('utf-8')
            tableName = bodyUnicode.strip()

            print("o tableName é", tableName)
            with connection.cursor() as cursor:
                
                tableName = "matching_" + tableName.replace('"', '')
                
                cursor.execute(f"DROP TABLE IF EXISTS {tableName}")
                
                createTableQuery = f"""
                CREATE TABLE {tableName} (
                    id serial PRIMARY KEY,
                    iduserdata integer,
                    inputField VARCHAR(255),
                    referenceField VARCHAR(255),
                    modelName VARCHAR(255),
                    editBased_hamming FLOAT DEFAULT 0.0,
                    editBased_mlipns FLOAT DEFAULT 0.0,
                    editBased_levenshtein FLOAT DEFAULT 0.0,
                    editBased_dameraulevenshtein FLOAT DEFAULT 0.0,
                    editBased_jarowinkler FLOAT DEFAULT 0.0,
                    editBased_strcmp95 FLOAT DEFAULT 0.0,
                    editBased_needlemanwunsch FLOAT DEFAULT 0.0,
                    editBased_gotoh FLOAT DEFAULT 0.0,
                    editBased_smithwaterman FLOAT DEFAULT 0.0,
                    tokenBased_jaccardindex FLOAT DEFAULT 0.0,
                    tokenBased_sørensendicecoefficient FLOAT DEFAULT 0.0,
                    tokenBased_tverskyindex FLOAT DEFAULT 0.0,
                    tokenBased_overlapcoefficient FLOAT DEFAULT 0.0,
                    tokenBased_cosinesimilarity FLOAT DEFAULT 0.0,
                    tokenBased_mongeelkan FLOAT DEFAULT 0.0,
                    tokenBased_bagdistance FLOAT DEFAULT 0.0,
                    sequenceBased_lcsseq FLOAT DEFAULT 0.0,
                    sequenceBased_lcsstr FLOAT DEFAULT 0.0,
                    sequenceBased_ratcliffobershelpsimilarity FLOAT DEFAULT 0.0,
                    compressionBased_arithmeticcoding FLOAT DEFAULT 0.0,
                    compressionBased_rle FLOAT DEFAULT 0.0,
                    compressionBased_bwtrle FLOAT DEFAULT 0.0,
                    compressionBased_squareroot FLOAT DEFAULT 0.0,
                    compressionBased_entropy FLOAT DEFAULT 0.0,
                    compressionBased_bz2 FLOAT DEFAULT 0.0,
                    compressionBased_lzma FLOAT DEFAULT 0.0,
                    compressionBased_zlib FLOAT DEFAULT 0.0,
                    phonetic_mra FLOAT DEFAULT 0.0,
                    phonetic_editex FLOAT DEFAULT 0.0,
                    simple_prefix FLOAT DEFAULT 0.0,
                    simple_postfix FLOAT DEFAULT 0.0,
                    simple_length FLOAT DEFAULT 0.0,
                    simple_identity FLOAT DEFAULT 0.0,
                    simple_matrix FLOAT DEFAULT 0.0,
                    generalindex FLOAT DEFAULT 0.0,
                    userChoice BOOLEAN DEFAULT FALSE,
                    tableName VARCHAR(255)
                )
                """
                cursor.execute(createTableQuery)

            return HttpResponse(tableName, content_type='text/plain')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def populateMatchingFields(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            matchingTableName = request_data.get('matchingTableName', {}).get('data', '')
            fieldsCSV = request_data.get('fieldsCSV', [])
            userDataId = request_data.get('userDataId', None)

            referenceFieldsByModel = getReferenceFieldsByModel()

            with connection.cursor() as cursor:
                for inputField in fieldsCSV:
                    for model, referenceFields in referenceFieldsByModel.items():
                        for referenceField in referenceFields:
                            try:
                                cursor.execute(f"""
                                    INSERT INTO {matchingTableName} (iduserdata, inputField, referenceField, modelName, tableName)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, [userDataId, inputField, referenceField, model, matchingTableName])
                            except Exception as e:
                                return JsonResponse({'error': str(e)}, status=500)
            
            calculatingSimilarity(matchingTableName)
            topReferencesJSON = findMostProbableReferences(matchingTableName)
            print("--------------------------------------------------------------")
            print(topReferencesJSON)
            print("--------------------------------------------------------------")
            
            return JsonResponse({'topReferencesJSON': topReferencesJSON})
            #return JsonResponse({'message': 'Success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def getReferenceFieldsByModel():
    referenceFieldsByModel = {}
    excludedModels = ['FieldMatching', 'ModeloDinamico', 'CustomUser', 'AdminUser']
    appModels = apps.get_app_config('api').get_models()
    for model in appModels:
        if model.__name__ not in excludedModels:
            fields = [field.name for field in model._meta.get_fields() if field.concrete and (not field.name.startswith('fk_') or field.name == 'id')]
            referenceFieldsByModel[model.__name__] = fields

    return referenceFieldsByModel

@csrf_exempt
def calculatingSimilarity(tableName):
    
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT inputField, referenceField FROM {tableName}")

        for row in cursor.fetchall():
            inputFieldDBOriginal = row[0]
            referenceFieldDBOriginal = row[1]
            
            inputFieldDB = inputFieldDBOriginal.lower()
            referenceFieldDB = referenceFieldDBOriginal.lower()

            # Cálculo dos índices de similaridade
            #editBasedHamming = td.hamming.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedMLIPNS = td.mlipns.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedLevenshtein = td.levenshtein.normalized_similarity(inputFieldDB, referenceFieldDB)
            editBasedDamerauLevenshtein = td.damerau_levenshtein.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedJaroWinkler = td.jaro_winkler.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedStrcmp95 = td.strcmp95.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedNeedlemanWunsch = td.needleman_wunsch.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedGotoh = td.gotoh.normalized_similarity(inputFieldDB, referenceFieldDB)
            #editBasedSmithWaterman = td.smith_waterman.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenBasedJaccardIndex = td.jaccard.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenBasedSorensenDiceCoefficient = td.sorensen_dice.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenTverskyIndex = td.tversky.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenOverlapCoefficient = td.overlap.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenTanimotoDistance = td.tanimoto.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenCosineSimilarity = td.cosine.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenMongeElkan = td.monge_elkan.normalized_similarity(inputFieldDB, referenceFieldDB)
            #tokenBagDistance = td.bag.normalized_similarity(inputFieldDB, referenceFieldDB)
            #sequenceBasedLCSSeq = td.lcsseq.normalized_similarity(inputFieldDB, referenceFieldDB)
            #sequenceBasedLCSStr = td.lcsstr.normalized_similarity(inputFieldDB, referenceFieldDB)
            #sequenceBasedRatcliffObershelpSimilarity = td.ratcliff_obershelp.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedArithmeticcoding = td.arith_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedRLE = td.rle_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedBWTRLE = td.bwtrle_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedSquareroot = td.sqrt_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedEntropy = td.entropy_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedBZ2 = td.bz2_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedLZMA = td.lzma_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #compressionBasedZlib = td.zlib_ncd.normalized_similarity(inputFieldDB, referenceFieldDB)
            #phoneticMRA = td.mra.normalized_similarity(inputFieldDB, referenceFieldDB)
            #phoneticEditex = td.editex.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simplePrefix = td.prefix.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simplePostfix = td.postfix.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simpleLength = td.length.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simpleIdentity = td.identity.normalized_similarity(inputFieldDB, referenceFieldDB)
            #simpleMatrix = td.matrix.normalized_similarity(inputFieldDB, referenceFieldDB)
            #generalIndex = (editBasedHamming*0.25)  + (editBasedLevenshtein*0.25) + (simplePrefix*0.5)
            generalIndex = (editBasedDamerauLevenshtein)
            userChoice = False

            cursor.execute(f"""
                            UPDATE {tableName}
                            SET 
                                editBased_levenshtein = {editBasedDamerauLevenshtein},
                                generalindex = {generalIndex},
                                userChoice = 'False'
                            WHERE 
                                inputfield = '{inputFieldDBOriginal}' AND referencefield = '{referenceFieldDBOriginal}'
                        """)

        connection.commit()

api_view(['POST'])
@csrf_exempt
def retrievingMatchingFields(request):
    if request.method == 'POST':

        request_data = json.loads(request.body)
        matchingTableName = request_data.get('matchingTableName', '')

        try:
            topReferencesJSON = findMostProbableReferences(matchingTableName)
            return JsonResponse({'topReferencesJSON': topReferencesJSON})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def findMostProbableReferences(tableName, topN=5):
    with connection.cursor() as cursor:
        query = f"""
            SELECT inputfield, referencefield, generalindex 
            FROM {tableName}
        """
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)

    grouped = df.groupby('referencefield')

    mostProbableReferences = {}
    for referencefield, group in grouped:
        topReferences = group.nlargest(topN, 'generalindex')['inputfield'].tolist()
        remainingReferences = group[~group['inputfield'].isin(topReferences)]['inputfield'].tolist()
        combinedReferences = ['SUGESTÃO'] + topReferences + ['ORDEM ALFABÉTICA'] + sorted(remainingReferences)
        mostProbableReferences[referencefield] = combinedReferences

    return json.dumps(mostProbableReferences, indent=4)

api_view(['POST'])
@csrf_exempt
def getUserChoices(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        table_name = data.get('matchingTableName')

        if not table_name:
            return JsonResponse({'error': 'Parameter "matchingTableName" is required'}, status=400)

        with connection.cursor() as cursor:
            query = f"""
            SELECT modelname, referencefield, inputfield
            FROM {table_name}
            WHERE userchoice = True
            """
            cursor.execute(query)
            data = cursor.fetchall()
            userChoices = {}
            for row in data:
                model_name, reference_field, input_field = row
                if model_name not in userChoices:
                    userChoices[model_name] = {}
                userChoices[model_name][reference_field] = input_field

        return JsonResponse(userChoices, safe=False)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


#Populando a tabela de descrição dos campos

'''INSERT INTO public.api_fielddescription ("fieldName", "fieldDescription", "fieldModel", "fieldType") VALUES
('areaTotalTerreno', 'Área total do imóvel. Unidade: m².', 'BR_CaracteristicasTerreno', 'float'),
('areaTotalTerreno_privativa', 'Área total do terreno privativa. Por exemplo: área do lote em condomínio horizontal. Unidade: m².', 'BR_CaracteristicasTerreno', 'float'),
('areaTotalTerreno_comum', 'Área total do terreno comum. Por exemplo: área do lote em condomínio horizontal incluída a área de lazer. Unidade: m².', 'BR_CaracteristicasTerreno', 'float'),
('areaTotalConstruida', 'Área total edificada sobre o imóvel. Por exemplo: total de área edificada em condomínio horizontal. Unidade: m².', 'BR_CaracteristicasTerreno', 'float'),
('areaTotalConstruida_privada', 'Área total construída privada. Por exemplo: área edificada sobre lote individualizado em condomínio horizontal. Unidade: m².', 'BR_CaracteristicasTerreno', 'float'),
('areaTotalConstruida_comum', 'Área total construída comum. Por exemplo: total de área construída incluída construções da área de lazer. Unidade: m².', 'BR_CaracteristicasTerreno', 'float'),
('numCasas', 'Número de edificações construídas sobre o imóvel. Por exemplo: 1, 2, 3, 4. Unidade: número inteiro.', 'BR_CaracteristicasTerreno', 'int'),
('numTorres', 'Número de torres incorporadas sobre o imóvel, em caso de condomínio vertical. Por exemplo: 1, 2, 3. Unidade: número inteiro.', 'BR_CaracteristicasTerreno', 'int'),
('totalUnidadesPrivativas', 'Total de construções individualizadas. Por exemplo: total de apartamentos de um prédio. Por exemplo: 12, 48, 50. Unidade: número inteiro.', 'BR_CaracteristicasTerreno', 'int'),
('limitacao', 'Tipo de limite que cerca o imóvel. Por exemplo: muro, cerca, sem delimitação física. Unidade: campo descritivo.', 'BR_CaracteristicasTerreno', 'varchar'),
('topografia', 'Topografia do terreno. Por exemplo: plana, ondulada, acidentada. Unidade: campo descritivo.', 'BR_CaracteristicasTerreno', 'varchar'),
('situacao', 'Situação do terreno. Por exemplo: regular, irregular, sem ocupação. Unidade: campo descritivo.', 'BR_CaracteristicasTerreno', 'varchar'),
('numVagas', 'Número de vagas disponíveis no imóvel. Por exemplo: 1, 2, 3. Unidade: número inteiro.', 'BR_CaracteristicasTerreno', 'int'),
('nivelamento', 'Tipo de nivelamento do terreno. Por exemplo: plano, em aclive, em declive. Unidade: campo descritivo.', 'BR_CaracteristicasTerreno', 'varchar'),
('area', 'Área da edificação. Unidade: m².', 'BR_CaracteristicasEdificacao', 'float'),
('status', 'Status da edificação. Por exemplo: nova, usada, em construção. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('tipologia', 'Tipologia da edificação. Por exemplo: residencial, comercial, industrial. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('elevador', 'Presença de elevador na edificação. Por exemplo: True/False, 0/1 Unidade: booleano.', 'BR_CaracteristicasEdificacao', 'bool'),
('posicao', 'Posição da edificação no terreno. Por exemplo: frente, meio, fundos. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('conservacao', 'Estado de conservação da edificação. Por exemplo: excelente, bom, regular, ruim. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('orientacao', 'Orientação da edificação. Por exemplo: norte, sul, leste, oeste. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('esquadria', 'Tipo de esquadria utilizada na edificação. Por exemplo: alumínio, madeira, PVC. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('estrutura', 'Tipo de estrutura da edificação. Por exemplo: concreto, aço, madeira. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('acabamento', 'Tipo de acabamento da edificação. Por exemplo: luxo, padrão, simples. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('utilizacao', 'Utilização principal da edificação. Por exemplo: residencial, comercial. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('utilizacaoSecundaria', 'Utilização secundária da edificação. Por exemplo: loja, depósito. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('condicao', 'Condição atual da edificação. Por exemplo: habitável, inabitável. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('cobertura', 'Tipo de cobertura da edificação. Por exemplo: telha, laje. Unidade: campo descritivo.', 'BR_CaracteristicasEdificacao', 'varchar'),
('energiaEletrica', 'Presença de energia elétrica no imóvel. Por exemplo: True/False, 0/1 Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('abastecimentoAgua', 'Presença de abastecimento de água no imóvel. Por exemplo: True/False, 0/1 Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('iluminacaoPublica', 'Presença de iluminação pública no imóvel. Por exemplo: True/False, 0/1 Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('esgoto', 'Presença de sistema de esgoto no imóvel. Por exemplo: True/False, 0/1 Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('coletaLixo', 'Presença de coleta de lixo no imóvel. Por exemplo: True/False, 0/1 Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('pavimentacao', 'Presença de pavimentação no imóvel. Por exemplo: True/False, 0/1. Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('telefonia', 'Presença de telefonia no imóvel. Por exemplo: True/False, 0/1. Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('arborizacao', 'Presença de arborização no imóvel. Por exemplo: True/False, 0/1. Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('passeio', 'Presença de passeio público no imóvel. Por exemplo: True/False, 0/1. Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('drenagemPluvial', 'Presença de drenagem pluvial no imóvel. Por exemplo: True/False, 0/1. Unidade: booleano.', 'BR_Infraestrutura', 'bool'),
('valorVenal', 'Valor venal do imóvel para fins tributários. Unidade: R$.', 'BR_Tributo', 'float'),
('IPTU', 'Valor do Imposto Predial e Territorial Urbano (IPTU). Unidade: R$.', 'BR_Tributo', 'float'),
('isencaoIPTU', 'Indica se há isenção do IPTU. Por exemplo: True/False, 0/1. Unidade: booleano.', 'BR_Tributo', 'bool'),
('fatorTerreno', 'Fator do terreno para cálculo tributário. Por exemplo: 1,1, 0,8. Unidade: coeficiente.', 'BR_Tributo', 'float'),
('codigo', 'Código do trecho do logradouro. Unidade: campo descritivo.', 'BR_TrechoLogradouro', 'varchar'),
('valor', 'Valor associado ao trecho do logradouro. Unidade: R$.', 'BR_TrechoLogradouro', 'float'),
('numero', 'Número do endereço do imóvel. Unidade: campo descritivo.', 'BR_EnderecoImovel', 'varchar'),
('complemento', 'Complemento do endereço do imóvel. Unidade: campo descritivo.', 'BR_EnderecoImovel', 'varchar'),
('bairro', 'Bairro do endereço do imóvel. Unidade: campo descritivo.', 'BR_EnderecoImovel', 'varchar'),
('cep', 'Código de Endereçamento Postal do imóvel. Por exemplo: 88802100, 81630-050. Unidade: campo descritivo.', 'BR_EnderecoImovel', 'varchar'),
('tipoLogradouro', 'Tipo de logradouro. Por exemplo: rua, avenida, travessa. Unidade: campo descritivo.', 'BR_EnderecoCorrespondencia', 'varchar'),
('nomeLogradouro', 'Nome do logradouro. Unidade: campo descritivo.', 'BR_EnderecoCorrespondencia', 'varchar'),
('municipio', 'Nome do município. Unidade: campo descritivo.', 'BR_EnderecoCorrespondencia', 'varchar'),
('UF', 'Unidade Federativa. Unidade: campo descritivo.', 'BR_EnderecoCorrespondencia', 'varchar'),
('CEP', 'Código de Endereçamento Postal. Unidade: campo descritivo.', 'BR_EnderecoCorrespondencia', 'varchar'),
('classificacao', 'Classificação do endereço. Por exemplo: residencial, comercial. Unidade: campo descritivo.', 'BR_EnderecoCorrespondencia', 'varchar'),
('nomeFantasia', 'Nome fantasia da pessoa jurídica. Unidade: campo descritivo.', 'BR_PessoaJuridica', 'varchar'),
('razaoSocial', 'Razão social da pessoa jurídica. Unidade: campo descritivo.', 'BR_PessoaJuridica', 'varchar'),
('estadoCivil', 'Estado civil da pessoa física. Por exemplo: solteiro, casado. Unidade: campo descritivo.', 'BR_PessoaFisica', 'varchar'),
('nome', 'Nome da pessoa física. Unidade: campo descritivo.', 'BR_PessoaFisica', 'varchar'),
('telefone', 'Número de telefone de contato. Por exemplo: (99) 999999999, (88) 88888-8888 Unidade: campo descritivo.', 'BR_ContatoPessoa', 'varchar'),
('celular', 'Número de celular de contato. Unidade: campo descritivo.', 'BR_ContatoPessoa', 'varchar'),
('email', 'Endereço de e-mail de contato. Unidade: campo descritivo.', 'BR_ContatoPessoa', 'varchar'),
('documento', 'Tipo de documento de identificação. Por exemplo: RG, CPF. Unidade: campo descritivo.', 'BR_DocumentoPessoa', 'varchar'),
('numeroDocumento', 'Número do documento de identificação. Unidade: campo descritivo.', 'BR_DocumentoPessoa', 'varchar'),
('tipoPessoa', 'Tipo de pessoa. Por exemplo: física, jurídica. Unidade: campo descritivo.', 'BR_Pessoa', 'varchar'),
('codContribuinte', 'Código do contribuinte no cadastro municipal. Unidade: campo descritivo.', 'BR_Pessoa', 'varchar'),
('papel', 'Papel da pessoa no cadastro. Por exemplo: proprietário, locatário. Unidade: campo descritivo.', 'BR_Pessoa', 'varchar'); '''