# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20160417_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='end_of_module',
            field=models.TextField(default=None, help_text='Wrap and summarize this module', null=True, verbose_name='End Of Module Summary'),
        ),
    ]
