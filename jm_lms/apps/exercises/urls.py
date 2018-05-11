from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^exercise_submit/(?P<lesson_id>[0-9]+)/(?P<exercise_id>[0-9]+)/$', views.lesson_exercise_posted, name='exercise_submit'),
]
