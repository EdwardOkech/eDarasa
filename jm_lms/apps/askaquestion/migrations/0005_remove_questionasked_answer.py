# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0004_auto_20160407_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionasked',
            name='answer',
        ),
    ]
