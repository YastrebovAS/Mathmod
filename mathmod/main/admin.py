from django.contrib import admin

from django.contrib import admin

from .models import topic,practices,Answer,questions,User,results,changelogs

admin.site.register(topic)
admin.site.register(practices)
admin.site.register(Answer)
admin.site.register(questions)
admin.site.register(User)
admin.site.register(results)
admin.site.register(changelogs)

