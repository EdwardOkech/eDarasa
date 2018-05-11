from django.contrib import admin

from .models import JobType, JobPost

class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

admin.site.register(JobType, JobTypeAdmin)


class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'posted_by', 'date_posted')
    list_filter = ('type',)
    search_fields = ('title',)

admin.site.register(JobPost, JobPostAdmin)
