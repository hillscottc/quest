"""A python Fabric (http://www.fabfile.org/) module to assist in automating database tasks.
Uses settings from the user's DJANGO_SETTINGS_MODULE.
"""
import os

from fabric.api import local, sudo, env, task, abort
from fabric.contrib.console import confirm
from questapp.utils import load_samples
from django.conf import settings

env.hosts = ['localhost', ]

DB_NAME = settings.DATABASES['default']['NAME']
DB_USER = settings.DATABASES['default']['USER']


@task
def rebuild(db_user=DB_USER, db_name=DB_NAME):
    """Recreate and sync db, load fixtures.
    """
    db_args = dict(db_name=db_name, db_user=db_user)
    if not confirm("\nSettings module:{module}, db:{db_user}, owner:{db_name}. Proceed?".format(
            module=os.environ['DJANGO_SETTINGS_MODULE'], **db_args)):
        abort("Aborting at user request.")

    # sudo("psql template1 -U {db_user} -c \"DROP DATABASE IF EXISTS {db_name}\"".format(**db_args))
    # sudo("createdb -U {db_user} -E UTF8 --owner {db_user} {db_name}".format(**db_args))

    local("psql -c \"DROP DATABASE IF EXISTS %s\"" % db_name)
    local('createdb -E UTF8 quest_db')
    local('django-admin.py syncdb')


@task
def load_jeap(num=500):
    load_samples(num)



def _get_fixture_fname(name="proj_samples"):
    return os.path.join(os.path.dirname(settings.PROJ_DIR), 'questproj', 'fixtures',
                        '%s.json' % name)

@task
def dump_fixtures(filename="proj_samples"):
    local("django-admin.py dumpdata > %s" % _get_fixture_fname(filename))


@task
def load_fixtures(filename="proj_samples"):
    local("django-admin.py loaddata %s" % _get_fixture_fname(filename))