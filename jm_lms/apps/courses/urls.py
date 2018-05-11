from django.conf.urls import patterns, url

from .views import  (CourseListView, 
                    CourseDetailView, 
                    ModuleListView, 
                    ModuleDetailView, 
                    LessonCreateView, 
                    LessonDetailView,
                    EnrolUserTemplateView)


def course_url(path):
    return r'^(?P<course_slug>[-\w\d]+){}'.format(path)
    
def module_url(path):
    return course_url(r'/(?P<module_slug>[-\w\d]+){}'.format(path))
    
def lesson_url(path):
    return module_url(r'/(?P<lesson_slug>[-\w\d]+){}'.format(path))

urlpatterns = patterns('',
    url(r'^$', CourseListView.as_view(), name='course_list'),
    url(course_url('/$'), CourseDetailView.as_view(), name='course_detail'),
    url(r'^module/$', ModuleListView.as_view(), name='module_list'),
    url(module_url('/$'), ModuleDetailView.as_view(), name='module_detail'),
    url(module_url('/lesson/create$'), LessonCreateView.as_view(), name='lesson_create'),
    url(module_url('/(?P<lesson_slug>[-\w\d]+)$'), LessonDetailView.as_view(), name='lesson_detail'),
    url(r'^enrol/(?P<userid>\d+)/(?P<courseid>\d+)/$', EnrolUserTemplateView.as_view(), name='enrol_to_course'),
)
