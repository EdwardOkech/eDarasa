# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The course title', max_length=200, verbose_name='Course Name')),
                ('description', models.TextField(help_text='Course description', verbose_name=b'Course Description')),
                ('slug', models.SlugField(help_text='Unique identifier', editable=False)),
                ('position', positions.fields.PositionField(default=-1)),
                ('position_order', models.IntegerField(default=0, verbose_name='Order to be shown in views')),
                ('prerequisite', models.ForeignKey(default=None, blank=True, to='courses.Course', null=True, verbose_name='Prerequisite Course')),
            ],
            options={
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(verbose_name=b'In Course', to='courses.Course', help_text='Course of Enrolment.')),
                ('student', models.ForeignKey(related_name='enrolment_student', verbose_name=b'The Enrolled', to=settings.AUTH_USER_MODEL, help_text='Enrol this user as student in Course.')),
            ],
            options={
                'ordering': ('student', 'course'),
            },
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('link', models.URLField(blank=True)),
                ('file', models.FileField(upload_to=b'examples_upload/%Y/%m/%d', blank=True)),
            ],
            options={
                'verbose_name': 'Example',
                'verbose_name_plural': 'Examples',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The lesson title', max_length=200, verbose_name='Lesson Title')),
                ('content', models.TextField()),
                ('instructions_before', models.TextField(default=None, null=True, verbose_name='Instructions before exercise', blank=True)),
                ('instructions_after', models.TextField(default=None, null=True, verbose_name='Instructions after exercise', blank=True)),
                ('slug', models.SlugField(help_text='Unique identifier', editable=False)),
                ('position', positions.fields.PositionField(default=0)),
                ('exercises', models.ManyToManyField(related_name='lesson_exercises', verbose_name='Exercise', to='exercises.Exercise', blank=True)),
            ],
            options={
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
            },
        ),
        migrations.CreateModel(
            name='LessonQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Question Title')),
                ('description', models.TextField(help_text='Description about the question', verbose_name=b'Student Question Description')),
                ('date_asked', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('status', models.IntegerField(default=1, verbose_name=b'Question Status', choices=[(0, 'Closed'), (1, 'Open')])),
                ('lesson', models.ForeignKey(verbose_name=b'Lesson', to='courses.Lesson', help_text='The Lesson to get more information about.')),
                ('student', models.ForeignKey(related_name='student_lesson_questions', verbose_name=b'The asker of the question', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lesson Question',
                'verbose_name_plural': 'Lesson Questions',
            },
        ),
        migrations.CreateModel(
            name='LessonQuestionResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reply', models.TextField(help_text='Answer to Student Question', verbose_name=b'Reply to Student Question')),
                ('date_answered', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('lesson_question', models.ForeignKey(verbose_name=b'Lesson Question', to='courses.LessonQuestion')),
                ('replier', models.ForeignKey(verbose_name=b'The replier to the question', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_answered'],
                'verbose_name': 'Response to Lesson Question',
                'verbose_name_plural': 'Response to Lesson Questions',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The module title', max_length=200, verbose_name='Module Name')),
                ('description', models.TextField(help_text='Module description', verbose_name=b'Module Description')),
                ('slug', models.SlugField(help_text='Unique identifier', editable=False)),
                ('status', models.IntegerField(default=3, verbose_name=b'Module Status', choices=[(1, 'Draft'), (2, 'Suspended'), (3, 'Published')])),
                ('position', positions.fields.PositionField(default=0)),
                ('course', models.ForeignKey(to='courses.Course')),
                ('prerequisite', models.ForeignKey(default=None, blank=True, to='courses.Module', null=True, verbose_name='Prerequisite Module')),
            ],
            options={
                'verbose_name_plural': 'Modules',
            },
        ),
        migrations.CreateModel(
            name='StudentLessonProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Lesson Status', choices=[(0, 'Not Started'), (1, 'In Progress'), (2, 'Completed')])),
                ('done_percent', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lesson', models.ForeignKey(to='courses.Lesson')),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student Lesson Progress',
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='module',
            field=models.ForeignKey(to='courses.Module'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='prerequisite',
            field=models.ForeignKey(default=None, blank=True, to='courses.Lesson', null=True, verbose_name='Prerequisite Lesson'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='quizzes',
            field=models.ManyToManyField(related_name='lessons', verbose_name='Quiz', to='quiz.Quiz', blank=True),
        ),
        migrations.AddField(
            model_name='example',
            name='lesson',
            field=models.ForeignKey(to='courses.Lesson'),
        ),
        migrations.AlterUniqueTogether(
            name='studentlessonprogress',
            unique_together=set([('student', 'lesson')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together=set([('student', 'course')]),
        ),
    ]
