# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # ('exercises', '0011_auto_20160426_2301'),
         ('exercises', '0016_auto_20160426_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='essayuseranswer',
            name='forward',
            field=models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward User Answer'),
        ),
        migrations.AddField(
            model_name='essayuseranswer',
            name='forward_to_exercise',
            field=models.ManyToManyField(related_name='forwarded_exercises_eq', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True),
        ),
        migrations.AddField(
            model_name='multichoiceusersubmittedanswer',
            name='forward',
            field=models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward User Answer'),
        ),
        migrations.AddField(
            model_name='multichoiceusersubmittedanswer',
            name='forward_to_exercise',
            field=models.ManyToManyField(related_name='forwarded_exercises_mc', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='forward',
            field=models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward User Answer'),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='forward_to_exercise',
            field=models.ManyToManyField(related_name='forwarded_exercises', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True),
        ),
    ]
