from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _, ugettext_lazy

class HomeRegistrationForm(forms.Form):
    EDUCATION_LEVEL_OPTIONS = (
                ("1", "Just completed secondary school"),
                ("2", "Waiting to join university/college"),
                ("3", "Undertaking a certificate/diploma"),
                ("4", "Degree first year"),
                ("5", "Degree second year"),
                ("6", "Degree third year"),
                ("7", "Degree fourth year"),
                ("8", "Degree fifth + year"),
                ("9", "Graduate with certificate/diploma/degree"),
                ("10", "Currently undertaking a masters")
              )
              
    JOB_STATUS_OPTIONS = (
                ("1", "Currently unemployed and looking for an internship"),
                ("2", "Currently unemployed and looking for a job"),
                ("3", "Currently on my (1st, 2nd, 3rd) internship"),
                ("4", "Currently working a temporary/contract job"),
                ("5", "Currently working a permanent job with less than 2 years experience"),
                ("6", "Currently working a permanent job with 2 + years of experience")
              )
                
    full_names = forms.CharField(label='Your Full Name', max_length=150)
    phone_number = forms.CharField(label='Your Phone Number')
    education_level = forms.ChoiceField(widget=forms.Select, choices=EDUCATION_LEVEL_OPTIONS)
    job_status = forms.ChoiceField(widget=forms.Select, choices=JOB_STATUS_OPTIONS)
    username = forms.CharField(label=_('Your Username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=50)), label=_('Your Email Address'))
    email2 = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=50)), label=_("Email address (again)"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=40, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=40, render_value=False)), label=_("Password (again)"))
 
    
    def __init__(self, *args, **kwargs):
        super(HomeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['job_status'].initial = 'Current job status'
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_("The email already exists. Please try another one."), code='invalid')
        return email
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError(_("The username already exists. Please try another one."), code='invalid')
        return username
        
    def clean(self):
        # Check Passwords match
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."), code='invalid')
        
        # Check Emails match
        if 'email' in self.cleaned_data and 'email2' in self.cleaned_data:
            if self.cleaned_data['email'] != self.cleaned_data['email2']:
                raise forms.ValidationError(_("The two email fields did not match."), code='invalid')
                
        return self.cleaned_data


class ContactForm(forms.Form):
    names = forms.CharField(max_length=200)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=50)
    comments = forms.Textarea()