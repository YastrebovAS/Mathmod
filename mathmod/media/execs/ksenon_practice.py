import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly as plt

def func(request):
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
    return context