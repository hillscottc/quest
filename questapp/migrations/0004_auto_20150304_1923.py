# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questapp', '0003_auto_20150303_2122'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='clue',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='clue',
            name='game',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
    ]
