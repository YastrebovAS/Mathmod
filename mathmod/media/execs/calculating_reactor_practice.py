import pandas as pd
import json
import plotly.express as px
import plotly as plt
import re

def func(request):
    vver = {"(NuF*SigmaF)t":[0.158041,0.160349,0.16154,0.161874,0.161527,0.160626,0.159268,0.157531,0.155476,0.153156,
                             0.150614,0.147886,0.145004,0.141994,0.13888,0.135683,0.132419,0.129105,0.125755,0.122382,
                             0.118998,0.115612,0.112234,0.108874,0.10554,0.10224,0.0989822,0.0957738,0.0926225,0.0895349,
                             0.0865182,0.0835795,0.0807249,0.0752053,0.0729702,0.0707626,0.0686037,0.066511,0.0644975,
                             0.0625744, 0, 0],
            "(Sigma_A)t":[0.0896994,0.0917619,0.0931467,0.0940008,0.0944272,0.0945021,0.0942846,0.0938219,0.0931525,
                          0.0923086,0.0913168,0.0902,0.0889777,0.0876664,0.086281,0.0848339,0.083336,0.0817976,0.0802272,
                          0.0786325,0.0770205,0.0753977,0.0737698,0.0721421,0.0705196,0.0689073,0.0673093,0.0657299,0.0641735,
                          0.0626437,0.0611445,0.0596798,0.0582529,0.0552849,0.0541828,0.053088,0.0520119,0.0509642,0.0499519,
                          0.0489814,1.364,0.005],
            "Dt":[0.369351,0.36848,0.367916,0.367591,0.367457,0.367481,0.367634,0.367897,0.368253,0.368687,0.369188,
                  0.369747,0.370355,0.371004,0.371689,0.372404,0.373144,0.373904,0.374682,0.375474,0.376276,0.377085,
                  0.3779,0.378716,0.379533,0.380347,0.381156,0.381959,0.382752,0.383535,0.384304,0.385058,0.385795
                  ,0.387301,0.387881,0.388457,0.389023,0.389576,0.390111,0.390625,0.390625,0.390625]}
    rbmk = {
        "(NuF*SigmaF)t": [0.00617621,0.00611414,0.00601823,0.00589667,0.00575519,0.00560616,0.00543391,0.00525316,
                          0.00506657,0.00487654,0.00468531,0.00449508,0.00430785,0.00412557,0.00395008,0.00378314,
                          0.00362634,0.00348108,0.00334846,0.00322924, 0, 0],
        "(Sigma_A)t": [0.00419722,0.00419515,0.00417541,0.0041422,0.00409848,0.00408019,0.00402109,0.00395716,0.00388978,
                       0.00382021,0.00374922,0.00367816,0.00360808,0.00353986,0.00347431,0.00341219,0.00335416,0.00330078,
                       0.0032525,0.00320958,0.314,0.005],
        "Dt": [0.779096,0.779105,0.779072,0.77901,0.778922,0.778892,0.778769,0.778634,0.778491,0.778343,0.77819,0.778037,
               0.777885,0.777736,0.777593,0.777457,0.777329,0.777211,0.777105,0.77701,0.77701,0.77701]}
    context = {}
    if request.method == 'POST':
        dict_of_post = dict(request._post)
        #print(dict_of_post)
        operation = str(dict_of_post['operation-type'][0])
        reactor = str(dict_of_post['reactor-type'][0])
        step = int(dict_of_post['step'][0])
        start_values = list(re.split(",",str(dict_of_post['start_val'][0])))
        start_values[0] =  start_values[0].replace('[','')
        start_values[-1] = start_values[-1].replace(']', '')
        Colunms1 = ['Начальные значения', 'Фи', "Загрузка", "(NuF*SigmaF)t", "(Sigma_A)t",	"Dt",
 'A', 'B', 'C', 'S1', 'alpha1', 'beta1', 'phi1', 'S2', 'alpha2', 'beta2', 'phi2']
        phi, loading, nufsigmaft, sigma_at, Dt, A, B, C, S1, alpha1, beta1, phi1, S2, alpha2, beta2, phi2,conclusion,m =\
            [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
        phi1 = [0] * 61
        phi2 = [0] * 61
        for i in range(0,61):  # Считывание начальных данных из реактора
            m.append(i)
            loading.append(1)
            if reactor == 'ВВЭР':
                nufsigmaft.append(vver['(NuF*SigmaF)t'][loading[i]-1])
                sigma_at.append(vver['(Sigma_A)t'][loading[i]-1])
                Dt.append(vver['Dt'][loading[i]-1])
            else:
                nufsigmaft.append(rbmk['(NuF*SigmaF)t'][loading[i]-1])
                sigma_at.append(rbmk['(Sigma_A)t'][loading[i]-1])
                Dt.append(rbmk['Dt'][loading[i]-1])
        for i in range(0,61): # Генерация A,B,C и обеих альф
            if i == 0:
                alpha1.append(0)
                alpha2.append(0)
                A.append(0)
                B.append(0)
                C.append(0)
            else:
                A.append((Dt[i - 1] + Dt[i]) / (2 * step * step))
                if i == 60:
                    B.append((2 * Dt[i] + Dt[i - 1]) / (2 * step * step) + sigma_at[i])
                    C.append((Dt[i]) / (2 * step * step))
                else:
                    B.append((Dt[i + 1] + 2 * Dt[i] + Dt[i - 1]) / (2 * step * step) + sigma_at[i])
                    C.append((Dt[i + 1] + Dt[i]) / (2 * step * step))
                alpha1.append(C[i] / (B[i] - A[i] * alpha1[i - 1]))
                alpha2.append(C[i] / (B[i] - A[i] * alpha1[i - 1]))
        for i in range(0, 61):
            if operation == 'Настройка':
                phi.append(int(start_values[i]))
                S1.append(phi[i] * nufsigmaft[loading[i] - 1])
            else:
                phi.append(phi1[i])
                S1.append(phi[i] * nufsigmaft[loading[i] - 1])
        dividor1 = sum(S1)
        S1 = [float(x / dividor1) for x in S1]
        for i in range(0, 61):
            if i == 0:
                beta1.append(0)
            else:
                beta1.append((A[i]*beta1[i-1]+S1[i])/(B[i]-A[i]*alpha1[i-1]))

        for i in range(0, 61):
            if i != 0 and i != 60:
                phi1[60-i] = (alpha1[60-i]*phi1[61-i]+beta1[60-i])



        for i in range(0, 61):
            S2.append(phi1[i] * nufsigmaft[loading[i] - 1])
        dividor2 = sum(S2)
        S2 = [float(x / dividor2) for x in S2]
        for i in range(0, 61):
            if i == 0:
                beta2.append(0)
            else:
                beta2.append((A[i]*beta2[i-1]+S2[i])/(B[i]-A[i]*alpha2[i-1]))
        for i in range(0, 61):
            if i != 0 and i != 60:
                phi2[60-i] = (alpha2[60-i]*phi2[61-i]+beta2[60-i])

        numbers1 = [start_values, phi, loading, nufsigmaft, sigma_at, Dt, A, B, C, S1, alpha1, beta1, phi1, S2,
                    alpha2, beta2, phi2]
        if operation == 'Настройка':
            conclusion = [0]*61
        else:
            for i in range(0,61):
                conclusion.append(phi1[i]/max(phi1))
        dat1 = {}
        dat2 = {'m': m,
                'Итог': conclusion,
                'Начало': [0]+[1]*59+[0]}
        for i in range(0, 17):
            dat1[Colunms1[i]] = numbers1[i]
        df1 = pd.DataFrame(dat1)
        df2 = pd.DataFrame(dat2)
        json_records = df1.reset_index().to_json(orient='records')
        data1 = json.loads(json_records)
        json_records = df2.reset_index().to_json(orient='records')
        data2 = json.loads(json_records)
        fig2 = px.line(df2, x='m', y=['Итог','Начало'])
        graph2 = plt.offline.plot(fig2, auto_open=False, output_type="div")
        context = {'d1': data1, 'k1': Colunms1, 'd2': data2, 'k2': ['m','Итог','Начало'], 'graph2': graph2}
    return context