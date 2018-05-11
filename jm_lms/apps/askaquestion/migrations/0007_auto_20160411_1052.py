# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0006_auto_20160410_0248'),
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
