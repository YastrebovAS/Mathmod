from django.contrib import admin

from django.contrib import admin

from .models import topic,practices,options,questions,User,results,changelogs

admin.site.register(topic)
admin.site.register(practices)
admin.site.register(options)
admin.site.register(questions)
admin.site.register(User)
admin.site.register(results)
admin.site.register(changelogs)

