from random import randint

def get_random_objs(obj_type, num_returned=1):
    """Yields given number of random objects of given type."""
    # Get a list of all the object's ids.
    obj_ids = [obj.id for obj in obj_type.objects.all()]
    id_count = len(obj_ids)

    # Pull list of random ids from id list.
    rand_ids = []
    for i in range(num_returned):
        rand_ids.append(obj_ids[randint(0, id_count - 1)])

    # Get and yield the objects using list of random ids.
    for obj_id in rand_ids:
        yield obj_type.objects.get(id=obj_id)


def trim(txt, length=30):
    if txt and len(txt) > length:
        return txt[:length-1] + '...'