from random import randint


def get_random_ids(obj_type, num_returned=1):
    rand_ids = []
    obj_ids = [obj.id for obj in obj_type.objects.all()]
    id_count = len(obj_ids)

    if id_count:
        for i in range(num_returned):
            rand_ids.append(obj_ids[randint(0, id_count - 1)])
    return rand_ids


def get_random_objs(obj_type, num_returned=1):
    """Yields given number of random objects of given type."""

    # Get a list of random clue ids
    rand_ids = get_random_ids(obj_type, num_returned)

    # Get and yield the objects using list of random ids.
    for obj_id in rand_ids:
        yield obj_type.objects.get(id=obj_id)


def trim(txt, length=30):
    if txt and len(txt) > length:
        return txt[:length-1] + '...'