# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0002_auto_20160407_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionasked',
            name='answer',
            field=models.TextField(default=None, help_text='Answer question asked', null=True, verbose_name='Question Description'),
        ),
    ]
