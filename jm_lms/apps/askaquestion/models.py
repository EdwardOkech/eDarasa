from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from jm_lms.apps.courses.models import Lesson


class QuestionAsked(models.Model):
    title = models.CharField(_("Question Title"), max_length=120)
    body = models.TextField(_("Question Description"))
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='asked_questions', verbose_name=_("Sender"))
    lesson = models.ForeignKey(Lesson)
    parent_question = models.ForeignKey('self', related_name='next_questions', null=True, blank=True, verbose_name=_("Parent question"))
    sent_at = models.DateTimeField(_("sent at"), auto_now_add=True, null=True, blank=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
    slug = models.SlugField(editable=False)
    answer = models.TextField(_("Question's Answer"), null=True, blank=True)
    
    

    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("Question Asked")
        verbose_name_plural = _("Questions Asked")
        
    def __unicode__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.id:
            slug = slugify(self.title)
            new_slug = slug
            count = 0
            while QuestionAsked.objects.filter(slug=new_slug).exclude(id=self.id).count() > 0:
                count += 1
                new_slug = '{slug}-{count}'.format(slug=slug, count=count)
            self.slug = new_slug
            
        super(QuestionAsked, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('askedquestion_detail', args=[self.slug])







