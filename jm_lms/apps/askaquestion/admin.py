from django.contrib import admin
from .models import QuestionAsked


class QuestionAskedAdmin(admin.ModelAdmin):
    list_display = ('title','sender', 'lesson', 'sent_at', 'replied_at')




admin.site.register(QuestionAsked, QuestionAskedAdmin)
# admin.site.register(QuestionAnswer)


