from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from apps.accountusers.views import LoginView, LogoutView, RegisterView, EmailSentView, ActivationView, NewUserRegistrationAPI
from apps.registrations.views import ProspectiveUserList, ProspectiveUserDetail


urlpatterns = [
    # Examples:
    # url(r'^$', 'project_name.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^summernote/', include('django_summernote.urls')),
    
    # Pesapal processing url
    url(r'^payments/', include('django_pesapal.urls')),
    
    #url(r'^$', TemplateView.as_view(template_name='homepage.html')),
    
    url(r'^', include('jm_lms.apps.homesite.urls', namespace='home')), # Directing root url to a different app
    url(r'^dashboard/', include('jm_lms.apps.dashboard.urls')),
    url(r'^course/', include('jm_lms.apps.courses.urls')),
    url(r'^exercise/', include('jm_lms.apps.exercises.urls')),
    url(r'^purchase/', include('jm_lms.apps.purchase.urls', namespace='purchase')),
    url(r'^askaquestion/', include('jm_lms.apps.askaquestion.urls', namespace='askaquestion')),
    
    # user authentication and registration
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^registration_email_sent\.html', EmailSentView.as_view(), name='confirmation_mail_sent'),
    url(r'^user_activation\.html', ActivationView.as_view(), name='activation'),
    url(r'^terms_and_conditions\.html', TemplateView.as_view(template_name='terms_conditions.html')),
    
    # Quiz links
    url(r'^quiz/', include('jm_lms.apps.quiz.urls')),
    
    # REST API for new signups
    url(r'^pusers/', ProspectiveUserList.as_view()),
    url(r'^pusers/(?P<pk>[0-9]+)/$', ProspectiveUserDetail.as_view()),
    url(r'^newreg/', NewUserRegistrationAPI.as_view()),

    url(r'^admin/', include(admin.site.urls)),
]
