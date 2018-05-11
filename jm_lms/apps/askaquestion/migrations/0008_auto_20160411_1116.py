# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('askaquestion', '0007_auto_20160411_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionasked',
            name='answer',
            field=models.TextField(default=datetime.datetime(2016, 4, 11, 8, 16, 29, 705803, tzinfo=utc), help_text='Relevant trainer answer to question asked', verbose_name='Answer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionasked',
            name='trainer_name',
            field=models.ForeignKey(related_name='answered_questions', verbose_name='Trainer Name', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
