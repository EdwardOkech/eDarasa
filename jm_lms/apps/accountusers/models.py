import uuid
from dateutil.relativedelta import relativedelta
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


def two_days_from_now():
    return timezone.now() + relativedelta(days=2)


class AuthUserManager(BaseUserManager):
    
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          is_staff=is_staff, 
                          is_active=True,
                          is_superuser=is_superuser, 
                          last_login=now,
                          date_joined=now, 
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)


class AuthUser(AbstractBaseUser, PermissionsMixin):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')

    ### Redefine the basic fields that would normally be defined in User ###
    username = models.CharField(unique=True, max_length=20, validators=[alphanumeric])
    email = models.EmailField(verbose_name='email address', unique=True, max_length=255)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, 
                                    null=False, 
                                    help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_staff = models.BooleanField(default=False, 
                                   null=False, 
                                   help_text=_('Designates whether the user can log into this admin site.'))

    ### NOTE: is_superuser is not defined here. This is because PermissionsMixin already defines this, and if you override it,
    ### then all the default Django user permissions won't work correctly, so you have to make sure you don't override the
    ### is_superuser field.
    
    ### Our own fields ###
    profile_image = models.ImageField(upload_to="uploads", blank=False, null=False, default="/static/images/defaultuserimage.png")
    user_bio = models.CharField(max_length=600, blank=True)

    objects = AuthUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def get_full_name(self):
        fullname = "{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name)
        return fullname

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return "{0} ({1})".format(self.username, self.email)
        
    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
        
        
class Registration(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(AuthUser, related_name='registration')
    expires = models.DateTimeField(default=two_days_from_now)
    type = models.CharField(max_length=10, choices=(
      ('register', 'register'),
      ('lostpass', 'lostpass'),
    ), default = 'register')
