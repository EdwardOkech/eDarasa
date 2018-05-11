from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm, AuthenticationForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.forms import TextInput

from .models import AuthUser


class CustomUserCreationForm(UserCreationForm):
    """ A form for creating new users. Includes all the required fields, plus a repeated password. """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = AuthUser
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            AuthUser._default_manager.get(username=username)
        except AuthUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        #Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        
        
class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields on the user, but 
    replaces the password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField(label="password",
                                         help_text="""Raw passwords are not stored, so there is no way to see this
                                         user's password, but you can change the password using <a href=\"password/\">
                                         this form</a>.""")

    class Meta(UserChangeForm.Meta):
        model = AuthUser
        fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'user_permissions')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
        
        
class LoginForm(forms.Form):                           
         
    login = forms.CharField(label = 'Username or e-mail', required=True)                                         
    password  = forms.CharField(label = 'Password', widget = forms.PasswordInput, required = True)
       
    def clean(self):                                     
        login = self.cleaned_data.get('login', '')         
        password = self.cleaned_data.get('password', '')
        self.user = None
        users = get_user_model().objects.filter(Q(username=login)|Q(email=login))
        for user in users:
            if user.is_active and user.check_password(password):
                self.user = user
        if self.user is None:
            raise forms.ValidationError('Invalid username or password')
        return self.cleaned_data
        

class UserRegistrationForm(CustomUserCreationForm):
    class Meta:
        model = AuthUser
        fields = ('username', 'email')

       
"""class RegistrationForm(forms.ModelForm):
"""
#Form for registering a new user.
"""
email = forms.EmailField(widget=forms.widget.TextInput,label="Email")
password1 = forms.CharField(widget=forms.widget.PasswordInput,
                        label="Password")
password2 = forms.CharField(widget=forms.widget.PasswordInput,
                        label="Password (again)")
                        
class Meta:
model = AuthUser
fields = ['email', 'password1', 'password2']

def clean(self):
"""
#Verifies that the values entered into the password fields match

#NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
"""
cleaned_data = super(RegistrationForm, self).clean()
if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
    if self.cleaned_data['password1'] != self.cleaned_data['password2']:
        raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
return self.cleaned_data

def save(self, commit=True):
user = super(RegistrationForm, self).save(commit=False)
user.set_password(self.cleaned_data['password1'])
# TODO: Save the Group
if commit:
    user.save()
return user"""
