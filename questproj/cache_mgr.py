import random
import logging
from django.core.cache import cache
from questapp.models import Clue
from questproj.utils import get_random_objs

log = logging.getLogger(__name__)


def reset_cache(key='rand_clues', timeout=3600, size=1000):
    """
    Resets the cache of Clues
    :param size:
    :param secs:
    :return: the newly cached value
    """
    log.info('Begin reset cache.')
    value = list(get_random_objs(Clue, size))
    cache.set(key, value, timeout)
    log.info('End cache reset.')
    return cache.get('rand_clues')


def get_cached_clues(num=5):
    """
    Get some clues from the cache.
    :param num: how many
    :return: a list of clues
    """
    log.info('Gettng %s cached clues.' % num)
    rand_clues = cache.get('rand_clues')
    if not rand_clues:
        rand_clues = reset_cache()
    clue_list = []
    for i in range(num):
        clue_list.append(random.choice(rand_clues))
    return clue_list
