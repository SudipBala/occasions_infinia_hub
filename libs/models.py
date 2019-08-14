from __future__ import unicode_literals

import hashlib

import binascii
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class HashModel(models.Model):
    hash = models.CharField(_("Hash Value"), max_length=100, blank=True, null=True,
                            help_text=_("Auto Fill"), unique=True)

    class Meta:
        abstract = True


@receiver(post_save)
def generate_hash(sender, **kwargs):
    if issubclass(sender, HashModel):
        instance = kwargs.get('instance')
        if instance.hash:
            return
        derived_key = hashlib.pbkdf2_hmac('sha256',
                                          (instance._meta.model_name+str(instance.id)+instance._meta.app_label).encode('ascii'),
                                          settings.SECRET_KEY.encode('ascii'),
                                          1000)
        instance.hash = binascii.hexlify(derived_key)
        instance.save()
