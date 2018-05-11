from django.forms import ModelForm
from .models import QuestionAsked


class AskQuestionForm(ModelForm):
    class Meta:
        model = QuestionAsked
        fields = ['title', 'body', 'lesson']
