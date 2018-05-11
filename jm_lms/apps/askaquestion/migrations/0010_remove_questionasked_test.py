# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0009_auto_20160411_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionasked',
            name='test',
        ),
    ]
