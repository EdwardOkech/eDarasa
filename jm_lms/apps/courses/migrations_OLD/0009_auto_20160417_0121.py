# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20160417_0117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='end_of_module_summary',
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
