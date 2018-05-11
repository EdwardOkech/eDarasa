# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    
        ('exercises', '0010_auto_20160411_1142'),
        
    ]

    operations = [
        migrations.RemoveField(
            model_name='tableexercisequestion',
            name='exercise',
        ),
        migrations.RemoveField(
            model_name='tableexerciseuseranswer',
            name='exercise_submission',
        ),
        migrations.RemoveField(
            model_name='tableexerciseuseranswer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='tableexerciseuseranswer',
            name='student',
        ),
        migrations.DeleteModel(
            name='TableExerciseQuestion',
        ),
        migrations.DeleteModel(
            name='TableExerciseUserAnswer',
        ),
    ]
