# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0014_testmodule'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestModule',
        ),
        migrations.RemoveField(
            model_name='questionasked',
            name='test1',
        ),
        migrations.RemoveField(
            model_name='questionasked',
            name='test2',
        ),
    ]
