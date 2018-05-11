# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20160409_1918'),
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
