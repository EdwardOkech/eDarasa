# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askaquestion', '0013_questionasked_test2'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('t', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'testmodules',
            },
        ),
    ]
