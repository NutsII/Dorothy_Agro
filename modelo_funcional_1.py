# CONTACTA O PROJETA API do CpTEC PARA OBTER INFOS #

from typing import List

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import urllib.request, json
import numpy as np
import datetime
import pandas as pd


###### DEFINIR OS PARÂMETROS DA RODADA - PREENCHER ####

caminho_planilha = '/home/rodfranco/Documentos/DPM3.xlsx'
nome_aba = 'Plantio Precoce'
dia_ult_fungicida = '2019-12-13'

diagnostico_visual = np.array(

[['Doença','Nível'],
['oidio',      '0'],
['ferrugem',    '0'],
['mancha alvo', '0'],
['antracnose',  '0'],
['mofo branco', '0'],
['olho de rã',  '0']
 ]

)

latitude = '-13.40'
longitude = '-46.09'

########################################

dia_da_emergencia = '2019-12-01' #ok
dia_do_v8 = '2019-01-15' #ok
dia_da_colheita = '2020-03-30'
#dia_do_plantio = '2019-11-21' #ok
dia_aparecimento_esporo = '2099-11-21'
#estadio = 'V2'

def posicao(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def ProcValores(valor_procurado,ocorrencia,matriz_procurada,coluna):

    proc_pt1 = np.where(matriz_procurada==valor_procurado)
    proc_pt2 = [item[ocorrencia] for item in proc_pt1]
    proc_pt3 = matriz_procurada[proc_pt2[0]][coluna]

    return proc_pt3


def ProcIndice(valor_procurado,ocorrencia,matriz_procurada,coord):

    proc_pt1 = np.where(matriz_procurada==valor_procurado)
    proc_pt2 = [item[ocorrencia] for item in proc_pt1]
    proc_pt3 = 'Verificar'
    if coord == 'X':
        proc_pt3 = proc_pt2[0]
    if coord == 'Y':
        proc_pt3 = proc_pt2[1]
    return proc_pt3

a = pd.read_excel(caminho_planilha, header=6, sheet_name=nome_aba)
planilha = pd.DataFrame.to_numpy(a)

dt_hoje = datetime.datetime.now()
dt_hoje = dt_hoje.replace(hour=0,minute=0,second=0,microsecond=0)

diagnostico_bool_vect = np.where(diagnostico_visual=='4')
diagnostico_bool_vect_2 = np.where(diagnostico_visual=='5')

if (diagnostico_bool_vect[0].size > 0 or diagnostico_bool_vect_2[0].size > 0):
    diagnostico_bool = True
else:
    diagnostico_bool = False


b = ProcIndice(dt_hoje,0,planilha,'X')

planilha_corte = planilha[0:b,[0,5,1,2,3,4]]

nan_remover = pd.isnull(planilha_corte)
planilha_corte[nan_remover] = 0

"""
for contador_conv in range (0 , len(planilha_corte)):
    if type(planilha_corte[contador_conv][0]) == 'Timestamp':
        meio = planilha_corte[contador_conv][0].to_pydatetime()
    else:
        meio = planilha_corte[contador_conv][0]
    planilha_corte[contador_conv][0] =  meio.strftime('%Y-%m-%d')
"""
for contador_conv in range (0 , len(planilha_corte)):
    if type(planilha_corte[contador_conv, 0]) == 'Timestamp':
        meio = planilha_corte[contador_conv,0].to_pydatetime()
    else:
        meio = planilha_corte[contador_conv,0]
    planilha_corte[contador_conv,0] =  meio.strftime('%Y-%m-%d')

estadio = planilha_corte[-1,3]

dia_do_plantio = planilha_corte[0,0]
esp_estad_0 = np.where(planilha_corte == 'Sim')
esp_estad = esp_estad_0[0]

if esp_estad.size > 0:
    dia_aparecimento_esporo = planilha_corte[esp_estad[0],0]

dp = datetime.datetime.strptime(dia_do_plantio, '%Y-%m-%d')
de = datetime.datetime.strptime(dia_da_emergencia, '%Y-%m-%d')
dv8 = datetime.datetime.strptime(dia_do_v8, '%Y-%m-%d')
dc = datetime.datetime.strptime(dia_da_colheita, '%Y-%m-%d')
desp = datetime.datetime.strptime(dia_aparecimento_esporo, '%Y-%m-%d')
duf = datetime.datetime.strptime(dia_ult_fungicida, '%Y-%m-%d')

duf_delta = dt_hoje - duf
duf_delta_dias = duf_delta.days

api_1 = "https://projeta.cptec.inpe.br/api/v1/public/ETA/2/DAILY/2/11/2019/12/2019/PREC/" + latitude + "/" + longitude + "/"
api_2 = "https://projeta.cptec.inpe.br/api/v1/public/ETA/2/DAILY/2/1/2020/4/2020/PREC/" + latitude + "/" + longitude + "/"

api_3 = "https://projeta.cptec.inpe.br/api/v1/public/ETA/2/HOURLY/1/12/2019/12/2019/PREC/" + latitude + "/" + longitude + "/"
api_4 = "https://projeta.cptec.inpe.br/api/v1/public/ETA/2/HOURLY/1/1/2020/1/2020/PREC/" + latitude + "/" + longitude + "/"


########################################


with urllib.request.urlopen(api_1) as url:
    data_1 = json.loads(url.read().decode())

with urllib.request.urlopen(api_2) as url:
    data_2 = json.loads(url.read().decode())

    data = data_1 + data_2


with urllib.request.urlopen(api_3) as url:
    data_3 = json.loads(url.read().decode())

with urllib.request.urlopen(api_4) as url:
    data_4 = json.loads(url.read().decode())

    data_b = data_3 + data_4

    data_fim_dados = dt_hoje + datetime.timedelta(days=7)
    data_inicio_dados = dt_hoje + datetime.timedelta(days=-30)

    # DECIFRA O JSON RECEBIDO #
    dados_met = []

    for item in data:
        if (datetime.datetime.strptime(item['date'], '%Y-%m-%d') < data_fim_dados
                and datetime.datetime.strptime(item['date'], '%Y-%m-%d') > data_inicio_dados):
            met_valores = {"date": None, "value": None, "dia": None, "dia_da_semana": None,}
            met_valores['date'] = item['date']
            met_valores['value'] = item['value']

            for contador_subs in range(0,len(planilha_corte)):
                if planilha_corte[contador_subs][0] == met_valores['date']:
                    met_valores['value'] = planilha_corte[contador_subs][1]


            if item['value'] == 0:
                met_valores['dia'] = 0
            else: met_valores['dia'] = 1

            met_valores['dia_da_semana'] = int(datetime.datetime.strptime(item['date'], '%Y-%m-%d').strftime('%w'))

            dados_met.append(met_valores)


    # OBTEM A PRECIPITACAO DOS ULTIMOS 30 DIAS #

    # print(dados_met)

    chuva_acumulada = []
    dias_acumulado = []
    fator_acumulado = []
    dia_da_semana = []
    dia_do_ano = []


    for contador_1 in range(29, len(dados_met)):
        # print(contador_1 - 1)
        a =  dados_met[contador_1]['value'] + dados_met[contador_1-1]['value'] + dados_met[contador_1-2]['value'] + dados_met[contador_1 - 3]['value'] + dados_met[contador_1 - 4]['value'] + dados_met[contador_1 - 5]['value'] + dados_met[contador_1 - 6]['value'] + dados_met[contador_1 - 7]['value'] + dados_met[contador_1 - 8]['value'] + dados_met[contador_1 - 9]['value'] + dados_met[contador_1 - 10]['value'] + dados_met[contador_1 - 11]['value'] + dados_met[contador_1 - 12]['value'] + dados_met[contador_1 - 13]['value'] + dados_met[contador_1 - 14]['value'] + dados_met[contador_1 - 15]['value'] + dados_met[contador_1 - 16]['value'] + dados_met[contador_1 - 17]['value'] + dados_met[contador_1 - 18]['value'] + dados_met[contador_1 - 19]['value'] + dados_met[contador_1 - 20]['value'] + dados_met[contador_1 - 21]['value'] + dados_met[contador_1 - 22]['value'] + dados_met[contador_1 - 23]['value'] + dados_met[contador_1 - 24]['value'] + dados_met[contador_1 - 25]['value'] + dados_met[contador_1 - 26]['value'] + dados_met[contador_1 - 27]['value'] + dados_met[contador_1 - 28]['value'] + dados_met[contador_1 - 29]['value']
        b = dados_met[contador_1]['dia'] + dados_met[contador_1 - 1]['dia'] + dados_met[contador_1 - 2]['dia'] + dados_met[contador_1 - 3]['dia'] + dados_met[contador_1 - 4]['dia'] + dados_met[contador_1 - 5]['dia'] + dados_met[contador_1 - 6]['dia'] + dados_met[contador_1 - 7]['dia'] + dados_met[contador_1 - 8]['dia'] + dados_met[contador_1 - 9]['dia'] + dados_met[contador_1 - 10]['dia'] + dados_met[contador_1 - 11]['dia'] + dados_met[contador_1 - 12]['dia'] + dados_met[contador_1 - 13]['dia'] + dados_met[contador_1 - 14]['dia'] + dados_met[contador_1 - 15]['dia'] + dados_met[contador_1 - 16]['dia'] + dados_met[contador_1 - 17]['dia'] + dados_met[contador_1 - 18]['dia'] + dados_met[contador_1 - 19]['dia'] + dados_met[contador_1 - 20]['dia'] + dados_met[contador_1 - 21]['dia'] + dados_met[contador_1 - 22]['dia'] + dados_met[contador_1 - 23]['dia'] + dados_met[contador_1 - 24]['dia'] + dados_met[contador_1 - 25]['dia'] + dados_met[contador_1 - 26]['dia'] + dados_met[contador_1 - 27]['dia'] + dados_met[contador_1 - 28]['dia'] + dados_met[contador_1 - 29]['dia']
        c = (-2.1433) + (a * 0.1811) + (b*1.2865)
        d = dados_met[contador_1]['dia_da_semana']
        e = datetime.datetime.strptime(dados_met[contador_1]['date'], '%Y-%m-%d')

        contador_1 += 1
        chuva_acumulada.append(a)
        dias_acumulado.append(b)
        fator_acumulado.append(c)
        dia_da_semana.append(d)
        dia_do_ano.append(e)

    # print(type(dia_do_ano))


    while dia_da_semana[0] > 0:
        dia_da_semana.insert(0, dia_da_semana[0] - 1)
        chuva_acumulada.insert(0,0)
        dias_acumulado.insert(0, 0)
        fator_acumulado.insert(0, 0)
        dia_do_ano.insert(0,dia_do_ano[0] - datetime.timedelta(days=1))


    #while dia_da_semana[len(dia_da_semana)] < 6:
    #    dia_da_semana.insert(len(dia_da_semana), dia_da_semana[len(dia_da_semana)] + 1)


    while dia_da_semana[len(dia_da_semana)-1] < 6:

        dia_da_semana.insert(len(dia_da_semana), dia_da_semana[len(dia_da_semana) - 1] + 1)

        chuva_acumulada.insert(len(dia_da_semana), 0)
        dias_acumulado.insert(len(dia_da_semana), 0)
        fator_acumulado.insert(len(dia_da_semana), 0)
        dia_do_ano.insert(len(dia_da_semana), dia_do_ano[len(dia_da_semana)-2] + datetime.timedelta(days=1))



    aplica_fungicida = []
    aplica_fungicida_leg = []
    auxiliar_contador = 0
    af = 0
    leg_af = ''

    for contador_2 in range(0, len(fator_acumulado)):
        if fator_acumulado[contador_2] > 60 and auxiliar_contador == 0 and dia_do_ano[contador_2] >= desp:
            af = 100
            auxiliar_contador = 15
            leg_af = 'Aplicar'
        if diagnostico_bool == True and auxiliar_contador==0 and dia_do_ano[contador_2] >= dt_hoje:
            af = 100
            auxiliar_contador = 15
            leg_af = 'Aplicar'
        if duf_delta_dias < 15:
            auxiliar_contador = 15 - duf_delta_dias
        if dia_do_ano[contador_2] < dp:
            af = 0
            auxiliar_contador = 0
            leg_af = '-'

        if dia_do_ano[contador_2] < de:
            af = 0
            auxiliar_contador = 0
            leg_af = '-'

        if dia_do_ano[contador_2] < dv8:
            af = 0
            auxiliar_contador = 0
            leg_af = '-'

        if dia_do_ano[contador_2] > dc:
            af = 0
            auxiliar_contador = 0
            leg_af = '-'

        if auxiliar_contador > 0:
            auxiliar_contador = auxiliar_contador - 1

        aplica_fungicida.append(af)
        aplica_fungicida_leg.append(leg_af)
        af = 0
        leg_af = '-'

    leg_fator_matriz = []

    for contador_2 in range(0, len(fator_acumulado)):

        if fator_acumulado[contador_2] == 0:
            leg_fator = '-'
        if (fator_acumulado[contador_2] > 0 and fator_acumulado[contador_2] <= 30):
            leg_fator = 'Baixo'
        if (fator_acumulado[contador_2] > 30 and fator_acumulado[contador_2] <= 60):
            leg_fator = 'Médio'
        if (fator_acumulado[contador_2] > 60):
            leg_fator = 'Alto'

        leg_fator_matriz.append(leg_fator)

    fa_matrix = np.reshape(fator_acumulado, (-1, 7))
    leg_fator_reshape = np.reshape(leg_fator_matriz, (-1,7))

    af_matrix = np.reshape(aplica_fungicida, (-1,7))
    aplica_fungicida_leg_reshape = np.reshape(aplica_fungicida_leg, (-1,7))

    dia_do_ano_str = []

    for item in dia_do_ano:
        h = datetime.datetime.strftime(item,'%d-%m')
        dia_do_ano_str.append(h)

    fa_dias_do_ano = np.reshape(dia_do_ano_str, (-1, 7))
    fa_dias_do_ano_1 = fa_dias_do_ano[:,[1]]

    dados_met_h = []


    for item in data_b:
        if (datetime.datetime.strptime(item['date'], '%Y-%m-%d') < data_fim_dados
                and datetime.datetime.strptime(item['date'], '%Y-%m-%d') >= dt_hoje):
            met_valores_h = {"date": None, "value": None, "dia": None, "dia_da_semana": None, "data_abreviada":None,}
            met_valores_h['date'] = item['date']
            met_valores_h['value'] = item['value']

            if item['value'] == 0:
                met_valores_h['dia'] = 0
            else: met_valores_h['dia'] = 1

            met_valores_h['dia_da_semana'] = int(datetime.datetime.strptime(item['date'], '%Y-%m-%d').strftime('%w'))
            met_valores_h['data_abreviada'] = datetime.datetime.strptime(item['date'], '%Y-%m-%d').strftime('%d-%m')
            dados_met_h.append(met_valores_h)

    # print(dados_met_h)

    tamanho = int(len(dados_met_h)/8)
    tempo_acumulada = [[0 for x in range(tamanho)] for y in range(8)]
    dia_acumulada = []
    hora_acumulada = [[0 for x in range(tamanho)] for y in range(8)]

    # print(tamanho)

    "tempo_acumulada = [[0 for x in range(8)] for y in range(tamanho)]"

    for contador_1 in range(0, tamanho):
        # print(contador_1 - 1)
        t0 = dados_met_h[contador_1*8]['value']
        t1 = dados_met_h[contador_1*8+1]['value']
        t2 = dados_met_h[contador_1*8+2]['value']
        t3 = dados_met_h[contador_1*8+3]['value']
        t4 = dados_met_h[contador_1*8+4]['value']
        t5 = dados_met_h[contador_1*8+5]['value']
        t6 = dados_met_h[contador_1*8+6]['value']
        t7 = dados_met_h[contador_1*8+7]['value']
        t8 = dados_met_h[contador_1*8]['data_abreviada']

        tempo_acumulada[0][contador_1] = t0
        tempo_acumulada[1][contador_1] = t1
        tempo_acumulada[2][contador_1] = t2
        tempo_acumulada[3][contador_1] = t3
        tempo_acumulada[4][contador_1] = t4
        tempo_acumulada[5][contador_1] = t5
        tempo_acumulada[6][contador_1] = t6
        tempo_acumulada[7][contador_1] = t7
        dia_acumulada.append(t8)

        hora_acumulada[0][contador_1] = '00:00'
        hora_acumulada[1][contador_1] = '03:00'
        hora_acumulada[2][contador_1] = '06:00'
        hora_acumulada[3][contador_1] = '09:00'
        hora_acumulada[4][contador_1] = '12:00'
        hora_acumulada[5][contador_1] = '15:00'
        hora_acumulada[6][contador_1] = '18:00'
        hora_acumulada[7][contador_1] = '21:00'

    tempo_acumulada_reshape = np.reshape(tempo_acumulada, (8, -1))
    hora_acumulada_reshape = np.reshape(hora_acumulada, (8, -1))

    a_est = np.array([[0, 15, 25, 35, 45, 55, 65, 75, 85, 91, 97, 103, 109, 128, 147, 155, 163], [0, 13, 23, 33, 43, 53, 63, 73, 83, 90, 97, 104, 111, 131, 151, 160, 169], [0, 11, 21, 31, 42, 53, 64, 75, 86, 92, 98, 104, 110, 130, 150, 159, 168], [0, 10, 20, 30, 41, 52, 63, 74, 85, 91, 97, 103, 109, 129, 149, 159, 169], [0, 10, 20, 30, 41, 52, 63, 74, 85, 90, 95, 100, 105, 125, 145, 156, 167], [0, 9, 19, 29, 39, 49, 59, 69, 79, 84, 89, 94, 99, 120, 141, 151, 161], [0, 8, 18, 28, 38, 48, 58, 68, 78, 83, 88, 93, 98, 120, 142, 152, 162], [0, 8, 18, 28, 37, 46, 55, 64, 73, 77, 81, 85, 89, 112, 135, 143, 151], [0, 7, 17, 27, 36, 45, 54, 63, 72, 76, 80, 84, 88, 112, 136, 143, 150], [0,7,17,27,35,43,51,59,67,71,75,79,83,107,131,136,141]])
    b_est = np.array(['01/10/2019', '11/10/2019', '21/10/2019', '01/11/2019', '11/11/2019', '21/11/2019', '01/12/2019', '11/12/2019', '21/12/2019', '31/12/2019'])
    c_est = np.array([['S', 'E', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'COL']])
    d_est = np.array(['S', 'E', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'COL'])



    lista_dias = []

    for contador_1 in range(0, len(b_est)):
        t = b_est[contador_1]
        delta = datetime.datetime.strptime(t, '%d/%m/%Y')  - dt_hoje #datetime.datetime.strptime(dt_hoje, '%Y/%m/%d')
        delta_valor = abs(delta.days)
        lista_dias.append(delta_valor)


    pos_dia = posicao(lista_dias,0)
    pos_estad_0 = np.where(c_est == estadio)
    pos_estad = pos_estad_0[1]

    delta_data = datetime.datetime.strptime(dia_do_plantio, '%Y-%m-%d') - dt_hoje
    delta_days = abs(delta_data.days)


    fator = delta_days/a_est[pos_dia][pos_estad]
    ajustada = a_est[pos_dia] * fator

    datas_final = []

    for contador_1 in range(0, len(ajustada)):
        z = datetime.datetime.strptime(dia_do_plantio, '%Y-%m-%d') + datetime.timedelta(days=ajustada[contador_1])
        y = z.strftime('%d-%m')
        datas_final.append(y)

    datas_tabela = np.asarray(datas_final)
    tabela_final = np.stack((d_est, datas_tabela))

    tabela_final_1 = tabela_final[0:2,0:8].copy()
    tabela_final_2 = tabela_final[0:2,8:16].copy()

    tabela_final_3 = np.vstack((tabela_final_1, tabela_final_2))


# OBTENDO A DIREção do Vento

    api_dir_1 = "https://projeta.cptec.inpe.br/api/v1/public/ETA/1/DAILY/2/12/2019/12/2019/D10M/" + latitude + "/" + longitude + "/"
    api_dir_2 = "https://projeta.cptec.inpe.br/api/v1/public/ETA/1/DAILY/2/1/2020/6/2020/D10M/" + latitude + "/" + longitude + "/"

    with urllib.request.urlopen(api_dir_1) as url:
        data_dir_1 = json.loads(url.read().decode())

    with urllib.request.urlopen(api_dir_2) as url:
        data_dir_2 = json.loads(url.read().decode())

    data_dir_0 = data_dir_1 + data_dir_2

    # OBTENDO A VELOCIDADE do Vento

    api_vel_1 = "https://projeta.cptec.inpe.br/api/v1/public/ETA/1/DAILY/2/12/2019/12/2019/W10M/" + latitude + "/" + longitude + "/"
    api_vel_2 = "https://projeta.cptec.inpe.br/api/v1/public/ETA/1/DAILY/2/1/2020/6/2020/W10M/" + latitude + "/" + longitude + "/"

    with urllib.request.urlopen(api_vel_1) as url:
        data_vel_1 = json.loads(url.read().decode())

    with urllib.request.urlopen(api_vel_2) as url:
        data_vel_2 = json.loads(url.read().decode())

    data_vel_0 = data_vel_1 + data_vel_2

    # DECIFRA O JSON RECEBIDO #

    dados_dir = []
    dados_dir_valores = []
    dias_passados = []
    cont = 0

    for item in data_dir_0:
        if (datetime.datetime.strptime(item['date'], '%Y-%m-%d') < data_fim_dados
                and datetime.datetime.strptime(item['date'], '%Y-%m-%d') > data_inicio_dados):
            met_valores = {"date": None, "value": None, "dia": None, "dia_da_semana": None,}
            met_valores['date'] = item['date']
            met_valores['value'] = item['value']
            a = item['value']
            cont = cont + 1

            dados_dir.append(met_valores)
            dados_dir_valores.append(a)
            dias_passados.append(cont)


    dados_vel = []
    dados_vel_valores = []

    for item in data_vel_0:
        if (datetime.datetime.strptime(item['date'], '%Y-%m-%d') < data_fim_dados
               and datetime.datetime.strptime(item['date'], '%Y-%m-%d') > data_inicio_dados):
            met_valores = {"date": None, "value": None, "dia": None, "dia_da_semana": None,}
            met_valores['date'] = item['date']
            met_valores['value'] = item['value']
            a = item['value']

            dados_vel.append(met_valores)
            dados_vel_valores.append(a)


    r = dados_vel_valores
    theta = dados_dir_valores
    area = 40 * np.pi #np.power(r,2)
    colors = np.power(dias_passados, 2)

    #fig, ((ax0, ax1, ax2), (ax3, ax4,ax5)) = plt.subplots(nrows=3, ncols=2,gridspec_kw={'height_ratios': [1, 1,3]})
    fig, ((ax0,ax3),(ax1,ax4),(ax2,ax5)) = plt.subplots(nrows=3, ncols=2,gridspec_kw={'height_ratios': [1, 1,3]})
    fig.subplots_adjust(hspace=0.9, wspace=-1.0)

    #GRÁFICO 1 - INDICE DE SEVERIDADE

    c = ax0.pcolor(fa_matrix, cmap='cool',edgecolors='white', linewidths=2)



    data_labels_x = ["D", "S", "T", "Q",
                     "Q", "S", "S"]


    for y in range(fa_matrix.shape[0]):
        for x in range(fa_matrix.shape[1]):
            ax0.text(x + 0.5, y + 0.5, '%s' % leg_fator_reshape[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize='8')
            ax0.text(x + 0.2, y + 0.2, '%s' % fa_dias_do_ano[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize='6')
            ax0.text(x + 0.8, y + 0.8, '%.2f' % fa_matrix[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize='6')

    ax0.axes.invert_yaxis()
    ax0.set_xticklabels(np.arange(len(data_labels_x)))
    ax0.set_title('Índice de Severidade da Ferrugem Asiática', fontsize='10',fontweight='bold')
    ax0.set_yticklabels('')
    ax0.set_xticklabels('')
    ax0.set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5],      minor=True)
    ax0.set_xticklabels(['Dom','Seg','Ter','Qua','Qui','Sex','Sab'], minor=True)

    #GRÁFICO 2 - DIAS DE NECESSIDADE DE APLICAçÃO de FUNGICIDA

    c = ax1.pcolor(af_matrix, cmap='Wistia',edgecolors='white', linewidths=2)

    if dia_aparecimento_esporo == '2099-11-21':
        dia_aparecimento_esporo = '-'

    titulo_ax1 = 'Aparecimento do primeiro esporo em ' + dia_aparecimento_esporo

    for y in range(af_matrix.shape[0]):
        for x in range(af_matrix.shape[1]):
            ax1.text(x + 0.5, y + 0.5, '%s' % aplica_fungicida_leg_reshape[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize='8')
            ax1.text(x + 0.08, y + 0.08, '%s' % fa_dias_do_ano[y, x],
                     horizontalalignment='left',
                     verticalalignment='top',
                     fontsize='5')

    ax1.axes.invert_yaxis()
    ax1.set_xticklabels(np.arange(len(data_labels_x)))
    ax1.set_xticklabels('')
    ax1.set_yticklabels('')
    ax1.set_title(titulo_ax1, fontsize='10',fontweight='bold')
    ax1.set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5],      minor=True)
    ax1.set_xticklabels(['Dom','Seg','Ter','Qua','Qui','Sex','Sab'], minor=True)

    # GRÁFICO 3 - MELHOR HORARIO PARA APLICACAO

    c = ax2.pcolor(tempo_acumulada, cmap='YlGn',edgecolors='white', linewidths=2)

    for y in range(tempo_acumulada_reshape.shape[0]):
        for x in range(tempo_acumulada_reshape.shape[1]):
            ax2.text(x + 0.60, y + 0.55, '%.2f' % tempo_acumulada_reshape[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize='8')
            ax2.text(x + 0.2, y + 0.2, '%s' % hora_acumulada_reshape[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize='5.5',style = 'italic')


    ax2.axes.invert_yaxis()
    ax2.set_yticklabels('')
    ax2.set_xticklabels('')
    ax2.set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5],      minor=True)
    ax2.set_xticklabels(dia_acumulada, minor=True)
    ax2.set_title('Precipitação para Aplicação de Fungicida [mm]', fontsize='10',fontweight='bold')

    table = ax3.table(cellText = tabela_final_3, loc='center',colWidths=16*[0.02], cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(6,0.5)
    ax3.set_title('Previsão de Estádio para o plantio. Estádio Atual: ' + estadio, fontsize='10',fontweight='bold')
    ax3.axis('off')

    table = ax4.table(cellText = diagnostico_visual, loc='center',colWidths=2*[0.2], cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(2,0.4)
    ax4.set_title('Avaliação visual de outras doenças na plantação', fontsize='10',fontweight='bold')
    ax4.axis('off')

    ax5.axis('off')
    ax5.set_title('Medição de Atividade de Vento, últimos 30 dias', fontsize='10',fontweight='bold')
    ax5 = fig.add_subplot(326, projection='polar')
    c = ax5.scatter(theta, r, c=colors, s=area, cmap='YlGnBu', alpha=0.75)
    ax5.set_ylabel('Radius', rotation=45, size=2)
    #ax5.set_xlabel(size=4)


    fig.tight_layout()


    plt.savefig('matriz.png', dpi=400, format='png')
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    plt.show()



