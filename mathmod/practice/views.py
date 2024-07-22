from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from main.models import *

import pandas as pd
import xlwings
import openpyxl
import plotly.express as px
import plotly as plt
import json
import importlib
import os
from datetime import datetime


def return_cell_range(range): # на вход идет массив объектов-клеток excel, выходит массив значений в этих клетках
    return [cell[0].value for cell in range]

def practice_display(request,practice_id):

    current_user = User.objects.get(id=request.user.id)
    title = practices.objects.select_related('topic_prac').get(id = practice_id).topic_prac.title


    current_practice = practices.objects.get(id=practice_id)
    path = current_practice.practice
    extension = str(path).split(".")[-1] #расширение файла
    temp_name = str(path)[6:-4] #имя практики
    tempfile = "media/" + str(request.user) + "_" + temp_name + extension # собирается имя временного файла
    #print(tempfile)


    tables = []


    variables = []
    macro_results = []
    graphs = []
    #print(extension)
    if extension == "xlsm": #параметры открытия файля меняются взависимости от того, есть макросы или нет
        starter_wb = openpyxl.load_workbook(path, read_only=False, keep_vba=True)

    else:
        starter_wb = openpyxl.load_workbook(path)


    input_sheet = starter_wb['Входные данные']

    inputs = []

    input_name = input_sheet['A1']
    number_of_inputs = 1
    while input_name.value != None:
        number_of_inputs += 1
        input_name = input_sheet.cell(row=number_of_inputs, column=1)
        input_type = input_sheet.cell(row=number_of_inputs, column=2).value
        input_val = input_sheet.cell(row=number_of_inputs, column=3).value
        input_measurement = input_sheet.cell(row=number_of_inputs, column=4).value
        input_step = input_sheet.cell(row=number_of_inputs, column=5).value
        input_min = input_sheet.cell(row=number_of_inputs, column=6).value
        input_max = input_sheet.cell(row=number_of_inputs, column=7).value
        address = input_sheet.cell(row=number_of_inputs, column=3).coordinate
        if input_type == 'выбор':
            input_measurement = input_measurement.split(",")
        elif input_type == 'массив':
            input_val = return_cell_range(input_sheet[input_val])

        if input_name.value != None:
            inputs.append([input_name.value, input_val, input_measurement, input_step,
                           input_min, input_max, address, input_type])

    starter_tables_sheet = starter_wb['Начальные таблицы']

    start_tables = []
    starter_names = []

    f = 1
    starter_tables_empty_row_counter = 0
    while starter_tables_empty_row_counter != 1:
        calc_row = starter_tables_sheet.cell(row=f, column=1)
        if starter_tables_sheet.cell(row=f, column=2).value == None:
            starter_names.append(f)
        if calc_row.value == None:
            starter_tables_empty_row_counter += 1
        f += 1


    starter_prev_rows = 1
    for w in range(0, len(starter_names) - 1):
        upper_border = starter_names[w]
        lower_border = starter_names[w + 1]
        name = starter_tables_sheet.cell(row=upper_border, column=1).value

        last_column = 0
        while True:
            if starter_tables_sheet.cell(row=upper_border + 1, column=last_column + 1).value is not None:
                last_column += 1

            else:
                break
        # print(starter_prev_rows, lower_border)
        table_dataframe = pd.read_excel('media/'+ str(path), sheet_name='Начальные таблицы', skiprows=starter_prev_rows,
                                        nrows=lower_border - upper_border - 2,
                                        usecols=[x for x in range(0, last_column)])
        # print(table_dataframe)
        json_records = table_dataframe.reset_index().to_json(orient='records')
        data2 = json.loads(json_records)
        start_tables.append((name, data2, list(table_dataframe.columns)))
        starter_prev_rows = lower_border

    if request.method =='POST':

        for v in range(0,len(inputs)):
            if inputs[v][7] == 'массив':
                array_range = input_sheet[inputs[v][6]].value
                values_to_be_replaced = list(input_sheet[array_range])
                for q in range(len(values_to_be_replaced)):
                    values_to_be_replaced[q][0].value = request.POST.getlist(inputs[v][0])[q]
                inputs[v][1] = request.POST.getlist(inputs[v][0])
            else:
                input_sheet[inputs[v][6]].value = request.POST[inputs[v][0]].replace(".",",")
                inputs[v][1] = request.POST[inputs[v][0]]

        
        starter_wb.save(tempfile)

        macros = []
        excel_app = xlwings.App(visible=False)
        excel_book = excel_app.books.open(tempfile)
        res = excel_book.sheets['Результат']
        macro_counter = 1
        while True:
            if res[macro_counter, 10].value is not None:
                macros.append(res[macro_counter, 10].value)
                #print(res[macro_counter, 10].value)
                macro_counter += 1
            else:
                break
        #print(macro_counter - 1)
        for macro in macros:
            current_macro = excel_book.macro(macro)
            current_macro()
        excel_book.save()
        excel_book.close()
        excel_app.quit()

        actual_wb = openpyxl.load_workbook(tempfile,data_only=True)
        calculation_sheet = actual_wb['Расчеты']
        results = actual_wb['Результат']
        names = []
        tables = []

        macro_results = []
        variables = []
        graph_info = []
        graphs = []

        k = 1
        empty_row_counter = 0
        while empty_row_counter != 1:
            calc_row = calculation_sheet.cell(row=k, column=1)
            if calculation_sheet.cell(row=k, column=2).value == None:
                names.append(k)
            if calc_row.value == None:
                empty_row_counter += 1
            k += 1
        #print(names)

        prev_rows = 1
        for m in range(0, len(names) - 1):
            upper_border = names[m]
            lower_border = names[m + 1]
            name = calculation_sheet.cell(row=upper_border, column=1).value

            last_column = 0
            while True:
                if calculation_sheet.cell(row=upper_border + 1, column=last_column + 1).value is not None:
                    last_column += 1

                else:
                    break
            #print(prev_rows, lower_border)
            table_dataframe = pd.read_excel(tempfile, sheet_name='Расчеты', skiprows=prev_rows,
                                            nrows=lower_border-upper_border-2,
                                            usecols=[x for x in range(0, last_column)])
            #print(table_dataframe)
            json_records = table_dataframe.reset_index().to_json(orient='records')
            data1 = json.loads(json_records)
            tables.append((name, data1, list(table_dataframe.columns)))
            prev_rows = lower_border

        for d in range(2, macro_counter+1):
            macro_results.append((results.cell(row=d, column=10).value, results.cell(row=d, column=12).value,
                                  results.cell(row=d, column=13).value))
        result_var_counter = 1
        while True:
            if results.cell(row=result_var_counter, column=1).value is not None:
                result_var_counter += 1
            else:
                break
        #print(result_var_counter-2)
        for n in range(2, result_var_counter):
            variables.append((results.cell(row=n, column=1).value, results.cell(row=n, column=3).value,
                              results.cell(row=n, column=4).value))
        #print(variables)

        result_graph_counter = 1
        while True:
            if results.cell(row=result_graph_counter, column=8).value is not None:
                # print(results[result_graph_counter, 6].value)
                result_graph_counter += 1
            else:
                break
        #print(result_graph_counter)

        prev_graph = 1
        y_axis = []
        for b in range(2, result_graph_counter):
            if results.cell(row=b, column=6).value is not None:
                name = results.cell(row=b, column=6).value
                x_axis = return_cell_range(calculation_sheet[results.cell(row=b, column=7).value])
                y_axis.append(return_cell_range(calculation_sheet[results.cell(row=b, column=8).value]))
                graph_info.append((name, x_axis, y_axis))
                #print(y_axis)
                y_axis = []
            else:
                y_axis.append(return_cell_range(calculation_sheet[results.cell(row=b, column=8).value]))

        for graph in graph_info:
            x_line = graph[1]
            y_graphs = graph[2]
            #print(y_graphs)
            data = {
                x_line[0]: x_line[1:]
            }
            for each in y_graphs:
                data[each[0]] = each[1:]
            graph_dataframe = pd.DataFrame(data)
            figure = px.line(graph_dataframe, x=x_line[0], y=[each[0] for each in y_graphs],
                             title=graph[0])
            actual_graph = plt.offline.plot(figure, auto_open=False, output_type="div")
            graphs.append(actual_graph)
        os.remove(tempfile)


    context = {'starter_tables':start_tables,
                'inputs': inputs,
               'tables': tables,
               'outputs': variables,
               'graphs': graphs,
               "macros": macro_results}


    if request.POST.getlist("testing_mode[]") == ['non_testing']:
        report = render_to_string("main/practice.html", context=context) + ""
        new_prac_report = PracticeReport(student=current_user, practice=current_practice, report=report,
                                         date=datetime.now())
        new_prac_report.save()

        newactivity = Activity(user=current_user, datetime=datetime.now(), activity=f'Получил отчет по практике темы "{title}"')
        newactivity.save()
    else:
        newactivity = Activity(user=current_user, datetime=datetime.now(), activity=f'Посетил практику темы "{title}"')
        newactivity.save()



    return render(request, 'practice/practice.html', context)