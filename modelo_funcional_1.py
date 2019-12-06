# CONTACTA O PROJETA < ApI do CpTEC PARA OBTER INFOS #

# FUNCIONA!

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
dia_do_v8 = '2020-01-15'
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


########################################


with urllib.request.urlopen(api_1) as url:
    data_1 = json.loads(url.read().decode())

with urllib.request.urlopen(api_2) as url:
    data_2 = json.loads(url.read().decode())

    data = data_1 + data_2

#https://projeta.cptec.inpe.br/api/v1/public/ETA/1/DAILY/2/10/2019/3/2020/PREC/#
#https://projeta.cptec.inpe.br/api/v1/public/ETA/1/DAILY/2/10/2019/12/2019/EVTP/-13.40/-46.09/#
#CORRENTINA >> "https://projeta.cptec.inpe.br/api/v1/public/ETA/2/DAILY/2/10/2019/12/2019/PREC/-13.40/-46.09/"

#"https://projeta.cptec.inpe.br/api/v1/public/ETA/2/DAILY/2/11/2019/12/2019/PREC/-13.40/-46.09/"
#"https://projeta.cptec.inpe.br/api/v1/public/ETA/2/DAILY/2/1/2020/4/2020/PREC/-13.40/-46.09/"

    # DECIFRA O JSON RECEBIDO #
    dados_met = []
    for item in data:
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
    auxiliar_contador = 0
    af = 0

    for contador_2 in range(0, len(fator_acumulado)):

        if fator_acumulado[contador_2] > 60 and auxiliar_contador == 0 and dia_do_ano[contador_2] >= desp:
            af = 100
            auxiliar_contador = 15

        if dia_do_ano[contador_2] < dp:
            af = 0
            auxiliar_contador = 0

        if dia_do_ano[contador_2] < de:
            af = 0
            auxiliar_contador = 0

        if dia_do_ano[contador_2] < dv8:
            af = 0
            auxiliar_contador = 0

        if dia_do_ano[contador_2] > dc:
            af = 0
            auxiliar_contador = 0

        if auxiliar_contador > 0:
            auxiliar_contador = auxiliar_contador - 1

        aplica_fungicida.append(af)
        af = 0

    fa_matrix = np.reshape(fator_acumulado, (-1, 7))
    af_matrix = np.reshape(aplica_fungicida, (-1,7))

    dia_do_ano_str = []

    for item in dia_do_ano:
        h = datetime.datetime.strftime(item,'%Y-%m-%d')
        dia_do_ano_str.append(h)

    fa_dias_do_ano = np.reshape(dia_do_ano_str, (-1, 7))
    fa_dias_do_ano_1 = fa_dias_do_ano[:,[1]]


    plt.subplot(2,1,1)

    data = fa_matrix
    heatmap = plt.pcolor(data)
    data_labels_x = ["D", "S", "T", "Q",
              "Q", "S", "S"]

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text(x + 0.5, y + 0.5, '%.2f' % data[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize='8')



    plt.colorbar(heatmap)
    heatmap.axes.set_title('Índice de Severidade da Ferrugem Asiática (Acima de 60 indica um índice alto)')
    heatmap.axes.set_yticks(np.arange(len(fa_dias_do_ano_1)))
    heatmap.axes.set_yticklabels(fa_dias_do_ano_1)
    heatmap.axes.invert_yaxis()
    heatmap.axes.set_xticks(np.arange(len(data_labels_x)))
    heatmap.axes.set_xticklabels(data_labels_x)
    plt.setp(heatmap.axes.get_xticklabels(), rotation=0, ha="center", rotation_mode="anchor")


    plt.subplot(2,1,2)
    data = af_matrix
    heatmap = plt.pcolor(data)
    data_labels_x = ["D", "S", "T", "Q",
              "Q", "S", "S"]

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text(x + 0.5, y + 0.5, '%.2f' % data[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize='8')


    plt.colorbar(heatmap)
    heatmap.axes.set_title('Dias de Aplicação do Fungicida (Onde for igual a 100 = Aplicação)')
    heatmap.axes.set_yticks(np.arange(len(fa_dias_do_ano_1)))
    heatmap.axes.set_yticklabels(fa_dias_do_ano_1)
    heatmap.axes.invert_yaxis()
    heatmap.axes.set_xticks(np.arange(len(data_labels_x)))
    heatmap.axes.set_xticklabels(data_labels_x)
    plt.setp(heatmap.axes.get_xticklabels(), rotation=0, ha="center", rotation_mode="anchor")


    plt.show()

