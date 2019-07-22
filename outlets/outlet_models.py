import datetime

from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from libs.constants import CURRENCY_CHOICES, area_choices, COUNTRY_CHOICES
from multiselectfield import MultiSelectField

from libs.db_func import OUTLET_IMAGE_PATH, update_file_path
from libs.fields import SizeRestrictedThumbnailerField
from libs.models import CustomModel


def outlet_image_path(instance, filename):
    return update_file_path(OUTLET_IMAGE_PATH + '{0}/{1}.{2}'.format(instance.display_name,
                                                                     instance.city,
                                                                     filename.split('.')[-1]))


# Create your models here.
class Outlet(CustomModel):
    date_created = models.DateField(_("Created Date"), default=timezone.now, null=True, blank=True)

    display_name = models.CharField("Outlet Name", max_length=100, blank=False)
    description = models.TextField(_("Description"), blank=False, help_text=_("Describe your Store."),

                                   default="Not Given.")
    opening_hours = models.TimeField(_("Opening Time"), default=datetime.time(8, 0), help_text=_("e.g. 9:00:00"),
                                     blank=True)
    closing_hours = models.TimeField(_("Closing Time"), default=datetime.time(16, 0), help_text=_("e.g. 18:00:00"),
                                     blank=True)

    country = models.CharField("Country", max_length=100, default="UAE", choices=COUNTRY_CHOICES)
    city = models.CharField("City", max_length=100, blank=False, help_text="Province/State/Region")
    street = models.CharField("Street Name", max_length=100, blank=False)
    longitude = models.FloatField("Outlet Longitude", default=0.0, blank=False, help_text="Longitude")
    latitude = models.FloatField("Outlet Latitude", default=0.0, blank=False, help_text="Latitude")

    time_zone = models.CharField("Outlet Timezone", max_length=100, )

    currency = models.FloatField("Currency", default=1, choices=CURRENCY_CHOICES, help_text="Choose Currency")
    delivery_area = MultiSelectField("Delivery Areas", choices=area_choices, blank=True,
                                     null=True, help_text="Approximately choose various delivery areas")
    contact = models.CharField(_("Outlet Contact Phone No."), max_length=50, blank=False,
                               help_text=_("example : +977 01 6643ABC, +977 01 6643XYZ"))

    tax_type = models.CharField(choices=(("GST", "GST"), ("TRN", "TRN")), max_length=3)
    thumbnail = models.ImageField("Thumbnail", upload_to="photos/thumbnails/outlets/", max_length=500, default="",
                                  blank=True)
    slug = models.SlugField("Short Display Name", null=True, blank=False, max_length=25,
                            help_text="Used to share your store among Customers", validators=[validators.RegexValidator])
    email = models.EmailField("Outlet Contact E-mail", blank=False, null=False,
                              validators=[
                                  validators.EmailValidator(
                                      'Enter a valid email. This value may contain only '
                                      'letters, numbers,' 'and @/./+/-/_ characters.'
                                  )
                              ])
    connected_email = models.EmailField("Outlet Admin E-mail",
                                        unique=True,
                                        null=True,
                                        blank=True,
                                        validators=[
                                            validators.EmailValidator(
                                                'Enter a valid email. This value may contain only '
                                                'letters, numbers,' 'and @/./+/-/_ characters.'
                                            ),
                                        ],
                                        error_messages={'unique': "Email address already exists"})

    image = SizeRestrictedThumbnailerField(_("Outlet Logo"), upload_to=outlet_image_path,
                                           max_upload_size=10485760, resize_source=dict(size=(300, 0),
                                                                                        sharpen=True,
                                                                                        replace_alpha="#fff"
                                                                                        ),
                                           max_length=500,blank=True)

    def __str__(self):
        return "%s (%s,%s)" % (self.display_name, self.city, self.country)



