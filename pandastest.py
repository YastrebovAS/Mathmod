import pandas as pd
import numpy as np
r = 0.036
beta = 0.0065
step = 0.05
lambd = 0.0773
l = 0.001
Colunms = ['Время', 'Аналитика', 'Р-К метод', 'к1', 'к2', 'к3', 'к4', 'dN', 'Соотн', 'm1', 'm2', 'm3', 'm4', 'dC']
time, analytics, PK,k1, k2, k3, k4, dN, sootn, m1, m2, m3, m4, dC = [],[],[],[],[],[],[],[],[],[],[],[],[],[]
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
    m1.append(lambd*(PK[i]-sootn[i])*step)
    k1.append(((1 / l) * (beta * (r - 1)) * PK[i] + (beta / l) * sootn[i]) * step)
    m2.append(lambd*((PK[i]+k1[i]/2)-(sootn[i]+m1[i]/2))*step)
    k2.append(((1 / l) * (beta * (r - 1)) * (PK[i] + k1[i] / 2) + (beta / l) * (sootn[i] + m1[i] / 2)) * step)
    m3.append(lambd*((PK[i]+k2[i]/2)-(sootn[i]+m2[i]/2))*step)
    k3.append(((1 / l) * (beta * (r - 1)) * (PK[i] + k2[i] / 2) + (beta / l) * (sootn[i] + m2[i] / 2)) * step)
    m4.append(lambd*((PK[i]+k3[i])-(sootn[i]+m3[i]))*step)
    k4.append(((1 / l) * (beta * (r - 1)) * (PK[i] + k3[i]) + (beta / l) * (sootn[i] + m3[i])) * step)
    dN.append((k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6)
    dC.append((m1[i] + 2 * m2[i] + 2 * m3[i] + m4[i]) / 6)

numbers = [time, analytics, PK,k1, k2, k3, k4, dN, sootn, m1, m2, m3, m4, dC]
data = {}
for i in range (0,14):
    data[Colunms[i]] = numbers[i]
df = pd.DataFrame(data)
