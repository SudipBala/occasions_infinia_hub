from __future__ import unicode_literals

from django.conf import settings
from django.utils.crypto import get_random_string
from easy_thumbnails.files import get_thumbnailer


def create_thumbnail_from_image(image, size=300, quality=85):
    thumbnail_options = {'crop': False, 'size': (size, size), 'quality': quality}
    thumbnailer = get_thumbnailer(image)
    return thumbnailer.get_thumbnail(thumbnail_options=thumbnail_options)


def get_absolute_media_url(name):
    return "{0}{1}".format(settings.MEDIA_URL, name)


def get_random_secret_key(size=6, extra=''):
    """
    Return character random string usable as a SECRET_KEY setting value.
    """
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return get_random_string(size, chars) + extra
