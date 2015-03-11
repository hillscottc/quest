# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questapp', '0004_auto_20150304_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='DbStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dbkey', models.CharField(max_length=255)),
                ('dbval', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='clue',
            name='last_accessed',
        ),
    ]
