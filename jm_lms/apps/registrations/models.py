from django.db import models

class ProspectiveUser(models.Model):
    full_names = models.CharField(max_length=130, blank=True)
    email = models.EmailField(max_length=70, unique=True)
    phone_number = models.CharField(max_length=12)
    education = models.CharField(max_length=60, blank=True)
    current_job = models.CharField(max_length=60, blank=True)
    
    class Meta:
        verbose_name = "Prospective User"
        verbose_name_plural = "Prospective Users"
