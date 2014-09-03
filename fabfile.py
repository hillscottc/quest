"""A python Fabric (http://www.fabfile.org/) module to assist in automating database tasks.
Uses settings from the user's DJANGO_SETTINGS_MODULE.

Usage:
  fab rebuild     Executes the main rebuild task.
  fab -l          Print these comments and available commands.
  fab rebuild:drop_db=True,user=some_user
                  To specify add'l options.
"""
import os

from fabric.api import local, sudo, env, task, abort
from django.conf import settings as django_settings

env.hosts = ['localhost', ]


@task
def rebuild(drop_db=True, user=None):
    """
    Recreate and sync db, load fixtures.
    """
    recreate(drop_db, user)
    local('./manage.py syncdb --noinput')


def recreate(drop_db=False, user=None):
    """
    Drop, then create the database.
    """
    sets = get_sets()
    user_cmd = ''

    if user:
        user_cmd = '-U {}'.format(user)

    if drop_db:
        sudo("psql template1 {} -c \"DROP DATABASE IF EXISTS {}\"".format(user_cmd, sets['dbname']))

    sudo("createdb {} -E UTF8 --echo --owner {} {}".format(
        user_cmd,
        sets['dbuser'],
        sets['dbname'])
    )


def get_sets():
    """Get settings from the user's DJANGO_SETTINGS_MODULE."""
    sets = {
        'dj_settings': os.environ['DJANGO_SETTINGS_MODULE'],
        'dbname': django_settings.DATABASES['default']['NAME'],
        'dbuser': django_settings.DATABASES['default']['USER']
    }
    for key, val in sets.iteritems():
        if not val:
            abort("Aborting...no value for " + key)
    return sets
