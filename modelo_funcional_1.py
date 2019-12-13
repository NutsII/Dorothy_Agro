# CONTACTA O PROJETA API do CpTEC PARA OBTER INFOS #

from typing import List

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import urllib.request, json
import numpy as np
import datetime


###### DEFINIR OS PARÂMETROS DA RODADA ####

dia_do_plantio = '2019-11-21'
dia_da_emergencia = '2019-12-01'
dia_do_v8 = '2019-01-15'
dia_da_colheita = '2020-03-30'
dia_aparecimento_esporo = '2019-11-21'

latitude = '-13.40'
longitude = '-46.09'

########################################


dp = datetime.datetime.strptime(dia_do_plantio, '%Y-%m-%d')
de = datetime.datetime.strptime(dia_da_emergencia, '%Y-%m-%d')
dv8 = datetime.datetime.strptime(dia_do_v8, '%Y-%m-%d')
dc = datetime.datetime.strptime(dia_da_colheita, '%Y-%m-%d')
desp = datetime.datetime.strptime(dia_aparecimento_esporo, '%Y-%m-%d')

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

    data_fim_dados = datetime.datetime.now() + datetime.timedelta(days=7)
    data_inicio_dados = datetime.datetime.now() + datetime.timedelta(days=-30)

    # DECIFRA O JSON RECEBIDO #
    dados_met = []

    for item in data:
        if (datetime.datetime.strptime(item['date'], '%Y-%m-%d') < data_fim_dados
                and datetime.datetime.strptime(item['date'], '%Y-%m-%d') > data_inicio_dados):
            met_valores = {"date": None, "value": None, "dia": None, "dia_da_semana": None,}
            met_valores['date'] = item['date']
            met_valores['value'] = item['value']

            if item['value'] == 0:
                met_valores['dia'] = 0
            else: met_valores['dia'] = 1

            met_valores['dia_da_semana'] = int(datetime.datetime.strptime(item['date'], '%Y-%m-%d').strftime('%w'))

            dados_met.append(met_valores)


    # OBTEM A PRECIPITACAO DOS ULTIMOS 30 DIAS #

    print(dados_met)

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

    print(type(dia_do_ano))


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
                and datetime.datetime.strptime(item['date'], '%Y-%m-%d') > datetime.datetime.now()):
            met_valores_h = {"date": None, "value": None, "dia": None, "dia_da_semana": None, "data_abreviada":None,}
            met_valores_h['date'] = item['date']
            met_valores_h['value'] = item['value']

            if item['value'] == 0:
                met_valores_h['dia'] = 0
            else: met_valores_h['dia'] = 1

            met_valores_h['dia_da_semana'] = int(datetime.datetime.strptime(item['date'], '%Y-%m-%d').strftime('%w'))
            met_valores_h['data_abreviada'] = datetime.datetime.strptime(item['date'], '%Y-%m-%d').strftime('%d-%m')
            dados_met_h.append(met_valores_h)

    print(dados_met_h)

    tamanho = int(len(dados_met_h)/8)
    tempo_acumulada = [[0 for x in range(tamanho)] for y in range(8)]
    dia_acumulada = []
    hora_acumulada = [[0 for x in range(tamanho)] for y in range(8)]

    print(tamanho)

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



    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1,gridspec_kw={'height_ratios': [1, 1,3]})
    fig.subplots_adjust(hspace=0.9)


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

    fig.tight_layout()

    plt.show()



