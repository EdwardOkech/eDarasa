# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_tableexercisequestion_tableexerciseuseranswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='tableexercisequestion',
            name='forward_to_exercise',
            field=models.ManyToManyField(related_name='forwarded_exercises_answers_ta', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True),
        ),
    ]
