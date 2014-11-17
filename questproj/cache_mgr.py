import random
import logging
from django.core.cache import cache
from questapp.models import Clue, Category
from questproj.utils import get_random_objs

log = logging.getLogger(__name__)


def get_dbstats():
    dbstats = cache.get('dbstats')
    if not dbstats:
        dbstats = {
            'clue_count': Clue.objects.count(),
            'cat_count': Category.objects.count(),
        }
        cache.set('dbstats', dbstats, 3600)
    return dbstats


def get_cache_key(obj):
    """Get the string used for the key."""
    return "random_%s" % obj.__name__


def reset_object_cache(obj, timeout=3600, size=1000):
    log.info('Begin reset cache of %s' % obj.__name__)
    key = get_cache_key(obj)
    value = list(get_random_objs(obj, size))
    cache.set(key, value, timeout)
    log.info('End cache reset of %s' % obj)
    return cache.get(key)


def get_cached_objs(obj, num=5):
    """Get some objects from the cache.
    If fails, cache for that object is reset. """
    log.info('Getting %s from cache of %s.' % (num, obj.__name__))
    rand_objs = cache.get(get_cache_key(obj))
    if not rand_objs:
        rand_objs = reset_object_cache(obj)
    obj_list = []
    for i in range(num):
        obj_list.append(random.choice(rand_objs))
    return obj_list

