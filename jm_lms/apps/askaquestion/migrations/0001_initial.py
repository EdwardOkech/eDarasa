# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField(default=None, verbose_name='Question Description')),
            ],
            options={
                'verbose_name': 'Question Answer',
            },
        ),
        migrations.CreateModel(
            name='QuestionAsked',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120, verbose_name='Question Title')),
                ('body', models.TextField(verbose_name='Question Description')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='sent at', null=True)),
                ('read_at', models.DateTimeField(null=True, verbose_name='read at', blank=True)),
                ('replied_at', models.DateTimeField(null=True, verbose_name='replied at', blank=True)),
                ('slug', models.SlugField(editable=False)),
                ('lesson', models.ForeignKey(to='courses.Lesson')),
                ('parent_question', models.ForeignKey(related_name='next_questions', verbose_name='Parent question', blank=True, to='askaquestion.QuestionAsked', null=True)),
                ('sender', models.ForeignKey(related_name='asked_questions', verbose_name='Sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_at'],
                'verbose_name': 'Question Asked',
                'verbose_name_plural': 'Questions Asked',
            },
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='question',
            field=models.ForeignKey(to='askaquestion.QuestionAsked'),
        ),
    ]
