from django.db import models
from outlets.outlet_models import Outlet


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Category"
    category_name = models.CharField("Category", max_length=50, blank=False)

    def __str__(self):
        return self.category_name


class Flavour(models.Model):
    class Meta:
        verbose_name_plural = "Flavour"
    flavour = models.CharField("Flavour", max_length=50, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="flavors", related_query_name="flavors")

    def __str__(self):
        return self.flavour


class Size(models.Model):
    class Meta:
        verbose_name_plural = "Size"
    size = models.CharField("Size", max_length=50, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.size


class SubCategory(models.Model):
    class Meta:
        verbose_name_plural = "Sub-Category"
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField("Sub Category", max_length=100)

    def __str__(self):
        return self.sub_category


class Item(models.Model):
    class Meta:
        verbose_name_plural = "Item"
    outlets = models.ManyToManyField(Outlet)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField("Item", max_length=100, blank=False)
    flavour = models.ForeignKey(Flavour, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    uom = models.CharField("UOM", max_length=50, blank=False)
    image = models.ImageField("Image")
    price = models.DecimalField("Price", decimal_places=2, max_digits=10)
    description = models.TextField("Description", max_length=500)
    quantity = models.FloatField("Quantity", max_length=25, blank=False)
    created_date = models.DateTimeField("Created Date")

    def __str__(self):
        return self.name


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
