from django import forms
from .models import TableExerciseQuestion


class TableExerciseQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = TableExerciseQuestion
        # exclude = ('exercise',)
        exclude = ('expected_answer',)

    def __init__(self, *args, **kwargs):
        super(TableExerciseQuestionAdminForm, self).__init__(*args, **kwargs)
        # self.fields['num_of_expected_entries']= forms.IntegerField(label='num_of_expected_entries')
        self.fields['table_header']= forms.CharField(label='table_header')
        self.fields['num_of_expected_entries']= forms.IntegerField(label='num_of_expected_entries')




