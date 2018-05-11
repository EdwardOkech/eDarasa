from django.conf.urls import patterns, url

from .views import (home_page)


urlpatterns = patterns('',
    url(r'^$', home_page, name='homepage'),
)
