from django.contrib import admin

from .models import *

# Тут происходит настройка  панели администритора
# В ней зарегистрирована каждая модель из main/models.py
# В list_display указаны поля, которые будут отображаться в панели при просмотре соответствующей таблицы


@admin.register(topic)
class topicAdmin(admin.ModelAdmin):
    list_display = ("title","theory")

@admin.register(practices)
class practicesAdmin(admin.ModelAdmin):
    list_display = ("topic_prac", "practice")

@admin.register(questions)
class questionsAdmin(admin.ModelAdmin):
    list_display = ("question","topic_test","marks")
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("answer","question","is_correct")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name","patronymic","role")

@admin.register(results)
class resultsAdmin(admin.ModelAdmin):
    list_display = ("theme", "student","grade")

@admin.register(PracticeReport)
class PracticeReportAdmin(admin.ModelAdmin):
    list_display = ("practice_title","student", "date")

    def practice_title(self,obj): # небольшая функция, чтобы практика показывалась именно как тема, а не как practices_object
        title = practices.objects.filter(id = obj.practice.id)[0].topic_prac
        return title

    practice_title.short_description = "Тема практики"

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'activity')

