import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly as plt
from scipy.optimize import fsolve
def func(request):
    context = {}
    if request.method == 'POST':
        dict_of_post = dict(request._post)
        reactor = str(dict_of_post['reactor-type'][0])
        amount = int(dict_of_post['step'][0])
        if reactor == 'РБМК':
            H = 700
            maz = 20
            d = 200
            M = 61
            reac = [0.004734, 0.004684, 0.004634, 0.004584, 0.004534, 0.004484, 0.004434, 0.004384, 0.004334, 0.004284,
                    0.004234, 0.004184, 0.004134,
                    0.004084, 0.004034, 0.003984, 0.003934, 0.003884, 0.003834, 0.003784, 0.003734, 0.003684, 0.003634,
                    0.003584, 0.003534, 0.003484, 0.003434]
            lent = 50
        else:
            H = 355
            maz = 8
            d = 10
            M = 5.85
            reac = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.011,0.012,0.013,0.014,0.015,0.016,0.017,
                    0.018,0.019,0.02,0.021,0.022,0.023,0.024,0.001,0.001,0.001]
            lent = 100
        def f(x):
            return (1 / np.tan(x * H/2))/M - x * np.tanh(d / M)
        step = float(format(H/amount,".1f"))

        col2,col3,step_list,flow = [],[],[],[]
        context['startheaders'] = ['H,см','Маз,см','d,см','M,отр','Шаг']
        context['startdata'] = [H,maz,d,M,step]
        alpha = fsolve(f,0.00000001)
        alpha = float(alpha[0])
        for i in range(len(reac)):
            col2.append((1 / np.tan(reac[i] * H/2))/M)
            col3.append(reac[i] * np.tanh(d/M))
        for i in range(lent):
            if step*i<=(H/2)+d:
                step_list.append(step*i)
            else:
                step_list.append(0)
            if step_list[i]<H/2:
                flow.append(np.cos(alpha*step_list[i]))
            else:
                flow.append(np.cos(alpha*H/2)*(np.sinh((H/2+d-step_list[i])/M)/np.sinh(d/M)))
        dat1 = {'': reac, 'Ряд1': col2,'Ряд2': col3}
        dat2 = {'Шаг': step_list, 'Поток': flow}
        df1 = pd.DataFrame(dat1)
        json_records = df1.reset_index().to_json(orient='records')
        data1 = json.loads(json_records)
        fig1 = px.line(df1, x='', y=['Ряд1','Ряд2'], title="Приближенное графическое решение")
        graph1 = plt.offline.plot(fig1, auto_open=False, output_type="div")
        df2 = pd.DataFrame(dat2)
        json_records = df2.reset_index().to_json(orient='records')
        data2 = json.loads(json_records)
        fig2 = px.line(df2, x='Шаг', y= ['Поток'], title="Распределение плотности потока нейтронов")
        graph2 = plt.offline.plot(fig2, auto_open=False, output_type="div")
        context['d1'] = data1
        context['d2'] = data2
        context['k1'] = ['','Ряд1','Ряд2']
        context['graph1'] = graph1
        context['graph2'] = graph2
        context['resdata'] = [alpha, 1 ,1+(alpha**2)*(maz**2), 1 + (np.pi**2)*((maz/H)**2)]
    return context