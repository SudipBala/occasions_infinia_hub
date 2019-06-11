from __future__ import unicode_literals

from django.conf import settings
from easy_thumbnails.files import get_thumbnailer


def create_thumbnail_from_image(image, size=300, quality=85):
    thumbnail_options = {'crop': False, 'size': (size, size), 'quality': quality}
    thumbnailer = get_thumbnailer(image)
    return thumbnailer.get_thumbnail(thumbnail_options=thumbnail_options)


def get_absolute_media_url(name):
    return "{0}{1}".format(settings.MEDIA_URL, name)

