# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0003_auto_20160407_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionasked',
            name='answer',
            field=models.TextField(default=datetime.datetime(2016, 4, 7, 18, 49, 21, 481299, tzinfo=utc), help_text='Answer question asked', verbose_name='Question Description'),
            preserve_default=False,
        ),
    ]
