from django.conf.urls import patterns, url

from jm_lms.apps.courses.views import LessonQuestionCreateView
from .views import (DashboardView, 
                    EmployerDashboardView, 
                    StudentDashboardView,
                    StudentDashboardCourseView,
                    StudentDashboardModuleView,
                    StudentDashboardLessonView,
                    StudentLearnLessonView,
                    StudentDashboardLessonQuestionsView,                    
                    StudentWelcomeView,
                    HowItWorksView)


def learner_url(path):
    return r'^learner{}'.format(path)
    
def learner_course_url(path):
    return learner_url(r'/course/(?P<course_slug>[-\w\d]+){}'.format(path))
    
def learner_lesson_url(path):
    return learner_course_url(r'/(?P<module_slug>[-\w\d]+)/(?P<lesson_slug>[-\w\d]+){}'.format(path))

urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^employer/$', EmployerDashboardView.as_view(), name='employer_dashboard'),
    url(learner_url('/$'), StudentDashboardView.as_view(), name='student_dashboard'),
    url(learner_url('/welcome$'), StudentWelcomeView.as_view(), name='first_user_welcome'),
    url(learner_url('/courses$'), StudentDashboardCourseView.as_view(), name='student_courses'),
    url(learner_course_url('/$'), StudentDashboardModuleView.as_view(), name='student_modules'),
    url(learner_course_url('/(?P<module_slug>[-\w\d]+)/$'), StudentDashboardLessonView.as_view(), name='student_lessons'),
    url(learner_course_url('/(?P<module_slug>[-\w\d]+)/(?P<lesson_slug>[-\w\d]+)/$'), StudentLearnLessonView.as_view(), name='learn_lesson'),
    url(learner_lesson_url('/lesson_question/new/$'), LessonQuestionCreateView.as_view(), name='lesson_question_new'),
    url(learner_url('/lesson_questions/$'), StudentDashboardLessonQuestionsView.as_view(), name='student_lesson_questions'),
    url(r'^howitworks\.html', HowItWorksView.as_view(), name='howitworks'),
    
)
