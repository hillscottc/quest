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
            name='Clue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('last_accessed', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=255)),
                ('question', models.CharField(max_length=355)),
                ('answer', models.CharField(max_length=355)),
            ],
            options={
                'ordering': ['category', 'question'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('last_accessed', models.DateTimeField(auto_now=True)),
                ('sid', models.CharField(help_text=b'(Jeapordy) Show id.', max_length=8, serialize=False, primary_key=True)),
                ('gid', models.CharField(help_text=b'(External) Game id.', max_length=8, unique=True, null=True, blank=True)),
                ('title', models.CharField(max_length=250)),
                ('air_date', models.DateField(null=True, blank=True)),
                ('comments', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ['-modified'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rights', models.IntegerField(default=0)),
                ('wrongs', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='clue',
            name='game',
            field=models.ForeignKey(to='questapp.Game'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='clue',
            unique_together=set([('game', 'category', 'question')]),
        ),
    ]
