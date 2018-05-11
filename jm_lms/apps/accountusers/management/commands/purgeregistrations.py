from django.core.management.base import BaseCommand
from django.utils import timezone
 
from accountusers.models import AuthUser, Registration


class Command(BaseCommand):
    args = None
    help = 'Purges expired registrations'

    def handle(self, *args, **kwargs):
        AuthUser.objects.filter(registration__expires__lte=timezone.now()).delete()
