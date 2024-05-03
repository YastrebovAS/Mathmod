import pandas as pd
import xlwings as xw
import plotly.express as px
import plotly as plt


path = 'Точечная кинетика_стандартизация.xlsx'
wb = xw.Book(path)
wks = xw.sheets


input_sheet = wks['Входные данные']
inputs = []

input_name = input_sheet.range('A1')
number_of_inputs=1
while input_name.value != None:
    number_of_inputs += 1
    input_name = input_sheet.range(f'A{number_of_inputs}')
    input_val = input_sheet.range(f'B{number_of_inputs}')
    count_after_decimal = str(input_val.value)[::-1].find('.')
    input_measurement = input_sheet.range(f'C{number_of_inputs}')
    input_min = input_sheet.range(f'D{number_of_inputs}')
    input_max = input_sheet.range(f'E{number_of_inputs}')
    print(input_val.address)
    if input_name.value != None:
        inputs.append(
            (input_name.value, input_val.value, input_measurement.value, 1 / 10 ** count_after_decimal, input_min.value,
             input_max.value))

calculation = wks['Расчеты']
names = []
tables = []


row = calculation.range('A1')
k=0
empty_row_counter = 0
while empty_row_counter !=1:
    row = calculation[k, 0]
    if calculation[k, 1].value == None:
        names.append(k)
    if row.value == None:
        empty_row_counter += 1
    k +=1

prev_rows = 1
for m in range(0,len(names)-1):
    upper_border = names[m]
    lower_border = names[m+1]
    name = calculation[upper_border,0].value
    last_column = 0
    while True:
        if calculation[upper_border+1,last_column].value is not None:
            last_column += 1
        else:
            break
    table_dataframe = pd.read_excel(path, sheet_name='Расчеты', skiprows = prev_rows, nrows = lower_border-2,
                                    usecols=[x for x in range(0,last_column)])
    tables.append((name,table_dataframe,list(table_dataframe.columns)))
    prev_rows += lower_border

results = wks['Результат']
variables = []
graph_info = []
graphs = []


result_var_counter = 0
while True:
    if results[result_var_counter, 0].value is not None:
        result_var_counter += 1
    else:
        break
for n in range(1, result_var_counter):
    variables.append((results[n, 0].value,results[n, 1].value,results[n, 2].value))

result_graph_counter = 0
while True:
    if results[result_graph_counter, 6].value is not None:
        #print(results[result_graph_counter, 6].value)
        result_graph_counter += 1
    else:
        break
prev_graph = 1
y_axis = []
for b in range(1,result_graph_counter):
    if results[b,4].value is not None:
        name = results[b,4].value
        x_axis = calculation[f'{results[b,5].value}'].value
        y_axis.append(calculation[f'{results[b, 6].value}'].value)
        graph_info.append((name,x_axis,y_axis))
        y_axis = []
    else:
        y_axis.append(calculation[f'{results[b, 6].value}'].value)

for graph in graph_info:
    x_line = graph[1]
    y_graphs = graph[2]
    data = {
        x_line[0]:x_line[1:]
    }
    for each in y_graphs:
        data[each[0]] = each[1:]

    graph_dataframe = pd.DataFrame(data)
    figure = px.line(graph_dataframe, x=x_line[0], y=[each[0] for each in y_graphs],
                   title=graph[0])
    actual_graph = plt.offline.plot(figure, auto_open=False, output_type="div")
    graphs.append(actual_graph)

context = {'input':inputs, 'tables': tables, 'outputs': variables, 'graphs':graphs}

