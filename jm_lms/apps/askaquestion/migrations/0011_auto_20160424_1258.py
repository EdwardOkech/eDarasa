# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('askaquestion', '0010_remove_questionasked_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionasked',
            name='answer',
            field=models.TextField(default=0, help_text='Relevant trainer answer to question asked', verbose_name='Answer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionasked',
            name='trainer_name',
            field=models.ForeignKey(related_name='answered_questions', verbose_name='Trainer Name', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
