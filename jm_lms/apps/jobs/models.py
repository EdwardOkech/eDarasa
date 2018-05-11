from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class JobType(models.Model):
    """
    An available job type for working i.e. contract, full time or part time.
    
    Field Attributes:
      name: The name of the job type
    """
    
    name = models.CharField(max_length=80)
    
    def __unicode__(self):
        return self.name
        

class JobPost(models.Model):
    type = models.ForeignKey(JobType)
    title = models.CharField(verbose_name=_("Job title"), max_length=200)
    description = models.TextField(verbose_name="Job description", help_text=_("Job description"))
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Posted by')
    date_posted = models.DateTimeField(verbose_name=_("Date posted"), auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(editable=False, help_text=_('Unique identifier'))
    
    class Meta:
        verbose_name_plural = "Jobs"
        
    def __unicode__(self):
        return self.title
