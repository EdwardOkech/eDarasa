from django import forms

from .models import LessonQuestion

class LessonQuestionForm(forms.ModelForm):

    class Meta:
        model = LessonQuestion
        fields = ('title', 'description',)
