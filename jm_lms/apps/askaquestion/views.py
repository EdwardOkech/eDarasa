from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from jm_lms.apps.courses.models import Lesson
from .forms import AskQuestionForm
from .models import QuestionAsked


def process_question_asked(request):
    if request.method == 'POST':
        askquestion_form = AskQuestionForm(request.POST, prefix='askquestion')
        if askquestion_form.is_valid():
            lesson = Lesson.objects.get(pk=askquestion_form.cleaned_data['lesson'].pk)
            question_asked = QuestionAsked(
                                title = askquestion_form.cleaned_data['title'],
                                body = askquestion_form.cleaned_data['body'],
                                sender = request.user,
                                lesson = lesson
                                )
            question_asked.save()
            return HttpResponseRedirect(reverse("learn_lesson", args=[lesson.module.course.slug, lesson.module.slug, lesson.slug]))
    return HttpResponseRedirect(reverse("student_dashboard"))
    
    
class QuestionAskedListView(ListView):

    model = QuestionAsked
    context_object_name = 'questions_asked'
    template_name = 'askaquestion/askedquestions_list.html'
    
    """def get_context_data(self, **kwargs):
        context = super(QuestionAskedListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context"""
        
    def get_queryset(self):
        return QuestionAsked.objects.filter(sender=self.request.user)
        
        
class QuestionAskedDetailView(DetailView):

    model = QuestionAsked
    context_object_name = 'question_asked'
    template_name = 'askaquestion/askedquestion_detail.html'

    """def get_context_data(self, **kwargs):
        context = super(QuestionAskedDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context"""
        
