# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_remove_module_end_of_module'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='last_module',
        ),
        migrations.RemoveField(
            model_name='module',
            name='next_module',
        ),
    ]
