# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0015_auto_20160426_1611'),
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
