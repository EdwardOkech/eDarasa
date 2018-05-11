# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essayquestion',
            name='title',
            field=models.TextField(help_text='Exercise Topic Title and description', null=True, verbose_name='Topic Box', blank=True),
        ),
        migrations.AlterField(
            model_name='multichoicequestion',
            name='title',
            field=models.TextField(help_text='Exercise Topic Title and description', null=True, verbose_name='Topic Box', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.TextField(help_text='Exercise Topic Title and description', null=True, verbose_name='Topic Box', blank=True),
        ),
    ]
