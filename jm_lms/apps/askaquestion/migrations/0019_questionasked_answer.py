# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0018_auto_20160510_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionasked',
            name='answer',
            field=models.TextField(null=True, verbose_name="Question's Answer", blank=True),
        ),
    ]
