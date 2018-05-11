# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProspectiveUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_names', models.CharField(max_length=130, blank=True)),
                ('email', models.EmailField(unique=True, max_length=70)),
                ('phone_number', models.CharField(max_length=12)),
                ('education', models.CharField(max_length=60, blank=True)),
                ('current_job', models.CharField(max_length=60, blank=True)),
            ],
            options={
                'verbose_name': 'Prospective User',
                'verbose_name_plural': 'Prospective Users',
            },
        ),
    ]
