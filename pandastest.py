import pandas as pd
import numpy as np
from openpyxl import Workbook
import openpyxl
from scipy.optimize import fsolve
import os
import matplotlib.pyplot as plt
import plotly.express as px
d = 200
h = 700/2
M = 1/61

def f(x):
    return M*(1/np.tan(x*h))-x*np.tanh(d*M)



x = fsolve(f,0.00000001)

print(x)

rbmk = [0.004734,0.004684,0.004634,0.004584,0.004534,0.004484,0.004434,0.004384,0.004334,0.004284,0.004234,0.004184,0.004134,
        0.004084,0.004034,0.003984,0.003934,0.003884,0.003834,0.003784,0.003734,0.003684,0.003634,0.003584,0.003534,0.003484,0.003434]
