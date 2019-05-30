from django.core import validators
from django.db import models
from lib.constants import CURRENCY_CHOICES, area_choices, COUNTRY_CHOICES
from multiselectfield import MultiSelectField
from django.contrib.auth.models import Group


# Create your models here.
class Outlet(models.Model):
    name = models.CharField("Outlet Name", max_length=100, blank=False)
    tax_type = models.CharField(choices=(("GST", "GST"), ("TRN", "TRN")), max_length=3)
    tax = models.DecimalField(decimal_places=2, max_digits=3)
    country = models.CharField("Country", max_length=100, default="UAE", choices=COUNTRY_CHOICES)
    contact = models.CharField("Contact", max_length=50, blank=False, help_text="Outlet Contact Number")
    city = models.CharField("City", max_length=100, blank=False, help_text="Province/State/Region")
    street = models.CharField("Street Name", max_length=100, blank=False)
    longitude = models.FloatField("Outlet Longitude", default=0.0, blank=False, help_text="Longitude")
    latitude = models.FloatField("Outlet Latitude", default=0.0, blank=False, help_text="Latitude")
    thumbnail = models.ImageField("Thumbnail", upload_to="", max_length=500, default="", blank=True)
    time_zone = models.CharField("Outlet Timezone", max_length=100, )
    currency = models.FloatField("Currency", default=1, choices=CURRENCY_CHOICES, help_text="Choose Currency")
    delivery_area = MultiSelectField("Delivery Areas", choices=area_choices, blank=True,
                                     null=True, help_text="Approximately choose various delivery areas" )
    slug = models.SlugField("Short Display Name", null=True, blank=True, max_length=25,
                            help_text="Used to share your store among Customers")
    email = models.EmailField("Outlet Contact E-mail", blank=False, null=False,
                              validators=[
                                  validators.EmailValidator(
                                      'Enter a valid email. This value may contain only '
                                      'letters, numbers,' 'and @/./+/-/_ characters.'
                                  )
                              ])
    connected_email = models.EmailField("Outlet Admin Contact E-mail",
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
    registration = models.CharField("Outlet Registration ", blank=False, max_length=50)

    def __str__(self):
        return self.name


