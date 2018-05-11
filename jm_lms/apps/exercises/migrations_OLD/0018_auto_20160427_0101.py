# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # ('exercises', '0012_auto_20160426_2347'),
        ('exercises', '0017_auto_20160426_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essayuseranswer',
            name='forward',
        ),
        migrations.RemoveField(
            model_name='essayuseranswer',
            name='forward_to_exercise',
        ),
        migrations.RemoveField(
            model_name='multichoiceusersubmittedanswer',
            name='forward',
        ),
        migrations.RemoveField(
            model_name='multichoiceusersubmittedanswer',
            name='forward_to_exercise',
        ),
        migrations.RemoveField(
            model_name='useranswer',
            name='forward',
        ),
        migrations.RemoveField(
            model_name='useranswer',
            name='forward_to_exercise',
        ),
    ]
