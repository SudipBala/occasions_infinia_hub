from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from libs.constants import CURRENCY_CHOICES, UNIT_CHOICES
from libs.db_func import update_file_path, STOCK_IMAGE_PATH
from libs.fields import SizeRestrictedThumbnailerField, CustomJsonField
from libs.models import CustomModel
from libs.utils import get_absolute_media_url
from outlets.category_models import Category
from outlets.signals import create_thumbnail


def item_image_path(instance, filename):
    return update_file_path(
        STOCK_IMAGE_PATH + 'item_{0}.{1}'.format(
          instance.display_name, filename.split('.')[-1]))


class BaseItem(CustomModel):
    class Meta:
        verbose_name_plural = "Item"

    display_name = models.CharField(_("Display name"), max_length=500, blank=False)
    quantity = models.FloatField(_("UOM (Quantity)"), default=1, help_text=_("1.5 in 1.5 liters"),
                                 validators=[MinValueValidator(0, message=_("Quantity is below allocation.")),
                                             MaxValueValidator(100000, message=_("Quantity exceeds maximum allocation.")
                                                               ),
                                             ], blank=False, null=False)
    unit = models.CharField(_("UOM (Unit)"), max_length=20, choices=UNIT_CHOICES, help_text=_("liters in 1.5 liters"))

    search_fields = CustomJsonField(default=dict(), blank=True)  # auto
    filters = ArrayField(default=list(), base_field=models.CharField(max_length=400), null=True, blank=True)

    image = SizeRestrictedThumbnailerField(_("Image"), upload_to=item_image_path, null=True, blank=False,
                                           max_upload_size=10485760, resize_source=dict(size=(800, 0), sharpen=True,
                                                                                        replace_alpha="#fff"),
                                           help_text="`max_file_size`: 10 MB")
    # image2 = SizeRestrictedThumbnailerField(_("Different View Image"), upload_to=item_image_path_2, blank=True,
    #                                         null=True, max_upload_size=10485760,
    #                                         help_text="Optional; `max_file_size`: 10 MB",
    #                                         resize_source=dict(size=(800, 0), sharpen=True, replace_alpha="#fff"))
    # image3 = SizeRestrictedThumbnailerField(_("Different View Image"), upload_to=item_image_path_3, blank=True,
    #                                         null=True, max_upload_size=10485760,
    #                                         help_text="Optional; `max_file_size`: 10 MB",
    #                                         resize_source=dict(size=(800, 0), sharpen=True, replace_alpha="#fff"))
    # image4 = SizeRestrictedThumbnailerField(_("Different View Image"), upload_to=item_image_path_4, blank=True,
    #                                         null=True, max_upload_size=10485760,
    #                                         help_text="Optional; `max_file_size`: 10 MB",
    #                                         resize_source=dict(size=(800, 0), sharpen=True, replace_alpha="#fff"))

    thumbnail = models.ImageField(_("thumbnail"), upload_to="photos/thumbnails/",
                                  default='NA.png.120x120_q85_crop.jpg', blank=True)

    def __str__(self):
        return OutletItem.objects.get(id=self.id).__str__()


class OutletItem(BaseItem):
    type1 = models.ForeignKey(Category, verbose_name=_("Category"), related_name="first", on_delete=models.CASCADE)
    type2 = models.ForeignKey(Category, verbose_name=_("Sub-Category"), related_name="second", on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s %s) in %s > %s" % (self.display_name, self.quantity, self.unit, self.type1.get_display_name(),
                                          self.type2.get_display_name())

    def get_display_name(self):
        return "{} in {} - {}".format(self.display_name, self.type2.get_display_name(), self.type1.get_display_name())


class OutletStock(CustomModel):
    deleted = models.BooleanField(_("Deleted"), default=False)

    item = models.ForeignKey(OutletItem, verbose_name=_("Item"), on_delete=models.CASCADE)
    brand = models.CharField(_("Brand"), max_length=100, blank=False, default="Generic")
    country = models.CharField(_("Country of origin"), max_length=100, blank=False, default="UAE",
                               validators=[RegexValidator(regex=r'^[a-zA-Z ]+$',
                                                          message=_("Country can only have characters and spaces."))
                                           ]
                               )
    outlet = models.ForeignKey("outlets.Outlet", verbose_name=_("Outlet"), on_delete=models.CASCADE)
    sku = models.CharField(_("S.K.U stock code"), max_length=40)
    available = models.IntegerField(_("Online Shopping Quantity"), default=0, blank=True,
                                    # info store's stock have blankable `available`field
                                    help_text=_("'35' items available in infinia stock"),
                                    validators=[
                                        MinValueValidator(0, message=_("Minimum value should be zero."), )
                                    ])
    minimum_quantity = models.IntegerField(_("Minimum to be in cart"), default=0, blank=True,
                                           validators=[
                                               MinValueValidator(0, "Minimum value can only be zero")
                                           ],
                                           help_text=_("least number of this item to be bought"))
    maximum_quantity = models.IntegerField(_("Maximum to be in cart"), null=True, blank=True,
                                           validators=[
                                               MaxValueValidator(1000, "Maximum value 1000 for now.")
                                           ],
                                           help_text=_("max number of this item can be bought"))
    price = models.FloatField(_("Selling Price"), default=1, help_text=_("Enter price here!"),
                              validators=[MinValueValidator(0.1, message=_("Price is below allocation.")),
                                          MaxValueValidator(1000000, message=_("Price exceeds maximum allocation.")),
                                          ])
    currency = models.FloatField(_("Currency"), choices=CURRENCY_CHOICES, help_text=_("Choose currency"),
                                 max_length=20)
    description = models.TextField(_("Description"), help_text=_("short description for customers"), null=True,
                                   blank=True)

    extra = CustomJsonField(_("Other details"),
                            help_text=_('{"old_price": 299, "discount": 0.05}'), blank=True,
                            null=True)
    ratings = models.FloatField(_("Rating"), default=0.0,
                                validators=[
                                    MinValueValidator(0, message=_("Price is below minimum allocation.")),
                                    MaxValueValidator(5, message=_("Price exceeds maximum allocation.")),
                                ]
                                )
    rating_counts = models.IntegerField(_("Rating Counts"), default=0,
                                        validators=[
                                            MinValueValidator(0, message=_("Number of Ratings is below zero.")),
                                        ]
                                        )

    @property
    def thumbnail(self):
        return self.item.thumbnail

    def get_thumbnail_name(self):
        return self.thumbnail.name

    def get_thumbnail(self):
        if self.thumbnail:
            return get_absolute_media_url(self.thumbnail.name)

    def get_item_name(self):
        # excludes store
        return "%s %s" % (self.item, self.sku)

    def get_price_per_item(self, **kwargs):
        return self.price

    def __str__(self):
        return "%s %s (%s)" % (self.item, self.sku, self.outlet)

    class Meta:
        unique_together = (("outlet", "sku", "deleted"),)


