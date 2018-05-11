from django.conf.urls import patterns, url

from .views import (LipaNaMpesaView,
                    process_payment,
                    process_payment_feedback)


urlpatterns = patterns('',
    url(r'^payment/$', LipaNaMpesaView.as_view(), name='payment'),
    url(r'^process_payment/$', process_payment, name='process_payment'),
    url(r'^payment_feedback/$', process_payment_feedback, name='process_payment_feedback'),
)
