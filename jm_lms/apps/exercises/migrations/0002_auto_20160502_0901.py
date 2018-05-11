# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='essayquestion',
            name='forward',
            field=models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward Answer?'),
        ),
        migrations.AddField(
            model_name='multichoicequestion',
            name='forward',
            field=models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward Answer?'),
        ),
        migrations.AddField(
            model_name='question',
            name='forward',
            field=models.BooleanField(default=False, help_text="Click to forward user's answer to another exercise", verbose_name='Forward Answer?'),
        ),
    ]
