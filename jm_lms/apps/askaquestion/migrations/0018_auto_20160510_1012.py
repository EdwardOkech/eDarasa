# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0017_auto_20160510_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionasked',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='questionasked',
            name='trainer_name',
        ),
    ]
