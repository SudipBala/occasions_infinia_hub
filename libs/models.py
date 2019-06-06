from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings


class CustomManager(models.Manager):
    def get_queryset(self):
        try:
            if settings.DUMP:  # WHEN DUMPING WE WANT THE deleted=True data as well
                return super(CustomManager, self).get_queryset()
        except AttributeError:
            pass

        return super(CustomManager, self).get_queryset().filter(deleted=False)


class CustomModel(models.Model):
    deleted = models.BooleanField(_("Deleted"), default=False)

    def delete(self, using=None, keep_parents=False, force_flag=False):
        if force_flag:
            super(CustomModel, self).delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted = True
            print("force_flag = True for permanent")
            self.save()

    objects = CustomManager()
    _objects = models.Manager()

    class Meta:
        abstract = True
