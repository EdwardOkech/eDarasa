from django.conf.urls import patterns, url

from .views import (process_question_asked,
                    QuestionAskedListView,
                    QuestionAskedDetailView)


urlpatterns = patterns('',
    url(r'^process_questionasked/$', process_question_asked, name='process_questionasked'),
    url(r'^askedquestions/$', QuestionAskedListView.as_view(), name='askedquestions_list'),
    url(r'^(?P<slug>[-\w\d]+)/$', QuestionAskedDetailView.as_view(), name='askedquestion_detail'),
)
