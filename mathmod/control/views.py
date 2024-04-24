from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import questions,topic,results,User

def control_id(request, control_id):
    request.session['restest'] = None
    title = topic.objects.filter(id = control_id)[0]
    ctrl_list = questions.objects.filter(topic_test=control_id)
    ques_array = []
    for c in ctrl_list:
        ques_array.append(c.get_answers())

    if len(ctrl_list) == 0:
        context = {
            'title': 'Ошибка',
            'error': 'Вопросов по этой теме нет',

        }
        return render(request, 'main/fail.html', context)

    context = {
        'title': title.title,
        'questions': ctrl_list,
        'answers': ques_array
    }
    if request.method == 'POST':
        restest = []
        max_points = 0
        actual_points = 0
        for el in ctrl_list:
            max_points += el.marks
        correct_answers = []
        actual_answers = []

        for answerset in ques_array:
            #tempar = []
            for answer in answerset:
                if answer['is_correct'] == True:
                    correct_answers.append(answer['answer'])
            #correct_answers.append(tempar)

        for key,value in request.POST.items():
            actual_answers.append(value)
        actual_answers = actual_answers[1:]

        for j in range(len(correct_answers)):
            if actual_answers[j] == correct_answers[j]:
                actual_points += ctrl_list[j].marks
                temp = (ctrl_list[j].question,actual_answers[j],True)
            else:
                temp = (ctrl_list[j].question, actual_answers[j], False)
            restest.append(temp)


        grade = float(actual_points/max_points)*100

        current_user = User.objects.filter(id = request.user.id)[0]

        newres = results(theme = title, student = current_user, grade = grade)
        newres.save()
        request.session['restest'] = restest
        return redirect('control:testresult', control_id = control_id)



    return  render(request,'main/control.html',context)

def result(request, control_id):
    title = topic.objects.filter(id=control_id)[0]
    return render(request, 'main/result.html')