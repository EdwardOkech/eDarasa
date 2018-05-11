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
            name='JobPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Job title')),
                ('description', models.TextField(help_text='Job description', verbose_name=b'Job description')),
                ('date_posted', models.DateTimeField(auto_now_add=True, verbose_name='Date posted')),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(help_text='Unique identifier', editable=False)),
                ('posted_by', models.ForeignKey(verbose_name=b'Posted by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Jobs',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.AddField(
            model_name='jobpost',
            name='type',
            field=models.ForeignKey(to='jobs.JobType'),
        ),
    ]
