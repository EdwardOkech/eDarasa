from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from django_summernote.admin import SummernoteModelAdmin

from jm_lms.apps.quiz.models import Quiz
from .models import Course, Module, Lesson, Example, CourseEnrollment, LessonQuestion, StudentLessonProgress


# We apply summernote to all TextField in model.

class ModuleInline(admin.TabularInline):
    model = Module
    
    
class CourseAdmin(SummernoteModelAdmin):
    list_display = ('id', 'name', 'prerequisite', 'position_order')
    list_filter = ('name',)
    search_fields = ('name',)
    
    inlines = [
        ModuleInline,
    ]

admin.site.register(Course, CourseAdmin)


class ModuleAdmin(SummernoteModelAdmin):
    list_display = ('id', 'name', 'course', 'prerequisite', 'status', 'position')
    list_filter = ('course__name',)
    
admin.site.register(Module, ModuleAdmin)


# class ModuleWrapAdmin(SummernoteModelAdmin):
#     list_display = ('description', 'previous_module', 'next_module')
#
# admin.site.register(ModuleWrap, ModuleWrapAdmin)


class ExampleInline(admin.TabularInline):
    model = Example
    
    
class LessonAdminForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """

    class Meta:
        model = Lesson
        exclude = []
        
    quizzes = forms.ModelMultipleChoiceField(
        queryset=Quiz.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Quizzes',
            is_stacked=False))
            
    def __init__(self, *args, **kwargs):
        super(LessonAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['quizzes'].initial = self.instance.get_quizzes()
                
    def save(self, commit=True):
        lesson = super(LessonAdminForm, self).save(commit=False)
        lesson.save()
        lesson.quizzes_set = self.cleaned_data['quizzes']
        self.save_m2m()
        return lesson
        
        
class LessonAdmin(SummernoteModelAdmin):
    form = LessonAdminForm
    
    list_display = ('id', 'name', 'module', 'course', 'prerequisite', 'position')
    list_filter = ('module__course__name',)
    inlines = [
        ExampleInline,
    ]
    
admin.site.register(Lesson, LessonAdmin)


class LessonQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lesson')
    
admin.site.register(LessonQuestion, LessonQuestionAdmin)


class ExampleAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title', 'lesson')
    
admin.site.register(Example, ExampleAdmin)


class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course')
    list_filter = ('course', )
    search_fields = ('student__username', 'student__email', 'course__name')

admin.site.register(CourseEnrollment, CourseEnrollmentAdmin)


class StudentLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'lesson', 'status', 'done_percent')
    def has_add_permission(self, request):
        return False
        
admin.site.register(StudentLessonProgress, StudentLessonProgressAdmin)
