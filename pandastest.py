import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.DataFrame(dict(
    x = [1, 3, 2, 4],
    y = [1, 2, 3, 4],
    z = [2,4,5,6]
))
fig = px.line(df, x="x", y=['y','z'], title="Unsorted Input")
fig.show()
#context = {'chart': fig.to_html(full_html=False)}
