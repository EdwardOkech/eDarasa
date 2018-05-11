# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0003_auto_20160510_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='essayquestion',
            name='forward',
            field=models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward Answer?'),
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='forward_to_exercise',
            field=models.ManyToManyField(related_name='forwarded_exercises_answers_eq', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True),
        ),
        migrations.AddField(
            model_name='multichoicequestion',
            name='forward',
            field=models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward Answer?'),
        ),
        migrations.AddField(
            model_name='multichoicequestion',
            name='forward_to_exercise',
            field=models.ManyToManyField(related_name='forwarded_exercises_answers_mc', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='forward',
            field=models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward Answer?'),
        ),
        migrations.AddField(
            model_name='question',
            name='forward_to_exercise',
            field=models.ManyToManyField(related_name='forwarded_exercises_answers', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True),
        ),
    ]
