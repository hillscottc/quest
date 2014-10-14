from random import randint


def get_random_objs(obj_type, num_returned=1):
    db_count = obj_type.objects.count()
    for i in range(num_returned):
        yield obj_type.objects.all()[randint(0, db_count - 1)]


def trim(txt, length=30):
    if txt and len(txt) > length:
        return txt[:length-1] + '...'