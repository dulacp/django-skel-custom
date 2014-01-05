import os
import uuid
import datetime
import colorsys
import random
import hashlib

from django.utils.encoding import force_str, force_text

from colour import Color


def unique_filename(path, original_filename_field=None):
    """
    Return a unique filename, which is usefull for image upload for instance

    NB: you may need to override the model `save` method
        and force the update of the original filename field
        e.g. `super(YourModel, self).save(update_fields=['original_filename'])`
    """
    def _unique_path(obj, name):
        if original_filename_field and hasattr(obj, original_filename_field):
            setattr(obj, original_filename_field, name)
        parts = name.split('.')
        extension = parts[-1]
        directory_path = os.path.normpath(force_text(datetime.datetime.now().strftime(force_str(path))))
        unique_name = "{0}.{1}".format(uuid.uuid4(), extension)
        return os.path.join(directory_path, unique_name)
    return _unique_path

def queryset_iterator(queryset, chunksize=1000, reverse=False):
    """
    Execute the request by chunks to avoid database memory error
    """
    ordering = '-' if reverse else ''
    queryset = queryset.order_by(ordering + 'pk')
    last_pk = None
    new_items = True
    while new_items:
        new_items = False
        chunk = queryset
        if last_pk is not None:
            func = 'lt' if reverse else 'gt'
            chunk = chunk.filter(**{'pk__' + func: last_pk})
        chunk = chunk[:chunksize]
        row = None
        for row in chunk:
            yield row
        if row is not None:
            last_pk = row.pk
            new_items = True

def rgb_to_hex(rgb_tuple):
    assert len(rgb_tuple) == 3
    denormalized_values = tuple(map(lambda x: 256*x, rgb_tuple))
    return '#%02x%02x%02x' % denormalized_values

def generate_colors(num, from_color=Color('#178ed0'), to_color=Color('#ba3333')):
    """
    Generate `num` distinct Hexadecimal colors
    """
    if num == 0:
        return []
    elif num == 1:
        return [from_color.hex]
    return list(c.hex for c in from_color.range_to(to_color, num))

def random_token(extra=None, hash_func=hashlib.sha256):
    """
    Extracted from `django-user-accounts`
    """
    if extra is None:
        extra = []
    bits = map(force_str, extra) + [str(random.SystemRandom().getrandbits(512))]
    return hash_func("".join(bits)).hexdigest()
