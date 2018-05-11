# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0012_questionasked_test1'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionasked',
            name='test2',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
    ]
