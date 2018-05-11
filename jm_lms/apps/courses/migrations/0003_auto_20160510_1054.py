# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20160502_0849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='end_of_module',
        ),
        migrations.RemoveField(
            model_name='module',
            name='last_module',
        ),
        migrations.RemoveField(
            model_name='module',
            name='next_module',
        ),
    ]
