# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_auto_20160502_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essayquestion',
            name='forward',
        ),
        migrations.RemoveField(
            model_name='essayquestion',
            name='forward_to_exercise',
        ),
        migrations.RemoveField(
            model_name='multichoicequestion',
            name='forward',
        ),
        migrations.RemoveField(
            model_name='multichoicequestion',
            name='forward_to_exercise',
        ),
        migrations.RemoveField(
            model_name='question',
            name='forward',
        ),
        migrations.RemoveField(
            model_name='question',
            name='forward_to_exercise',
        ),
    ]
