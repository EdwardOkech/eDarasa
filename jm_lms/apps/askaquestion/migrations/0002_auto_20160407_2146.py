# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0001_initial'),
    ]
 
    operations = [
        migrations.AddField(
            model_name='questionasked',
            name='answer',
            field=models.TextField(default=None, blank=True, null=True, help_text='Answer question asked', verbose_name='Question Description'),
        ),
    ]
