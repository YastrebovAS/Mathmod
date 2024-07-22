from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import questions,topic,results,User, Activity
from datetime import datetime

def control_id(request, control_id):
    request.session['restest'] = None

    title = topic.objects.filter(id = control_id)[0]
    ctrl_list = questions.objects.filter(topic_test=control_id)
    current_user = User.objects.get(id=request.user.id)


    ques_array = []
    multiple_answers_confirmation = []
    for c in ctrl_list:

        number_of_correct_answers = 0
        for answer in c.get_answers():
            if answer['is_correct'] == True:
                number_of_correct_answers +=1
        multiple_answers_confirmation.append(number_of_correct_answers)
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
        'answers': ques_array,
        'number_of_correct_answers':multiple_answers_confirmation
    }
    if request.method == 'POST':
        restest = []
        correct_answers = []
        actual_answers = []
        max_points = 0
        actual_points = 0

        for el in ctrl_list:
            max_points += el.marks
            if el.question in request.POST.keys():
                actual_answers.append(request.POST.getlist(el.question))


        for answerset in ques_array:
            correct_answers_for_one_question= []
            for answer in answerset:
                if answer['is_correct'] == True:
                    correct_answers_for_one_question.append(answer['answer'])
            correct_answers.append(correct_answers_for_one_question)


        for j in range(len(actual_answers)):
            points_for_question = 0
            for r in range(len(actual_answers[j])):
                if actual_answers[j][r] in correct_answers[j]:
                    points_for_question += ctrl_list[j].marks/len(correct_answers[j])
                else:
                    points_for_question -= ctrl_list[j].marks / len(correct_answers[j])
            if points_for_question < 0:
                points_for_question = 0
            elif points_for_question.is_integer():
                points_for_question = int(str(points_for_question).split(".")[0])

            actual_points += points_for_question

            temp = (ctrl_list[j].question,actual_answers[j],points_for_question,ctrl_list[j].marks)
            restest.append(temp)



        grade = float(actual_points/max_points)*100

        current_user = User.objects.get(id = request.user.id)

        newres = results(theme = title, student = current_user, grade = grade)
        #newres.save()
        request.session['restest'] = restest
        newactivity = Activity(user=current_user, datetime=datetime.now(),
                               activity=f'Прошел тест темы "{title.title}"(Баллы:{actual_points}/{max_points})')

        #newactivity.save()
        return redirect('control:testresult', control_id = control_id)
    else:
        newactivity = Activity(user=current_user, datetime=datetime.now(), activity= f'Посетил тест темы "{title.title}"')
        #newactivity.save()


    return  render(request,'control/control.html',context)

def result(request, control_id):
    return render(request, 'control/result.html')