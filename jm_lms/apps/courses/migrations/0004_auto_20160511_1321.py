# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20160510_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='end_of_module',
            field=models.TextField(default=None, help_text='Wrap and summarize this module', null=True, verbose_name='Module Summary'),
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
