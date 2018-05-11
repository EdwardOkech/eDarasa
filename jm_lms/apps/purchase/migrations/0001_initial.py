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
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchased_at', models.DateTimeField(auto_now_add=True)),
                ('pesapal_tx_id', models.CharField(max_length=250)),
                ('purchaser', models.ForeignKey(verbose_name=b'The purchaser of the training', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
