# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20160409_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='end_of_module',
            field=models.TextField(default=datetime.datetime(2016, 4, 9, 16, 18, 52, 415372, tzinfo=utc), help_text='Wrap and summarize this module', verbose_name='End Of Module Summary'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module',
            name='last_module',
            field=models.ForeignKey(related_name='previous_module', default=None, blank=True, to='courses.Module', null=True, verbose_name='Previous Module'),
        ),
        migrations.AddField(
            model_name='module',
            name='next_module',
            field=models.ForeignKey(related_name='the_next_module', default=None, blank=True, to='courses.Module', null=True, verbose_name='Next Module'),
        ),
    ]
