from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly as plt
# Create your views here.


def index(request):
    return HttpResponse("<h1>Страница практики</h1>")

def ksenon(request):
    context = {}
    if request.method == 'POST':
        dict_of_post = dict(request._post)
        sigmax = float(dict_of_post['sigmax'][0])
        sigmaf = float(dict_of_post['sigmaf'][0])
        alpha = float(dict_of_post['alpha'][0])
        nf = float(dict_of_post['neutron_flow'][0])/10
        lambdai = 0.1008
        lambdax = 0.0758
        xinf = 0.06*sigmaf/sigmax
        i0 = sigmax*alpha*nf/lambdai
        x0 = sigmax*alpha*nf/(lambdax+sigmax*alpha*nf)
        zapas = 0.9364
        sigm_by_nf = nf*sigmax
        step = 0.5
        Colunms1 = ['Время', 'Йод', 'Ксенон']
        Colunms2 = ['Время', 'alf=0.5','alf=0.6','alf=0.7','alf=0.8','alf=0.9','alf=1']
        time,iod,xenon = [], [], []
        alf_05, alf_06,alf_07,alf_08,alf_09,alf_1 = [], [], [], [], [], []
        for i in range(0, 62):
            time.append(step * i)
            iod.append(i0*np.exp(-lambdai*time[i]))
            xenon.append(lambdai*i0*(np.exp(-lambdai*time[i])-np.exp(-lambdax*time[i]))/(lambdax-lambdai)+x0*np.exp(-lambdax*time[i]))
            alf_05.append(lambdai * i0 * (np.exp(-lambdai * time[i]) - np.exp(-lambdax * time[i])) / (
                        lambdax - lambdai) + x0 * np.exp(-lambdax * time[i]))
            alf_06.append(sigmax*(alpha+0.1)*nf*(np.exp(-lambdai*time[i])-np.exp(-lambdax*time[i]))/(lambdax-lambdai)+sigmax*(alpha+0.1)*nf/(lambdax+sigmax*(alpha+0.1)*nf)*np.exp(-lambdax*time[i]))
            alf_07.append(sigmax*(alpha+0.2)*nf*(np.exp(-lambdai*time[i])-np.exp(-lambdax*time[i]))/(lambdax-lambdai)+sigmax*(alpha+0.2)*nf/(lambdax+sigmax*(alpha+0.2)*nf)*np.exp(-lambdax*time[i]))
            alf_08.append(sigmax * (alpha + 0.3) * nf * (np.exp(-lambdai * time[i]) - np.exp(-lambdax * time[i])) / (
                        lambdax - lambdai) + sigmax * (alpha + 0.3) * nf / (
                                      lambdax + sigmax * (alpha + 0.3) * nf) * np.exp(-lambdax * time[i]))
            alf_09.append(sigmax * (alpha + 0.4) * nf * (np.exp(-lambdai * time[i]) - np.exp(-lambdax * time[i])) / (
                        lambdax - lambdai) + sigmax * (alpha + 0.4) * nf / (
                                      lambdax + sigmax * (alpha + 0.4) * nf) * np.exp(-lambdax * time[i]))
            alf_1.append(sigmax * (alpha + 0.5) * nf * (np.exp(-lambdai * time[i]) - np.exp(-lambdax * time[i])) / (
                        lambdax - lambdai) + sigmax * (alpha + 0.5) * nf / (
                                      lambdax + sigmax * (alpha + 0.5) * nf) * np.exp(-lambdax * time[i]))
        numbers1 = [time,iod,xenon]
        numbers2 = [time, alf_05, alf_06,alf_07,alf_08,alf_09,alf_1]
        dat1 = {}
        dat2 = {}
        for i in range(0, 3):
            dat1[Colunms1[i]] = numbers1[i]
        for i in range(0, 7):
            dat2[Colunms2[i]] = numbers2[i]
        df1 = pd.DataFrame(dat1)
        df2 = pd.DataFrame(dat2)
        json_records = df1.reset_index().to_json(orient='records')
        data1 = json.loads(json_records)
        fig1 = px.line(df1, x='Время', y=['Йод', 'Ксенон'], title="Концентрации йода и ксенона при полной остановке с 50% уровня мощности")
        graph1 = plt.offline.plot(fig1, auto_open=False, output_type="div")
        json_records = df2.reset_index().to_json(orient='records')
        data2 = json.loads(json_records)
        fig2 = px.line(df2, x='Время', y=['alf=0.5','alf=0.6','alf=0.7','alf=0.8','alf=0.9','alf=1'],
                       title="Йодная яма при остановке с различного уровня мощности")
        graph2 = plt.offline.plot(fig2, auto_open=False, output_type="div")
        context = {'d1': data1, 'k1': Colunms1, 'graph1': graph1, 'd2': data2, 'k2': Colunms2, 'graph2': graph2}
    return render(request, 'main/ksenon_practice.html',context)

