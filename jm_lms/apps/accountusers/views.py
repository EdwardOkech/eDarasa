from datetime import date, datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import UpdateView
from django.views.generic.base import RedirectView, TemplateView        
from django.views.generic.edit import FormView         
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.contrib.sites.models import Site
from django.shortcuts import render
from django.template import loader, Context

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from jm_lms.apps.purchase.models import Purchase       
from .forms import LoginForm, UserRegistrationForm
from .models import AuthUser, Registration
from .serializer import NewUserRegistrationSerializer


def is_employer(user):
    return user.groups.filter(name='Employer').exists()
    
def is_student(user):
    return user.groups.filter(name='Student').exists()
    
def is_in_multiple_groups(user):
    """ Check that a user belongs both in the Employer and Student group """
    return user.groups.filter(name__in=['Employer', 'Student']).exists()


class LoginView(FormView):
     
    template_name = 'users/login.html'
    form_class = LoginForm
    
    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return "%s" % (next_url)
        else:
            if is_employer(self.request.user):
                return reverse('employer_dashboard')
            elif is_student(self.request.user):
            
                # Users that join/register the site after this date are required to pay. 
                # Previous users who joined earlier will however not be required to pay.
                payment_activation_date = datetime.strptime('May 1 2016  12:00AM', '%b %d %Y %I:%M%p')                
                
                if self.request.user.date_joined.replace(tzinfo=None) >= payment_activation_date:
                    # For users who registered AFTER the payment activation date
                    print("User registered later")
                    
                    # Has the student paid for training?
                    try:
                        purchased = Purchase.objects.get( purchaser=self.request.user )
                        
                        # Is this a first time user
                        if date.today() == self.request.user.date_joined.date():
                            return reverse('first_user_welcome')
                        else:
                            #return reverse('payment')
                            return reverse('student_dashboard')
                    except Purchase.DoesNotExist:
                        return reverse('purchase:payment')                    
                    
                else: 
                    # For users who registered BEFORE the payment activation date
                    print("User registered earlier")
                    return reverse('student_dashboard')
                
                              
            else:
                return reverse('dashboard')
   
    """def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                if user.last_login is None:
                else:
                    login(self.request, user)
        return super(LoginView, self).form_valid(form)
        
        super(LoginView, self).form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                if not user.banned:
                    return super(Login, self).form_valid(form)
                else:
                    return redirect(reverse('ban-page'))
            else:
                form.errors['non_field_errors'] = ['Your account is not active.']
                return render(self.request, 'index.html', {'form': form})
        else:
            form.errors['non_field_errors'] = ['Invalid login']
            return render(self.request, 'login.html',
                          {'form': form})"""
                          
    def form_valid(self, form):
        form.user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, form.user)
        #messages.info(self.request, 'Login successful')
        return super(LoginView, self).form_valid(form)
        
        
class LogoutView(RedirectView):
                                                        
    permanent = False
                                                        
    def get_redirect_url(self):
        return reverse('login')
 
    def dispatch(self, request, *args, **kwargs):
        try:
            logout(request)
        except:
            ## if we can't log the user out, it probably means they we're not logged-in to begin with, so we do nothing
            pass
        #messages.info(request, 'You have successfully logged out. Come back soon.')
        return super(LogoutView, self).dispatch(request, *args, **kwargs)
        

def send_custom_email(user):
    registration = Registration.objects.create(user=user)
    
    # Assign user to group
    """user_role = self.request.POST.get('user_role', None)
    if user_role.strip() == "employer":
        employer_group = Group.objects.get(name="Employer")
        user.groups.add(employer_group)
    else:
        student_group = Group.objects.get(name="Student")
        user.groups.add(student_group)"""
        
    # Currently defaults to student group
    student_group = Group.objects.get(name="Student")
    user.groups.add(student_group)
    
    # Send email to user
    t = loader.get_template('templated_email/registration.txt')
    c = Context({
        'name': user.username,
        'product_name': settings.SITE_NAME,
        'product_url': 'http://{0}'.format(settings.SITE_URL),
        'login_url': 'http://{0}/login/'.format(settings.SITE_URL),
        
        # TODO: Delete these afterwards or edit as appropriate
        'url_name': 'activation',
        'url_param': 'key',
        'registration': registration,
    })
    subject = 'Welcome to {0}'.format(settings.SITE_NAME)
    #send_mail(subject, t.render(c), 'from@address.com', [new_data['email']], fail_silently=False)        
    user.email_user(subject, t.render(c), settings.DEFAULT_FROM_EMAIL)
        
        
class RegisterView(FormView):

    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    
    def get_success_url(self):
        return reverse('confirmation_mail_sent')
        
    def form_valid(self, form):
        user = form.save()
        #messages.info(self.request, 'Registration successful.')
        
        send_custom_email(user)
        return super(RegisterView, self).form_valid(form)
        
        
class NewUserRegistrationAPI(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
        users = get_user_model().objects.all()
        serializer = NewUserRegistrationSerializer(users, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None):
        serializer = NewUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Send custom email to user
            user = get_user_model().objects.latest('id')
            send_custom_email(user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class EmailSentView(TemplateView):
 
    template_name = 'users/email_sent.html'
    
    
class ActivationView(RedirectView):
 
    permanent = False
 
    def get_redirect_url(self):
        return reverse('login')
 
    def get(self, request, *args, **kwargs):
        uuid = request.GET.get('key', None)
        if uuid is None:
            raise Http404
        try:
            user = get_user_model().objects.get(registration__uuid=uuid, registration__type='register')
            user.is_active = True
            user.save()
            user.registration.delete()
            #messages.info(self.request, 'User activation successfull')
        except Exception as e:
            print(e)
            raise Http404
        return super(ActivationView, self).get(request, *args, **kwargs)
        
                
"""def register(request): # TODO: Convert this to CBV
"""
#User registration view.
"""
if request.method == 'POST':
form = RegistrationForm(data=request.POST)
if form.is_valid():
    user = form.save()
    return redirect('/')
else:
form = RegistrationForm()
return render_to_response('accounts/register.html', {
'form': form,
}, context_instance=RequestContext(request))"""
