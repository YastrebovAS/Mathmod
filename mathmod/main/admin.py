from django.contrib import admin

from django.contrib import admin

from .models import *

admin.site.register(topic)
admin.site.register(practices)
admin.site.register(Answer)
admin.site.register(questions)
admin.site.register(User)
admin.site.register(results)
admin.site.register(changelogs)
admin.site.register(PracticeReport)
admin.site.register(Activity)
admin.site.register(Session, SessionAdmin)

