# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0008_auto_20160411_1116'),
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
        migrations.AddField(
            model_name='questionasked',
            name='test',
            field=models.CharField(default=datetime.datetime(2016, 4, 11, 8, 27, 29, 198440, tzinfo=utc), max_length=256),
            preserve_default=False,
        ),
    ]
