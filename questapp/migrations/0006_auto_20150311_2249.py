# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('questapp', '0005_auto_20150307_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clue',
            name='modified',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now=True),
            preserve_default=True,
        ),
    ]
