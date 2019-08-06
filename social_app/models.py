from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager, Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import EmailValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.apps import apps as django_apps

from libs.fields import SizeRestrictedThumbnailerField# from libs.utils import get_permissions
from libs.signals import create_thumbnail
from libs.db_func import USER_IMAGE_PATH, update_directory_file_path, USER_THUMBNAIL_PATH
from libs.models import CustomModel
from libs.validators import PHONE_REGEX
from libs.constants import ADDRESS_CHOICES, COUNTRY_CHOICES
from social_app.validators import password_hashed


class OccasionUserManager(UserManager):
    def get_by_natural_key(self, username):
        """
        Username field is email
        """
        return self.get(email__iexact=username)

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password and other fields.
        """

        email = self.normalize_email(email).lower()
        user = self.model(email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class ShippingAddress(models.Model):
    hash = models.CharField(_("Hash Value"), max_length=65, blank=True, null=True,
                            help_text=_("Auto Fill"), unique=True)
    country = models.CharField(_("Country"),
                               choices=COUNTRY_CHOICES,
                               max_length=100)
    name = models.CharField(_("Full Name"), max_length=100)  # full_name
    city = models.CharField(_("City"),
                            # choices=CITY_CHOICES,
                            max_length=100)
    area = models.CharField(_("Area"),
                            # choices=area_choices,
                            max_length=100)
    building = models.CharField(_("Building Name/No."), max_length=50)
    nearest_landmark = models.CharField(_("Nearest Landmark"), max_length=100)

    mobile_number = models.CharField(_("Alternative Number"), validators=[PHONE_REGEX], max_length=17)
    type = models.CharField(_("Address Type"), max_length=10, choices=ADDRESS_CHOICES)

    alternative_email = models.EmailField(_("Alternative Email"), validators=[EmailValidator()], blank=True, null=True)
    floor = models.CharField(_("Floor No."), max_length=20, blank=True, null=True)
    apartment = models.CharField(_("Apartment No."), max_length=20, blank=True, null=True)
    company = models.CharField(_("Company Name"), max_length=40, blank=True, null=True)
    room = models.CharField(_("Room Number"), max_length=20, blank=True, null=True)
    street = models.CharField(_("Street Name/No."), max_length=100, blank=True, null=True)

    latitude = models.FloatField(_("Latitude"))
    longitude = models.FloatField(_("Longitude"))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ShippingAddress, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return "%s, %s - %s" % (self.area, self.city, self.mobile_number)


def update_user_image_path(instance, filename):
    return update_directory_file_path(USER_IMAGE_PATH + 'user_{0}/{1}'.format(instance.id, filename))


def update_user_thumbnail_path(instance, filename):
    return update_directory_file_path(USER_THUMBNAIL_PATH + 'user_{0}/{1}'.format(instance.id, filename))


class OccasionUser(AbstractUser):
    """
    An abstract base class implementing a fully featured User model with
    admin_templates-compliant permissions.

    email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), unique=True, validators=[
        EmailValidator()
    ])
    password = models.CharField(_('password'), max_length=128, null=True)  # nullable for facebook/google
    username = models.CharField(
        _('username'),
        null=True,
        blank=True,
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
    )
    image = SizeRestrictedThumbnailerField(_("Profile Image"), upload_to=update_user_image_path, null=True, blank=True,
                                           max_upload_size=5242880, resize_source=dict(size=(600, 0)),
                                           default='NA.png', help_text=_("Optional"))
    thumbnail = models.ImageField(_("thumbnail"), upload_to="photos/thumbnails/users/",
                                  default='NA.png.250x250_q85_crop.jpg', blank=True)
    digital_sign = models.CharField(max_length=15, blank=True, null=True)
    mobile_number = models.CharField(_("Contact Number"), validators=[PHONE_REGEX], max_length=17, null=True,
                                     blank=True)

    addresses = models.ManyToManyField(ShippingAddress, blank=True)
    associated_outlet = models.ManyToManyField('outlets.Outlet', blank=True)
    objects = OccasionUserManager()

    backend = models.CharField(_("Which backend the user belongs to"), max_length=50, blank=True)
    last_feed_access = models.DateTimeField(_("Last Feed Access Date"), null=True, blank=True)
    last_feed_count = models.IntegerField(_("Last Feed Count"), blank=True, default=0)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def get_user_lat_lon(self):
        address = self.addresses.first()
        if address:
            return address.latitude, address.longitude
        return False

    @property
    def is_outletadmin(self):
        try:
            return django_apps.get_model('outlet.Outlet').admin_objects.filter(connected_email=self.email)
        except ObjectDoesNotExist:
            return False

    @property
    def has_storerights(self):
        # if has store rights returns the list of stores user has rights to
        if self.associated_store.count():
            return self.associated_store.all()
        elif self.is_outletadmin:
            return self.is_outletadmin

    def __str__(self):
        return '%s' % (self.username or self.get_full_name() or self.email)

    def delete(self, force_flag=False, *args, **kwargs):
        if force_flag:
            return super(OccasionUser, self).delete(*args, **kwargs)
        self.is_active = False
        self.save(*args, **kwargs)

    @property
    def full_name(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if not self.id:
            if self.password is not None:
                # new user, check for hashed password
                if not password_hashed(self.password):
                    self.set_password(self.password)

        # self.full_clean(exclude=["password"])
        super(OccasionUser, self).save(*args, **kwargs)


post_save.connect(create_thumbnail, sender=OccasionUser)