def dot_kinetic(request):
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
    return render(request,'main/dot_kinetic_practice.html', context)


def ksenon(request):
    context = {}
    if request.method == 'POST':
        dict_of_post = dict(request._post)
        sigmax = float(dict_of_post['sigmax'][0])
        sigmaf = float(dict_of_post['sigmaf'][0])
        alpha = float(dict_of_post['alpha'][0])
        nf = float(dict_of_post['neutron_flow'][0])/10
        lambdai = 0.1008
        lambdax = 0.0758
        xinf = 0.06*sigmaf/sigmax
        i0 = sigmax*alpha*nf/lambdai
        x0 = sigmax*alpha*nf/(lambdax+sigmax*alpha*nf)
        zapas = 0.9364
        sigm_by_nf = nf*sigmax
        step = 0.5
        Colunms1 = ['Время', 'Йод', 'Ксенон']
        Colunms2 = ['Время', 'alf=0.5','alf=0.6','alf=0.7','alf=0.8','alf=0.9','alf=1']
        time,iod,xenon = [], [], []
        alf_05, alf_06,alf_07,alf_08,alf_09,alf_1 = [], [], [], [], [], []
        for i in range(0, 62):
            time.append(step * i)
            iod.append(i0*np.exp(-lambdai*time[i]))
            xenon.append(lambdai*i0*(np.exp(-lambdai*time[i])-np.exp(-lambdax*time[i]))/(lambdax-lambdai)+x0*np.exp(-lambdax*time[i]))
            alf_05.append(lambdai * i0 * (np.exp(-lambdai * time[i]) - np.exp(-lambdax * time[i])) / (
                        lambdax - lambdai) + x0 * np.exp(-lambdax * time[i]))
            alf_06.append(sigmax*(alpha+0.1)*nf*(np.exp(-lambdai*time[i])-np.exp(-lambdax*time[i]))/(lambdax-lambdai)+sigmax*(alpha+0.1)*nf/(lambdax+sigmax*(alpha+0.1)*nf)*np.exp(-lambdax*time[i]))
            alf_07.append(sigmax*(alpha+0.2)*nf*(np.exp(-lambdai*time[i])-np.exp(-lambdax*time[i]))/(lambdax-lambdai)+sigmax*(alpha+0.2)*nf/(lambdax+sigmax*(alpha+0.2)*nf)*np.exp(-lambdax*time[i]))
            alf_08.append(sigmax * (alpha + 0.3) * nf * (np.exp(-lambdai * time[i]) - np.exp(-lambdax * time[i])) / (
                        lambdax - lambdai) + sigmax * (alpha + 0.3) * nf / (
                                      lambdax + sigmax * (alpha + 0.3) * nf) * np.exp(-lambdax * time[i]))
            alf_09.append(sigmax * (alpha + 0.4) * nf * (np.exp(-lambdai * time[i]) - np.exp(-lambdax * time[i])) / (
                        lambdax - lambdai) + sigmax * (alpha + 0.4) * nf / (
                                      lambdax + sigmax * (alpha + 0.4) * nf) * np.exp(-lambdax * time[i]))
            alf_1.append(sigmax * (alpha + 0.5) * nf * (np.exp(-lambdai * time[i]) - np.exp(-lambdax * time[i])) / (
                        lambdax - lambdai) + sigmax * (alpha + 0.5) * nf / (
                                      lambdax + sigmax * (alpha + 0.5) * nf) * np.exp(-lambdax * time[i]))
        numbers1 = [time,iod,xenon]
        numbers2 = [time, alf_05, alf_06,alf_07,alf_08,alf_09,alf_1]
        dat1 = {}
        dat2 = {}
        for i in range(0, 3):
            dat1[Colunms1[i]] = numbers1[i]
        for i in range(0, 7):
            dat2[Colunms2[i]] = numbers2[i]
        df1 = pd.DataFrame(dat1)
        df2 = pd.DataFrame(dat2)
        json_records = df1.reset_index().to_json(orient='records')
        data1 = json.loads(json_records)
        fig1 = px.line(df1, x='Время', y=['Йод', 'Ксенон'], title="Концентрации йода и ксенона при полной остановке с 50% уровня мощности")
        graph1 = plt.offline.plot(fig1, auto_open=False, output_type="div")
        json_records = df2.reset_index().to_json(orient='records')
        data2 = json.loads(json_records)
        fig2 = px.line(df2, x='Время', y=['alf=0.5','alf=0.6','alf=0.7','alf=0.8','alf=0.9','alf=1'],
                       title="Йодная яма при остановке с различного уровня мощности")
        graph2 = plt.offline.plot(fig2, auto_open=False, output_type="div")
        context = {'d1': data1, 'k1': Colunms1, 'graph1': graph1, 'd2': data2, 'k2': Colunms2, 'graph2': graph2}
    return render(request, 'main/ksenon_practice.html',context)