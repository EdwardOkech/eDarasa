from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from jm_lms.apps.accountusers.views import send_custom_email
from .forms import HomeRegistrationForm


def home_page(request):
    """
    Displays and handles the home page
    """
    # Handling multiple forms
    # Ref: http://codereview.stackexchange.com/questions/2857/multiple-forms-in-django
    # Ref: http://stackoverflow.com/questions/5857363/using-multiple-forms-on-a-page-in-django
    # Ref: http://stackoverflow.com/questions/569468/django-multiple-models-in-one-template-using-forms
    # Ref: http://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django
    if request.method == 'POST':
        register_form = HomeRegistrationForm(request.POST, prefix="register")
        if register_form.is_valid():
            user = get_user_model().objects.create_user(
                                 first_name=register_form.cleaned_data['full_names'],
                                 username=register_form.cleaned_data['username'],
                                 email=register_form.cleaned_data['email'],
                                 password=register_form.cleaned_data['password'])
                                 
            # Send mail to new user
            send_custom_email(user)
            
            return HttpResponseRedirect(reverse("confirmation_mail_sent"))
    else:
        register_form = HomeRegistrationForm(prefix="register")
    return render(request, 'homesite/homepage.html', {
                            'register_form': register_form,
                        })


def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('names'):
            errors.append('Enter Full Names')
        if not request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid Email Address')
        if not request.POST.get('phone'):
            errors.append('Enter phone number')
        if not request.POST.get('comments'):
            errors.append('Enter Comments')
        if not errors:
            send_custom_email(
                request.POST['names'],
                request.POST.get('email', 'jobsmentor@gmail.com'),
                ['jobsmentor@gmail.com'],
                request.POST['phone'],
                request.POST['comments'],
            )
            return HttpResponseRedirect(reverse("confirmation_mail_sent"))
        return render(request, 'homesite/homepage.html', {
            'errors': errors,
            'names': request.POST.get('names', ''),
            'email': request.POST.get('email', ''),
            'phone': request.POST.get('phone', ''),
            'comments': request.POST.get('comments', ''),
        })