# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20160417_0105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='end_of_module',
        ),
        migrations.AddField(
            model_name='module',
            name='end_of_module_summary',
            field=models.TextField(default=None, help_text='Wrap and summarize this module', verbose_name='End Of Module Summary'),
        ),
    ]
