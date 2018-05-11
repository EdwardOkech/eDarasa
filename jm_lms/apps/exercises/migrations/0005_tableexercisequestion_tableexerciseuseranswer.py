# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercises', '0004_auto_20160510_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableExerciseQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(help_text='Exercise Topic Title and description', null=True, verbose_name='Topic Box', blank=True)),
                ('expected_answer', models.TextField(help_text='How the learner should answer the question. Shown after the question has been answered.', null=True, verbose_name=b'Expected Answer', blank=True)),
                ('forward', models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward Answer?')),
                ('table_header', models.CharField(max_length=256, null=True)),
                ('num_of_expected_entries', models.IntegerField(default=1, verbose_name='Number of expected entries')),
                ('exercise', models.ForeignKey(verbose_name='Exercise', to='exercises.Exercise')),
            ],
            options={
                'verbose_name': 'Table Exercise Question',
                'verbose_name_plural': 'Table Exercise Questions',
            },
        ),
        migrations.CreateModel(
            name='TableExerciseUserAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=256, null=True)),
                ('answered_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('exercise_submission', models.ForeignKey(verbose_name='Exercise Submission', blank=True, to='exercises.ExerciseSubmission', null=True)),
                ('question', models.ForeignKey(verbose_name=' Table Exercise Question', to='exercises.TableExerciseQuestion')),
                ('student', models.ForeignKey(related_name='table_exercise_answers', verbose_name=b'The Student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'User Answer to Table Exercise Question',
                'verbose_name_plural': 'User Answers to Table Exercise Question',
            },
        ),
    ]
