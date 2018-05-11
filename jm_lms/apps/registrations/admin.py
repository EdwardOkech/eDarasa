from django.contrib import admin
from .models import ProspectiveUser


class ProspectiveUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_names', 'email', 'education', 'current_job','phone_number')
    search_fields = ('email', 'full_names')

admin.site.register(ProspectiveUser, ProspectiveUserAdmin)
