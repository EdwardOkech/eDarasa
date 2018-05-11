from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Exercise, Question, UserAnswer, MultiChoiceQuestion, MultiChoiceQuestionOption, EssayQuestion, EssayUserAnswer, ExerciseSubmission, TableExerciseQuestion, TableExerciseUserAnswer
from .forms import TableExerciseQuestionAdminForm


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    

class ExerciseSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'exercise', 'date')
    
    
class QuestionAdmin(SummernoteModelAdmin):
    list_display = ('title', 'exercise','forward',)
    list_editable = ['forward']

    

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'answer', 'answered_on', 'question')


# class TableExerciseQuestionAdmin(SummernoteModelAdmin):
#     list_display = ('title', 'exercise')




    
class MultiChoiceQuestionOptionInline(admin.TabularInline):
    model = MultiChoiceQuestionOption

    
class MultiChoiceQuestionAdmin(SummernoteModelAdmin):
    list_display = ('title', 'exercise', 'forward',)
    list_editable = ['forward']
    
    inlines = [MultiChoiceQuestionOptionInline]
    
    
class EssayQuestionAdmin(SummernoteModelAdmin):
    list_display = ('title', 'exercise','forward',)
    list_editable = ['forward']

    

class EssayUserAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'answered_on')


class TableExerciseQuestionAdmin(admin.ModelAdmin):
    form = TableExerciseQuestionAdminForm

    list_display = ('title', 'exercise', 'forward')
    list_editable = ['forward']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(TableExerciseQuestionAdmin, self).get_fieldsets(request, obj)
        # fieldsets[0][1]['fields'] += ['num_of_expected_entries']
        fieldsets[0][1]['fields'] += ['table_header']
        fieldsets[0][1]['fields'] += ['num_of_expected_entries']
        return fieldsets


class TableExerciseUserAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'answer', 'answered_on', 'question')


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseSubmission, ExerciseSubmissionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(MultiChoiceQuestion, MultiChoiceQuestionAdmin)
admin.site.register(EssayQuestion, EssayQuestionAdmin)
admin.site.register(EssayUserAnswer, EssayUserAnswerAdmin)
admin.site.register(TableExerciseQuestion, TableExerciseQuestionAdmin)
admin.site.register(TableExerciseUserAnswer, TableExerciseUserAnswerAdmin)
