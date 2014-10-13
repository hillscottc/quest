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
from fabric.contrib.console import confirm
from django.conf import settings as django_settings

env.hosts = ['localhost', ]

DB_NAME = django_settings.DATABASES['default']['NAME']
DB_USER = django_settings.DATABASES['default']['USER']

@task
def rebuild(db_user=DB_USER, db_name=DB_NAME):
    """Recreate and sync db, load fixtures.
    """
    db_args = dict(db_name=db_name, db_user=db_user)
    if not confirm("\nSettings module:{module}, db:{db_user}, owner:{db_name}. Proceed?".format(
            module=os.environ['DJANGO_SETTINGS_MODULE'], **db_args)):
        abort("Aborting at user request.")

    sudo("psql template1 -U {db_user} -c \"DROP DATABASE IF EXISTS {db_name}\"".format(**db_args))
    sudo("createdb -U {db_user} -E UTF8 --owner {db_user} {db_name}".format(**db_args))
    local('django-admin.py syncdb')


@task
def dump_fixture(filename="proj_samples"):
    local('django-admin.py dumpdata > questproj/fixtures/%s.json' % filename)