post_save.connect(create_thumbnail, sender=BaseItem)


class PriceModifiers(models.Model):
    pass


'''class Stock(models.Model):
    class Meta:
        verbose_name_plural = "Stock"
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.FloatField("Quantity", max_length=25, blank=False)
    sku = models.CharField("S.K.U stock code", max_length=40)

    def __str__(self):
        return self.item
'''

"""class Customer(models.Model):
    first_name = models.CharField("First Name", max_length=50, blank=False)
    middle_name = models.CharField("Middle Name", max_length=50, blank=True, null=True)
    last_name = models.CharField("Last Name", max_length=50, blank=False)
    home_Address = models.CharField("Home Address", max_length=50, blank=False)
    work_Address = models.CharField("Work Address", max_length=50, blank=True, null=True)
    mobile_number = models.CharField("Alternative Number", validators=[PHONE_REGEX], max_length=17)


class DeliveryAddress(models.Model):
    country = models.CharField("Country",
                               choices=COUNTRY_CHOICES,
                               max_length=100)
    name = models.CharField("Full Name", max_length=100)  # full_name
    city = models.CharField("City",
                            # choices=CITY_CHOICES,
                            max_length=100)
    area = models.CharField("Area",
                            # choices=area_choices,
                            max_length=100)
    building = models.CharField("Building Name/No.", max_length=50)
    nearest_landmark = models.CharField("Nearest Landmark", max_length=100)

    mobile_number = models.CharField("Alternative Number", validators=[PHONE_REGEX], max_length=17)
    type = models.CharField("Address Type", max_length=10, choices=ADDRESS_CHOICES)

    alternative_email = models.EmailField("Alternative Email", validators=[EmailValidator()], blank=True, null=True)
    floor = models.CharField("Floor No.", max_length=20, blank=True, null=True)
    apartment = models.CharField("Apartment No.", max_length=20, blank=True, null=True)
    company = models.CharField("Company Name", max_length=40, blank=True, null=True)
    room = models.CharField("Room Number", max_length=20, blank=True, null=True)
    street = models.CharField("Street Name/No.", max_length=100, blank=True, null=True)
    latitude = models.FloatField("Latitude")
    longitude = models.FloatField("Longitude")


class OutletEmployee():
    email = models.EmailField('email address', unique=True, validators=[
        EmailValidator()
    ])
    password = models.CharField('password', max_length=128, null=True)  # nullable for facebook/google
    username = models.CharField(
        'username',
        null=True,
        blank=True,
        max_length=150,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        #validators=[AbstractUser.username_validator],
    )
    # = SizeRestrictedThumbnailerField(_("Profile Image"), upload_to=update_user_image_path, null=True, blank=True,
                                          # max_upload_size=5242880, resize_source=dict(size=(600, 0)),
                                          # default='NA.png', help_text=_("Optional"))
    thumbnail = models.ImageField("thumbnail", upload_to="photos/thumbnails/users/",
                                  default='NA.png.250x250_q85_crop.jpg', blank=True)
    digital_sign = models.CharField(max_length=15, blank=True, null=True)
    mobile_number = models.CharField("Contact Number", validators=[PHONE_REGEX], max_length=17, null=True,
                                     blank=True)
    associated_outlet = models.ManyToManyField('shop.InfiniaStore', blank=True)
    last_feed_access = models.DateTimeField("Last Feed Access Date", null=True, blank=True)
    last_feed_count = models.IntegerField("Last Feed Count", blank=True, default=0)


#employee rights and roles todo


class Orders(models.Model):
    outlet = models.CharField("Outlet", max_length=50, blank= False)
    #ordered_item =kun item ko foreign key
    status = models.CharField("Status", choices=ORDER_STATUS,max_length= 20)
    order_time = models.DateTimeField("Ordered Time")
    order_type = models.CharField("Order Type", max_length=50, choices=(("Gift a Friend", "Gift a Friend"),("hello", "abc")))


"""