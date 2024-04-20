import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly as plt

def func(request):
    context = {}
    if request.method == 'POST':
        dict_of_post = dict(request._post)
        r = float(dict_of_post['reactivity'][0])
        beta = float(dict_of_post['beta'][0])
        step = float(dict_of_post['step'][0])
        lambd = float(dict_of_post['lambda'][0])
        l = float(dict_of_post['average_lifetime'][0])
        Colunms1 = ['Время', 'Аналитика', 'Р-К метод', 'к1', 'к2', 'к3', 'к4', 'dN', 'Соотн', 'm1', 'm2', 'm3', 'm4',
                   'dC']
        Colunms2 = ['Время', 'Первое сл.','Второе сл.','Сумма']
        time, analytics, PK, k1, k2, k3, k4, dN, sootn, m1, m2, m3, m4, dC,  = [], [], [], [], [], [], [], [], [], [],\
                                                                               [], [], [], []
        first_sl, second_sl, summ = [],[],[]
        for i in range(0, 99):
            time.append(step * i)
            if i == 0:
                analytics.append(1)
                sootn.append(1)
                PK.append(1)
            else:
                analytics.append((1 / (1 - r)) * np.exp(lambd * r * time[i] / (1 - r)) - (r / (1 - r)) * np.exp(
                    (-1 / l) * beta * (1 - r) * time[i]))
                PK.append(PK[i - 1] + dN[i - 1])
                sootn.append(sootn[i - 1] + dC[i - 1])
            m1.append(lambd * (PK[i] - sootn[i]) * step)
            k1.append(((1 / l) * (beta * (r - 1)) * PK[i] + (beta / l) * sootn[i]) * step)
            m2.append(lambd * ((PK[i] + k1[i] / 2) - (sootn[i] + m1[i] / 2)) * step)
            k2.append(((1 / l) * (beta * (r - 1)) * (PK[i] + k1[i] / 2) + (beta / l) * (sootn[i] + m1[i] / 2)) * step)
            m3.append(lambd * ((PK[i] + k2[i] / 2) - (sootn[i] + m2[i] / 2)) * step)
            k3.append(((1 / l) * (beta * (r - 1)) * (PK[i] + k2[i] / 2) + (beta / l) * (sootn[i] + m2[i] / 2)) * step)
            m4.append(lambd * ((PK[i] + k3[i]) - (sootn[i] + m3[i])) * step)
            k4.append(((1 / l) * (beta * (r - 1)) * (PK[i] + k3[i]) + (beta / l) * (sootn[i] + m3[i])) * step)
            dN.append((k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6)
            dC.append((m1[i] + 2 * m2[i] + 2 * m3[i] + m4[i]) / 6)

        for i in range(1,99):
            first_sl.append((1 / (1 - r)) * np.exp(lambd * r * time[i] / (1 - r)))
            second_sl.append(-(r / (1 - r)) * np.exp((-1 / l) * beta * (1 - r) * time[i]))
            summ.append((1 / (1 - r)) * np.exp(lambd * r * time[i] / (1 - r)) - (r / (1 - r)) * np.exp(
                    (-1 / l) * beta * (1 - r) * time[i]))

        numbers1 = [time, analytics, PK, k1, k2, k3, k4, dN, sootn, m1, m2, m3, m4, dC]
        numbers2= [time[1:],first_sl,second_sl,summ]
        dat1= {}
        dat2 = {}
        for i in range(0, 14):
            dat1[Colunms1[i]] = numbers1[i]
        for i in range(0, 4):
            dat2[Colunms2[i]] = numbers2[i]
        df1 = pd.DataFrame(dat1)

        df2 = pd.DataFrame(dat2)
        json_records = df1.reset_index().to_json(orient='records')
        data1 = json.loads(json_records)
        fig1 = px.line(df1, x='Время', y=['Аналитика', 'Р-К метод'], title="Положительный скачок реактивности")
        graph1 = plt.offline.plot(fig1, auto_open=False, output_type="div")
        json_records = df2.reset_index().to_json(orient='records')
        data2 = json.loads(json_records)
        fig2 = px.line(df2, x='Время', y=['Первое сл.','Второе сл.','Сумма'], title="Слагаемые аналитического решения")
        graph2 = plt.offline.plot(fig2, auto_open=False, output_type="div")
        context = {'d1': data1, 'k1': Colunms1, 'graph1': graph1, 'd2': data2, 'k2': Colunms2, 'graph2': graph2 }
    return context