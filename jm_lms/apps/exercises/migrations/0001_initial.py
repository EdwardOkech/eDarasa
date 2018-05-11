# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EssayQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(help_text='Exercise Topic Title and description', null=True, verbose_name='Topic Box', blank=True)),
                ('expected_answer', models.TextField(help_text='How the learner should answer the question. Shown after the question has been answered.', null=True, verbose_name=b'Expected Answer', blank=True)),
            ],
            options={
                'verbose_name': 'Essay Question',
                'verbose_name_plural': 'Essay Questions',
            },
        ),
        migrations.CreateModel(
            name='EssayUserAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField(null=True, blank=True)),
                ('answered_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('exercise', models.ForeignKey(verbose_name='Exercise', to='exercises.Exercise')),
                ('student', models.ForeignKey(related_name='exercise_submissions', verbose_name=b'The Student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Exercise Submission',
                'verbose_name_plural': 'Exercise Submissions',
            },
        ),
        migrations.CreateModel(
            name='MultiChoiceQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(help_text='Exercise Topic Title and description', null=True, verbose_name='Topic Box', blank=True)),
                ('expected_answer', models.TextField(help_text='How the learner should answer the question. Shown after the question has been answered.', null=True, verbose_name=b'Expected Answer', blank=True)),
                ('exercise', models.ForeignKey(verbose_name='Exercise', to='exercises.Exercise')),
                ('forward_to_exercise', models.ManyToManyField(related_name='forwarded_exercises_answers_mc', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True)),
            ],
            options={
                'verbose_name': 'Multiple Choice Question',
                'verbose_name_plural': 'Multiple Choice Questions',
            },
        ),
        migrations.CreateModel(
            name='MultiChoiceQuestionOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(help_text='Enter the answer text that you want displayed', max_length=1000, verbose_name='Answer Content')),
                ('correct', models.BooleanField(default=False, help_text='Is this a correct answer?', verbose_name='Correct')),
                ('question', models.ForeignKey(verbose_name='Question', to='exercises.MultiChoiceQuestion')),
            ],
            options={
                'verbose_name': 'MultiChoice Option',
                'verbose_name_plural': 'MultiChoice Options',
            },
        ),
        migrations.CreateModel(
            name='MultiChoiceUserSubmittedAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answered_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('exercise_submission', models.ForeignKey(verbose_name='Exercise Submission', blank=True, to='exercises.ExerciseSubmission', null=True)),
                ('question', models.ForeignKey(verbose_name='Question', to='exercises.MultiChoiceQuestion')),
                ('selected_choice', models.ForeignKey(verbose_name='Question', to='exercises.MultiChoiceQuestionOption')),
                ('student', models.ForeignKey(related_name='exercise_submitted_choice', verbose_name=b'The Student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'MultiChoice Submitted User Answer',
                'verbose_name_plural': 'MultiChoice Submitted User Answers',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(help_text='Exercise Topic Title and description', null=True, verbose_name='Topic Box', blank=True)),
                ('expected_answer', models.TextField(help_text='How the learner should answer the question. Shown after the question has been answered.', null=True, verbose_name=b'Expected Answer', blank=True)),
                ('num_of_expected_answers', models.IntegerField(default=1, verbose_name='Number of expected answers')),
                ('exercise', models.ForeignKey(verbose_name='Exercise', to='exercises.Exercise')),
                ('forward_to_exercise', models.ManyToManyField(related_name='forwarded_exercises_answers', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True)),
            ],
            options={
                'verbose_name': 'List Question',
                'verbose_name_plural': 'List Questions',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=256, null=True)),
                ('answered_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('exercise_submission', models.ForeignKey(verbose_name='Exercise Submission', blank=True, to='exercises.ExerciseSubmission', null=True)),
                ('question', models.ForeignKey(verbose_name='Question', to='exercises.Question')),
                ('student', models.ForeignKey(related_name='exercise_answers', verbose_name=b'The Student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'User Answer to List Question',
                'verbose_name_plural': 'User Answers to List Question',
            },
        ),
        migrations.AddField(
            model_name='essayuseranswer',
            name='exercise_submission',
            field=models.ForeignKey(verbose_name='Exercise Submission', blank=True, to='exercises.ExerciseSubmission', null=True),
        ),
        migrations.AddField(
            model_name='essayuseranswer',
            name='question',
            field=models.ForeignKey(verbose_name='Question', to='exercises.EssayQuestion'),
        ),
        migrations.AddField(
            model_name='essayuseranswer',
            name='student',
            field=models.ForeignKey(related_name='exercise_essay_answers', verbose_name=b'The Student', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='exercise',
            field=models.ForeignKey(verbose_name='Exercise', to='exercises.Exercise'),
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='forward_to_exercise',
            field=models.ManyToManyField(related_name='forwarded_exercises_answers_eq', verbose_name='Forward To Exercise', to='exercises.Exercise', blank=True),
        ),
    ]
