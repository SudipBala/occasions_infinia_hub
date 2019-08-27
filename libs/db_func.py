import os
import shutil
from django.conf import settings

STOCK_IMAGE_PATH = 'stocks/'
OUTLET_IMAGE_PATH = 'outlets/'
CATEGORY_IMAGE_PATH = 'category/'

THUMBNAIL_PATH = 'thumbnails/'

USER_IMAGE_PATH = 'user/'
USER_THUMBNAIL_PATH = THUMBNAIL_PATH + 'user/'


def update_file_path(relative_path=None):
    """ delete existing file from the path and returns file full path name """
    path = os.path.join(settings.MEDIA_ROOT, relative_path)
    path_ = os.path.join(relative_path)
    try:
        if os.path.exists(path):
            os.remove(path)
        else:
            os.remove(path_)
    except OSError:  # no such file or directory
        pass
    return relative_path


def update_directory_file_path(relative_path=None):
    # folder for a single instance.
    path = os.path.join(settings.MEDIA_ROOT, relative_path)
    path_ = os.path.join(relative_path)

    base_dir = os.path.dirname(path)
    base_dir_ = os.path.dirname(path_)

    try:
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        else:
            shutil.rmtree(base_dir_)
    except OSError:
        pass
    return relative_path
